# First Contribution Guide

👋 Welcome to ProfileForge! We are thrilled to have you here. Whether this is your first open-source contribution or your hundredth, we appreciate your interest in improving ProfileForge.

This guide will walk you through the step-by-step process of making your first contribution.

## Prerequisites

Before you start, make sure you have the following installed:
- **Python 3.9+**
- **Git**
- A **GitHub Account**

## 1. Fork the Repository

1. Navigate to the [ProfileForge GitHub Repository](https://github.com/iisgaurav/profileforge).
2. Click the **Fork** button in the top right corner.
3. Select your personal account as the destination.

## 2. Clone Locally

Clone your forked repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/profileforge.git
cd profileforge
```

## 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install Development Dependencies

Install ProfileForge with all the necessary development tools:

```bash
pip install -e ".[dev]"
```

## 5. Run Tests & Linter

Before making changes, verify that everything is working out of the box.

Run the test suite:
```bash
pytest tests/ -v
```

Run the linter to ensure code style consistency:
```bash
ruff check src/ tests/ tools/
```

Run the doctor command to verify your environment setup:
```bash
profileforge doctor
```

## 6. Find a Good First Issue

Not sure what to work on? We label beginner-friendly issues as `good first issue`. 
Check them out here: [Good First Issues](https://github.com/iisgaurav/profileforge/labels/good%20first%20issue).

*(You can also check `.github/good-first-issues/` for curated lists or ideas!)*

## 7. Create a Branch

Create a new branch for your feature or bugfix:

```bash
git checkout -b feat/my-contribution
```
*(Use prefixes like `feat/`, `fix/`, `docs/`, or `refactor/`)*

## 8. Make Changes and Write Tests

- Write your code.
- Ensure your code follows our style guidelines (run `ruff` to check).
- Write or update tests in the `tests/` directory to cover your changes.

## 9. Check the API Lock

If you modified any public APIs, ensure you run the API lock check to avoid accidental breaking changes:

```bash
python tools/api_lock.py --check
```

## 10. Open a Pull Request (PR)

1. Commit your changes: `git commit -m "feat: add my new feature"`
2. Push your branch to your fork: `git push origin feat/my-contribution`
3. Go to the original ProfileForge repository on GitHub.
4. Click **New Pull Request** and select your branch.
5. Fill out the PR template with a clear description of your changes. **Keep it small and focused.**

## What to Expect Next?

Our reviewers will look at your PR within **3-5 business days**.
Expect kind, constructive feedback. We are here to help you get your code merged!

## Need Help?

Join our community! You can reach us on GitHub Discussions or through our other community channels. Happy coding! 🎉
