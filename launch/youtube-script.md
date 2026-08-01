# ProfileForge YouTube Demo Script

**Target Length:** 3 minutes

### [0:00] Hook - The Problem (30s)
**Audio:** "This is a standard GitHub profile. It’s okay, but it doesn't really say much about you as a developer. Now, you could spend hours hacking together external APIs, copy-pasting markdown, and relying on third-party servers to render your stats... hoping they don't get rate-limited and break your images."
**Visual:** [Screen shows a very basic, plain GitHub profile. Fast forward montage of someone furiously searching Google for 'github profile readme generator', copying messy markdown code, and an image showing a broken SVG link icon.]

### [0:30] The Solution (30s)
**Audio:** "There has to be a better way. Meet ProfileForge. It’s a declarative GitHub Profile and SVG Widget Engine. Instead of a messy README, you define your profile in simple YAML, and ProfileForge generates beautiful, static SVGs locally in milliseconds. Let me show you how fast it is."
**Visual:** [Title card: ProfileForge. Smooth transition to a beautifully crafted, complex GitHub profile with multiple widgets, perfectly themed.]

### [1:00] CLI Demo (60s)
**Audio:** "Since it's built in Python, installation is just `pip install profileforge`."
**Visual:** [Terminal window pops up. User types `pip install profileforge`.]
**Audio:** "To start, we’ll run `profileforge new my-profile` and let's use the backend template."
**Visual:** [User types `profileforge new my-profile --template backend`. Directory is created.]
**Audio:** "This gives us a clean `profile.yaml`. Before we build, let's run `profileforge doctor` to make sure our environment and GitHub tokens are set up."
**Visual:** [User types `cd my-profile`, then `profileforge doctor`. Green checkmarks appear on screen.]
**Audio:** "Everything looks good. Now, we just type `profileforge build`."
**Visual:** [User types `profileforge build`. The terminal outputs sub-15ms build times. User opens the generated `README.md` and SVGs to show the beautiful output.]
**Audio:** "In under 15 milliseconds, it fetched my data, ran it through a 6-layer pipeline, and generated these SVGs. No rate limits, completely local."

### [2:00] Studio Demo (45s)
**Audio:** "But what if you don't want to write YAML? We built ProfileForge Studio, a completely local visual builder. Just open `index.html` in the web folder."
**Visual:** [Browser opens to ProfileForge Studio UI.]
**Audio:** "Here, I can pick a template, let's say the Open Source Maintainer. I can toggle on the Spotify widget, turn off the blog posts, and easily swap the theme to Dracula."
**Visual:** [Cursor clicks through the UI, toggling widgets. Clicks a dropdown and selects 'Dracula'. The preview window updates instantly.]
**Audio:** "Once it looks perfect, you just copy the generated YAML or the GitHub Action workflow right here."
**Visual:** [Cursor clicks the 'Copy YAML' button.]

### [2:45] Call to Action (15s)
**Audio:** "ProfileForge comes with 15 widgets, 14 themes, and it’s 100% open source under the MIT license. Stop copy-pasting code, and forge your profile. Star the repo on GitHub, check out our good-first-issues, and let us know what widget you want to see next."
**Visual:** [End screen: ProfileForge Logo. URL: github.com/iisgaurav/profileforge. 'pip install profileforge'. GitHub Star animation.]
