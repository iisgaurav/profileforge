import subprocess
import sys
import time
from pathlib import Path

from colorama import Fore, Style


def rebuild_all():
    print(f"\n{Fore.CYAN}🚀 Full Rebuild Triggered{Style.RESET_ALL}")
    
    start = time.perf_counter()
    try:
        subprocess.run(
            [sys.executable, "-m", "profileforge.cli.main", "gallery", "export"],
            check=True,
            capture_output=True
        )
        t_gallery = (time.perf_counter() - start) * 1000
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Gallery Export    : {t_gallery:.0f}ms")
        
        print(f"{Fore.GREEN}✓ Rebuild complete in {t_gallery:.0f}ms{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}✗ Build failed: {e.stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")


def rebuild_incremental(modified_paths: list[str]):
    needs_full = False
    widgets_to_rebuild = set()
    themes_to_rebuild = set()

    for path in modified_paths:
        p = Path(path).resolve()
        try:
            rel = p.relative_to(Path.cwd() / "src" / "profileforge")
            if rel.parts[0] == "widgets" and rel.suffix == ".py":
                widgets_to_rebuild.add(rel.stem)
            elif rel.parts[0] == "themes" and rel.suffix == ".yaml":
                themes_to_rebuild.add(rel.stem)
            else:
                needs_full = True
        except ValueError:
            needs_full = True

    if needs_full or not (widgets_to_rebuild or themes_to_rebuild):
        rebuild_all()
        return

    start = time.perf_counter()
    
    if widgets_to_rebuild:
        for w in widgets_to_rebuild:
            print(f"{Fore.CYAN}↻ Rebuilding {w} widget...{Style.RESET_ALL}")
            # Just rebuild the gallery to update all themes for this widget
            # To be truly incremental, we'd only rebuild this specific SVG, but 
            # for now gallery export is fast enough or we can filter it.
            # A full gallery export takes ~200ms anyway.
            # Let's just run gallery export for safety in v1.
            try:
                subprocess.run(
                    [sys.executable, "-m", "profileforge.cli.main", "gallery", "export"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                 print(f"{Fore.RED}✗ Build failed: {e.stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
                 return

    if themes_to_rebuild:
        for t in themes_to_rebuild:
            print(f"{Fore.CYAN}↻ Rebuilding {t} theme...{Style.RESET_ALL}")
            try:
                subprocess.run(
                    [sys.executable, "-m", "profileforge.cli.main", "gallery", "export"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                 print(f"{Fore.RED}✗ Build failed: {e.stderr.decode('utf-8', errors='ignore')}{Style.RESET_ALL}")
                 return
                 


    elapsed = (time.perf_counter() - start) * 1000
    print(f"{Fore.GREEN}✓ Completed in {elapsed:.0f}ms{Style.RESET_ALL}")
