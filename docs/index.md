# Getting Started with ProfileForge

ProfileForge is a declarative engine for building developer profiles. It takes configuration files (`yaml`), processes them through extensible `Widgets`, builds a component tree, and renders SVGs that you can display on your GitHub Profile.

## Installation

```bash
pip install profileforge
```

## Quick Start (5 Minutes)

1. Scaffold a new profile:
```bash
profileforge new my-profile
cd my-profile
```

2. Edit your configurations in `config/`.

3. Generate the widgets:
```bash
profileforge build
```

4. Display them in your `README.md`!
