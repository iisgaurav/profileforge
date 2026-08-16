import argparse
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

try:
    import cairosvg
except ImportError:
    cairosvg = None

try:
    from PIL import Image, ImageChops
except ImportError:
    Image = None


def parse_val(s, default=0.0):
    if not s:
        return default
    m = re.match(r"^-?[\d.]+", str(s))
    return float(m.group(0)) if m else default


def run_gallery_export(out_dir):
    print(f"[*] Running profileforge gallery export to {out_dir}...")
    result = subprocess.run(
        ["profileforge", "gallery", "export", "--out-dir", out_dir],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[!] Gallery export failed:\n{result.stderr}")
        return False
    return True


class SvgAccessibilityValidator:
    VALID_ROLES = frozenset({"img", "presentation", "group", "term", "meter"})
    REQUIRED_ATTRIBUTES = frozenset({"title", "desc", "aria-labelledby", "aria-label"})

    @classmethod
    def validate(cls, root: ET.Element) -> list[str]:
        issues = []
        has_required_attr = False

        for elem in root.iter():
            if elem.tag.endswith("title") or elem.tag.endswith("desc"):
                has_required_attr = True

            for attr in cls.REQUIRED_ATTRIBUTES:
                if attr in elem.attrib:
                    has_required_attr = True

            if "role" in elem.attrib and elem.attrib["role"] not in cls.VALID_ROLES:
                issues.append(f"Invalid ARIA role: {elem.attrib['role']}")

        if not has_required_attr:
            issues.append(
                f"Missing A11y tags or attributes: {', '.join(cls.REQUIRED_ATTRIBUTES)}"
            )

        return issues


def validate_svg_and_bounds(svg_path):
    issues = []
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            root = ET.fromstring(f.read())
    except Exception as e:
        return [f"Invalid SVG XML: {e}"]

    width = parse_val(root.attrib.get("width", "820"))
    height = parse_val(root.attrib.get("height", "140"))
    viewbox = root.attrib.get("viewBox", "")
    if viewbox and not re.match(r"^[\d\.\s-]+$", viewbox):
        issues.append("Invalid viewBox format")

    # A11y Check
    issues.extend(SvgAccessibilityValidator.validate(root))

    # IDs Check
    ids = set()

    for elem in root.iter():
        elem_id = elem.attrib.get("id")
        if elem_id:
            if elem_id in ids:
                issues.append(f"Duplicate SVG ID found: {elem_id}")
            ids.add(elem_id)

        if elem.tag.endswith("g") and len(elem) == 0 and not elem.text:
            issues.append("Empty group <g> tag detected")

        # Check references (gradients, filters)
        fill = elem.attrib.get("fill", "")
        if fill.startswith("url(#"):
            ref_id = fill[5:-1]
            # Pytest warns about truth values of elements. Use 'is not None'
            if root.find(f".//*[@id='{ref_id}']") is None:
                issues.append(f"Broken reference to gradient/filter: {ref_id}")

    # Bounds Check
    for elem in root.iter():
        if elem.tag.endswith("text") or elem.tag.endswith("rect"):
            x = parse_val(elem.attrib.get("x", "0"))
            y = parse_val(elem.attrib.get("y", "0"))

            if elem.tag.endswith("text"):
                txt = elem.text or ""
                fs = parse_val(elem.attrib.get("font-size", "14"))
                elem_w = len(txt) * fs * 0.6
                elem_h = fs
                anchor = elem.attrib.get("text-anchor", "start")
                if anchor == "middle":
                    x -= elem_w / 2
                elif anchor == "end":
                    x -= elem_w
            else:
                elem_w = parse_val(elem.attrib.get("width", "0"))
                elem_h = parse_val(elem.attrib.get("height", "0"))

            if elem_w >= width * 0.9 and elem_h >= height * 0.9:
                continue

            if elem.tag.endswith("text"):
                if x < -50 or x + elem_w > width + 70:
                    issues.append(f"Text '{txt}' at x={x} overflows width={width}")
                if y > height + 20 or y < 0:
                    issues.append(f"Text '{txt}' at y={y} overflows height={height}")
            else:
                if x < 0 or x + elem_w > width + 5:
                    issues.append(f"Rect at x={x} overflows width={width}")
                if y < 0 or y + elem_h > height + 5:
                    issues.append(f"Rect at y={y} overflows height={height}")

    return issues


def render_png(svg_path, png_path):
    if not cairosvg:
        return False
    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        return True
    except Exception as e:
        print(f"[!] PNG render failed for {svg_path}: {e}")
        return False


def generate_diff(baseline_png, current_png, diff_png):
    if not Image:
        return False, False
    if not os.path.exists(baseline_png) or not os.path.exists(current_png):
        return False, False

    try:
        img1 = Image.open(baseline_png).convert("RGB")
        img2 = Image.open(current_png).convert("RGB")

        diff = ImageChops.difference(img1, img2)
        if diff.getbbox():
            diff.save(diff_png)
            return True, True  # Differences exist, diff saved
        return True, False  # No differences
    except Exception as e:
        print(f"[!] Diff generation failed: {e}")
        return False, False


def check_design_qa_exists(workspace_root):
    return os.path.exists(os.path.join(workspace_root, "DESIGN_QA.md"))


def main():
    parser = argparse.ArgumentParser(description="ProfileForge Visual QA Pipeline")
    parser.add_argument(
        "--baseline-dir",
        default="artifacts/baseline",
        help="Baseline gallery directory",
    )
    parser.add_argument(
        "--current-dir", default="artifacts/current", help="Current gallery directory"
    )
    parser.add_argument(
        "--diff-dir", default="artifacts/diff", help="Diff output directory"
    )
    parser.add_argument(
        "--require-qa",
        action="store_true",
        help="Fail if differences exist and DESIGN_QA.md is missing",
    )

    args = parser.parse_args()

    os.makedirs(args.current_dir, exist_ok=True)
    os.makedirs(args.diff_dir, exist_ok=True)

    if not run_gallery_export(args.current_dir):
        sys.exit(1)

    assets_dir = os.path.join(args.current_dir, "assets")
    svgs = [f for f in os.listdir(assets_dir) if f.endswith(".svg")]

    total_issues = 0
    visual_changes = 0

    print(f"\n[*] Validating {len(svgs)} SVG widgets...")
    for svg_file in svgs:
        svg_path = os.path.join(assets_dir, svg_file)

        # 1. Validate SVG, Bounds, A11y
        issues = validate_svg_and_bounds(svg_path)
        if issues:
            print(f"  [X] {svg_file} failed QA:")
            for issue in issues:
                print(f"      - {issue}")
            total_issues += len(issues)

        # 2. Render PNG & Diff
        baseline_png = os.path.join(args.baseline_dir, svg_file.replace(".svg", ".png"))
        current_png = os.path.join(args.current_dir, svg_file.replace(".svg", ".png"))
        diff_png = os.path.join(args.diff_dir, svg_file.replace(".svg", "-diff.png"))

        if render_png(svg_path, current_png):
            if os.path.exists(baseline_png):
                success, has_diff = generate_diff(baseline_png, current_png, diff_png)
                if success and has_diff:
                    print(f"  [~] {svg_file} has visual changes. Diff saved.")
                    visual_changes += 1

    print("\n--- Visual QA Summary ---")
    print(f"Total SVGs Checked: {len(svgs)}")
    print(f"Objective Issues:   {total_issues}")
    print(f"Visual Changes:     {visual_changes}")

    if total_issues > 0:
        print("\n[!] CI FAILED: Objective automated QA gates failed.")
        sys.exit(1)

    if visual_changes > 0 and args.require_qa:
        if not check_design_qa_exists(os.getcwd()):
            print(
                "\n[!] CI FAILED: Visual changes detected but DESIGN_QA.md is missing."
            )
            sys.exit(1)
        else:
            print("\n[OK] Visual changes detected. DESIGN_QA.md is present for review.")

    print("\n[OK] Pipeline completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
