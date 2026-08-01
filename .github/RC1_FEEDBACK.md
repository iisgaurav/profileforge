# ProfileForge v1.0.0-rc1 — Community Feedback

Thank you for testing ProfileForge v1.0.0-rc1!

This issue collects structured feedback before the final v1.0.0 release.

## How to Test

1. Install: `pip install git+https://github.com/iisgaurav/profileforge.git@v1.0.0-rc1`
2. Scaffold: `profileforge new my-profile --template backend`
3. Build: `profileforge build`
4. Studio: Open `web/index.html` in your browser

## Feedback Areas

### Installation
- Did `pip install` succeed on your OS + Python version?
- Any dependency conflicts?

### CLI Experience
- Were error messages helpful?
- Was the output clear?

### Studio
- Did the Studio load without errors?
- Did the live preview work as expected?
- What felt missing?

### Widgets
- Which widgets did you use?
- Did any widget fail to render?

### Documentation
- Was anything unclear or missing?
- Did you find what you needed?

## Reporting Bugs

For bugs, open a separate issue using the Bug Report template.

## Exit Criteria

RC1 will be promoted to v1.0.0 after:
- No critical bugs remain open
- No installation failures reported
- No API regressions confirmed
- 7-day feedback window closes
