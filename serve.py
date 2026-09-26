from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent / "dist"

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def translate_path(self, path):
        translated = super().translate_path(path)
        relative = Path(translated).relative_to(Path.cwd())
        return str(ROOT / relative)

    def do_GET(self):
        requested = ROOT / self.path.split("?", 1)[0].lstrip("/")
        if self.path.split("?", 1)[0].endswith("/") or not requested.exists():
            self.path = "/index.html"
        return super().do_GET()

ThreadingHTTPServer(("0.0.0.0", 4173), Handler).serve_forever()
