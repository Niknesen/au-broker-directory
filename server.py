#!/usr/bin/env python3
"""
Minimal local server for the broker directory MVP.

Serves the static site/ folder and adds two POST endpoints so the review and
"real case" forms actually work end to end:

  POST /api/reviews   -> data/submissions/reviews.jsonl
  POST /api/cases     -> data/submissions/cases.jsonl

Deliberately not a real app server or database - one JSON object per line,
append-only, human-readable. Good enough to "store it somewhere and deal
with it later"; swap for a real backend once there's an actual moderation
workflow to build against.

Stdlib only (http.server) so there's nothing to install.
"""
import json
import re
import socketserver
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler
from pathlib import Path

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
        pass  # quiet console; uncomment during debugging if needed

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path not in ("/api/reviews", "/api/cases"):
            self._send_json(404, {"ok": False, "error": "Unknown endpoint."})
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._send_json(400, {"ok": False, "error": "Invalid submission."})
            return

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        text = (data.get("text") or "").strip()
        broker_slug = (data.get("broker_slug") or "").strip()

        if not (name and email and text and broker_slug):
            self._send_json(400, {"ok": False, "error": "Please fill in every field."})
            return
        if not EMAIL_RE.match(email):
            self._send_json(400, {"ok": False, "error": "That email address doesn't look right."})
            return

        record = {
            "broker_slug": broker_slug,
            "broker_name": data.get("broker_name", ""),
            "name": name,
            "email": email,
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
                self._send_json(400, {"ok": False, "error": "Please choose a star rating."})
                return
            record["rating"] = rating
            outfile = SUBMISSIONS_DIR / "reviews.jsonl"
        else:
            role = data.get("role")
            if role not in ("client", "broker"):
                self._send_json(400, {"ok": False, "error": "Please choose who you're submitting as."})
                return
            record["role"] = role
            outfile = SUBMISSIONS_DIR / "cases.jsonl"

        with outfile.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        self._send_json(200, {"ok": True})


class ThreadingServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with ThreadingServer(("", PORT), Handler) as httpd:
        print(f"Serving {SITE_DIR} on http://localhost:{PORT}")
        print(f"Submissions saved to {SUBMISSIONS_DIR}")
        httpd.serve_forever()
