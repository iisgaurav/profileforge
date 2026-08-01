# Community Registry Architecture (Spec)

This document outlines the technical specification and governance for the upcoming ProfileForge Community Registry.

## Overview
The Registry will allow users to share, discover, and install community-created widgets and themes via the CLI.

Future CLI integration:
```bash
profileforge install myuser/awesome-widget
profileforge search "dark theme"
profileforge publish
```

## Registry Metadata Schema
Packages in the registry will be defined by a `package.yaml` schema:

```yaml
id: "awesome-widget"
name: "Awesome Widget"
version: "1.0.0"
author: "@myuser"
description: "Displays awesome metrics."
download_url: "https://registry.profileforge.dev/packages/awesome-widget-1.0.0.tar.gz"
checksum: "sha256-..."
tags: ["metrics", "awesome"]
category: "widget"
min_profileforge_version: "1.0.0"
```

## Validation Pipeline
To ensure security and quality, all submissions will go through an automated pipeline:
1. **Schema Linting:** Verify `package.yaml`.
2. **Doctor Check:** Run `profileforge doctor` against the code.
3. **Automated Tests:** Execute the widget's test suite in an isolated CI environment.
4. **Human Review:** A maintainer must approve the first version of any new package.

## Security Model
Security is the highest priority when allowing third-party Python code.
- **Checksums:** All downloads are verified against their SHA256 checksums.
- **Sandboxed Imports:** Community widgets run in a restricted environment. They cannot import arbitrary OS modules like `subprocess` or `os.system`.
- **No Arbitrary Code Execution:** The rendering engine strictly sanitizes all outputs before generating SVGs.

## REST API Design
The CLI will communicate with the registry via a REST API:
- `GET /api/v1/packages` - List/search packages
- `GET /api/v1/packages/{id}` - Get package metadata
- `POST /api/v1/packages` - Publish a new package (Authenticated)

## Governance
- **Approvals:** Core Maintainers approve new registry submissions.
- **Deprecation:** Authors can mark packages as deprecated. Abandoned packages with critical bugs may be unlisted by maintainers to protect users.
