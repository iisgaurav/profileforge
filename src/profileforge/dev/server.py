import http.server
import os
import socketserver
import threading

from colorama import Fore, Style

from profileforge.dev.events import livereload_bus

LIVERELOAD_SCRIPT = b"""
<script>
  const eventSource = new EventSource('/livereload');
  eventSource.onmessage = function(e) {
    if (e.data === 'RELOAD') {
      console.log('Live reload triggered');
      window.location.reload();
    }
  };
</script>
"""


class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress standard logging to keep console clean
        pass

    def translate_path(self, path):
        # Strip query string and fragments like SimpleHTTPRequestHandler does
        path = path.split("?", 1)[0].split("#", 1)[0]

        if path.startswith("/gallery/"):
            # The server runs in the 'web' directory, but 'gallery' is in the repo root
            return os.path.abspath(os.path.join(os.getcwd(), "..", path.lstrip("/")))
        return super().translate_path(path)

    def end_headers(self):
        # Force browser to never cache SVGs or assets during development
        self.send_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path == "/livereload":
            self.send_response(200)
            self.send_header("Content-type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            q = livereload_bus.subscribe()
            try:
                # Send initial connection success
                self.wfile.write(b"data: CONNECTED\n\n")
                self.wfile.flush()

                while True:
                    msg = q.get()
                    self.wfile.write(f"data: {msg}\n\n".encode("utf-8"))
                    self.wfile.flush()
            except Exception:
                pass
            finally:
                livereload_bus.unsubscribe(q)
            return

        # Serve normal files
        try:
            # Map request to local file in web/
            path = self.translate_path(self.path)
            if os.path.isdir(path):
                path = os.path.join(path, "index.html")

            if path.endswith(".html") and os.path.exists(path):
                with open(path, "rb") as f:
                    content = f.read()

                # Inject livereload script before </head>
                if b"</head>" in content:
                    content = content.replace(
                        b"</head>", LIVERELOAD_SCRIPT + b"</head>"
                    )
                else:
                    content += LIVERELOAD_SCRIPT

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        except Exception:
            pass

        return super().do_GET()


def start_server(port: int, directory: str):
    os.chdir(directory)
    handler = LiveReloadHandler

    # Allow port reuse
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    try:
        httpd = socketserver.ThreadingTCPServer(("", port), handler)
        print(
            f"  {Fore.GREEN}✓{Style.RESET_ALL} Studio Server : http://localhost:{port}/"
        )

        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        return httpd
    except Exception as e:
        print(
            f"  {Fore.RED}✗{Style.RESET_ALL} Failed to start server on port {port}: {e}"
        )
        return None
