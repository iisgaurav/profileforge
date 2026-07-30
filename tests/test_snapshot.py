import re

def normalize_svg(svg_str: str) -> str:
    """Removes whitespace and insignificant ordering to perform stable structural comparison."""
    # Strip metadata comments that might have version diffs
    svg = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
    # Remove all newlines
    svg = svg.replace('\n', '').replace('\r', '')
    # Remove multiple spaces
    svg = re.sub(r'\s+', ' ', svg)
    # Remove spacing around tags
    svg = re.sub(r'>\s+<', '><', svg)
    return svg.strip()

def test_svg_normalization():
    svg1 = '''
    <!-- Version 1 -->
    <svg width="100">
        <text>Hello</text>
    </svg>
    '''
    
    svg2 = '''<svg width="100"><text>Hello</text></svg>'''
    
    assert normalize_svg(svg1) == normalize_svg(svg2)
