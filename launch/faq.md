# ProfileForge Frequently Asked Questions (FAQ)

**1. How do I install ProfileForge?**
Simply run `pip install profileforge` in your terminal. It's hosted on PyPI.

**2. Do I need a GitHub Token?**
Yes, to fetch your statistics, commits, and repository data, you need a standard GitHub Personal Access Token (PAT). Set it as an environment variable: `export GITHUB_TOKEN=your_token`.

**3. What versions of Python are supported?**
ProfileForge requires Python 3.9 or higher.

**4. How do I automate this with GitHub Actions?**
ProfileForge is designed for automation. In ProfileForge Studio, click "Export" and select "GitHub Action". It will give you a `.github/workflows/profile.yml` file that runs `profileforge build` every night and commits the fresh SVGs to your repository.

**5. Can I create my own custom widgets?**
Absolutely. You can subclass the Python `BaseWidget` class, define your data fetching logic, and provide your own SVG template. 

**6. Can I create my own themes?**
Yes! In your `profile.yaml`, you can define custom color hex codes under the `theme` key if you don't want to use one of the 14 built-in themes.

**7. What is ProfileForge Studio?**
It's a visual, browser-based builder located in `web/index.html`. It lets you construct your profile using drag-and-drop mechanics and exports the corresponding YAML, so you never have to write code if you don't want to.

**8. How does the layout engine work?**
ProfileForge uses a simple grid-based layout defined in your YAML. You specify rows and columns, and the engine automatically sizes the SVGs to fit perfectly next to each other in your README.

**9. Can I run this in CI/CD pipelines other than GitHub Actions?**
Yes, since it's just a Python CLI tool, you can run it in GitLab CI, CircleCI, or Jenkins.

**10. How can I contribute?**
We welcome contributions! Check out our `CONTRIBUTING.md` file. We have several issues labeled `good first issue` to help you get started.

**11. Why did you choose YAML instead of JSON or Python for config?**
YAML provides the best balance of human-readability and declarative structure. It's clean, doesn't require brackets, and is standard across DevOps tooling.

**12. What are "Connectors"?**
Connectors are the data-fetching layer of ProfileForge. They reach out to APIs (GitHub GraphQL, Spotify, Dev.to RSS) asynchronously to pull the raw data needed for your widgets.

**13. How do the persona templates work?**
When you run `profileforge new --template <name>`, it generates a pre-configured YAML file optimized for that persona (e.g., frontend, data scientist, maintainer) with appropriate widgets and layouts.

**14. What is `render_safe()`?**
`render_safe()` is our architectural isolation layer. If a connector fails (e.g., Spotify API is down), `render_safe()` catches the error and renders a fallback for that specific widget. It ensures your entire build doesn't crash due to one bad API call.

**15. Where do I report a bug?**
Please open an issue on our GitHub repository with the steps to reproduce and the output of `profileforge doctor`.

**16. Is ProfileForge free?**
Yes, 100% free and open-source under the MIT License.

**17. Do I need to host the images anywhere?**
No. ProfileForge outputs raw `.svg` files directly into your repository. GitHub automatically serves them when someone views your README.

**18. How do I upgrade to the latest version?**
Run `pip install --upgrade profileforge`.

**19. What is the performance budget system?**
ProfileForge is optimized for speed. By doing all DOM assembly locally rather than relying on dynamic web endpoints, we enforce a strict performance budget, ensuring sub-15ms rendering times.

**20. Will there be a plugin ecosystem?**
Yes! We are working on an architecture that will allow the community to publish custom ProfileForge widgets and connectors directly to PyPI.
