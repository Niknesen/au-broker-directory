#!/usr/bin/env python3
"""
Local development server for Best Brokers Australia.

Serves the static site/ folder with extensionless routing support
and adds submission endpoints:
  POST /api/reviews      -> data/submissions/reviews.jsonl
  POST /api/cases        -> data/submissions/cases.jsonl

Stdlib only (http.server).
"""
import json
import re
import socketserver
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
SITE_DIR = ROOT / "site"
SUBMISSIONS_DIR = ROOT / "data" / "submissions"
SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)
PORT = 8941

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE_DIR), **kwargs)

    def log_message(self, format, *args):
        pass  # quiet console

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def do_GET(self):
        # Clean path resolution for extensionless URLs
        parsed = urlparse(self.path)
        path = parsed.path
        
        # If requested path does not have an extension and is not root
        if not re.search(r"\.[a-zA-Z0-9]+$", path):
            normalized = path.rstrip("/")
            candidate_index = SITE_DIR / normalized.lstrip("/") / "index.html"
            candidate_html = SITE_DIR / f"{normalized.lstrip('/')}.html"
            
            if candidate_index.exists():
                self.path = f"{normalized}/index.html"
            elif candidate_html.exists():
                self.path = f"{normalized}.html"

        super().do_GET()

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path not in ("/api/reviews", "/api/cases", "/api/claims", "/api/corrections"):
            self._send_json(404, {"ok": False, "error": "Unknown endpoint."})
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._send_json(400, {"ok": False, "error": "Invalid submission payload."})
            return

        name = (data.get("name") or data.get("contact_name") or "").strip()
        email = (data.get("email") or "").strip()
        text = (data.get("text") or "").strip()
        broker_slug = (data.get("broker_slug") or "").strip()

        if not (name and email and text):
            self._send_json(400, {"ok": False, "error": "Please fill in all required fields."})
            return
        if not EMAIL_RE.match(email):
            self._send_json(400, {"ok": False, "error": "Please provide a valid email address."})
            return

        record = {
            "broker_slug": broker_slug,
            "broker_name": data.get("broker_name", ""),
            "name": name,
            "email": email,
            "phone": data.get("phone", ""),
            "text": text,
            "status": "pending",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }

        if self.path == "/api/reviews":
            try:
                rating = int(data.get("rating"))
            except (TypeError, ValueError):
                rating = None
            if rating not in (1, 2, 3, 4, 5):
                self._send_json(400, {"ok": False, "error": "Please select a valid star rating (1-5)."})
                return
            record["rating"] = rating
            outfile = SUBMISSIONS_DIR / "reviews.jsonl"
        elif self.path == "/api/cases":
            role = data.get("role", "client")
            record["role"] = role
            outfile = SUBMISSIONS_DIR / "cases.jsonl"
        else:
            outfile = SUBMISSIONS_DIR / "corrections.jsonl"

        with outfile.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        self._send_json(200, {"ok": True})


class ThreadingServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with ThreadingServer(("", PORT), Handler) as httpd:
        print(f"Serving {SITE_DIR} on http://localhost:{PORT}")
        print(f"Submissions saved to {SUBMISSIONS_DIR}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
