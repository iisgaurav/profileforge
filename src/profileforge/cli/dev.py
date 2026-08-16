import time
from pathlib import Path

from colorama import Fore, Style, init


def cmd_dev(args):
    init()  # Initialize colorama

    port = getattr(args, "port", 8000)
    no_browser = getattr(args, "no_browser", False)

    print(f"\n{Fore.CYAN}🚀 ProfileForge Dev Server{Style.RESET_ALL}\n")

    # 1. Initial Build
    print(f"{Fore.YELLOW}» Performing initial startup build...{Style.RESET_ALL}")
    from profileforge.dev.rebuild import rebuild_all

    rebuild_all()

    # 2. Start Studio Server
    server_httpd = None
    if not no_browser:
        from profileforge.dev.server import start_server

        web_dir = Path.cwd() / "web"
        if not web_dir.exists():
            print(
                f"  {Fore.RED}✗{Style.RESET_ALL} 'web/' directory not found. Studio server disabled."
            )
        else:
            server_httpd = start_server(port, str(web_dir))
    else:
        print(
            f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Studio Server : Disabled (--no-browser)"
        )

    # 3. Start Watcher
    from profileforge.dev.watcher import start_watcher

    watch_dirs = [
        str(Path.cwd() / "src" / "profileforge"),
        str(Path.cwd() / "templates"),
        str(Path.cwd() / "themes"),
    ]
    observer, watched = start_watcher(watch_dirs)

    print("\nWatching:")
    for w in watched:
        try:
            rel = Path(w).relative_to(Path.cwd())
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {rel}")
        except ValueError:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {w}")

    print(f"\nPress {Fore.YELLOW}Ctrl+C{Style.RESET_ALL} to stop\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Stopping dev server...{Style.RESET_ALL}")
        try:
            observer.stop()
            if server_httpd:
                server_httpd.shutdown()
            observer.join()
        except KeyboardInterrupt:
            import sys

            sys.exit(0)
