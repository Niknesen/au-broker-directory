"""
Crawlable, SEO-friendly Pagination Component for Hub Pages.
"""
from typing import Optional


def render_pagination(base_url: str, current_page: int, total_pages: int) -> str:
    """
    Renders sequential, crawlable HTML pagination.
    Uses real <a href> links.
    """
    if total_pages <= 1:
        return ""

    def get_url(page: int) -> str:
        if page == 1:
            return base_url
        clean_base = base_url.rstrip("/")
        return f"{clean_base}/?page={page}"

    links = []

    # Prev link
    if current_page > 1:
        links.append(f'<a class="page-link" href="{get_url(current_page - 1)}" rel="prev" aria-label="Previous page">&larr; Prev</a>')
    else:
        links.append('<span class="page-link disabled" aria-hidden="true">&larr; Prev</span>')

    # Page numbers
    # Show first, last, and window around current
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, current_page + 2)

    if start_page > 1:
        links.append(f'<a class="page-link" href="{get_url(1)}">1</a>')
        if start_page > 2:
            links.append('<span class="page-link disabled">&hellip;</span>')

    for p in range(start_page, end_page + 1):
        if p == current_page:
            links.append(f'<span class="page-link active" aria-current="page">{p}</span>')
        else:
            links.append(f'<a class="page-link" href="{get_url(p)}">{p}</a>')

    if end_page < total_pages:
        if end_page < total_pages - 1:
            links.append('<span class="page-link disabled">&hellip;</span>')
        links.append(f'<a class="page-link" href="{get_url(total_pages)}">{total_pages}</a>')

    # Next link
    if current_page < total_pages:
        links.append(f'<a class="page-link" href="{get_url(current_page + 1)}" rel="next" aria-label="Next page">Next &rarr;</a>')
    else:
        links.append('<span class="page-link disabled" aria-hidden="true">Next &rarr;</span>')

    return f"""
<nav class="pagination" aria-label="Pagination Navigation">
  {''.join(links)}
</nav>
"""
