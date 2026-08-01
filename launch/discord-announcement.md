# ProfileForge Discord Announcements

## 1. Python Discord (Focus: Architecture & Tech Stack)

**Channel:** `#showcase` or `#open-source`

Hey pythonistas 👋 I just open-sourced a new CLI tool built entirely in Python 3.9+ called **ProfileForge**. It’s a declarative engine that takes YAML configurations and generates dynamic SVG widgets for your GitHub profile. 

I wanted to share it here because I spent a lot of time optimizing the Python architecture. It uses an asynchronous 6-layer pipeline (Parse → Fetch → Context → Render → Assemble → Output) that manages to hit sub-15ms build times and >100 ops/sec. I also implemented a `render_safe()` isolation layer so that if external APIs timeout during the fetch phase, the build falls back gracefully instead of crashing. 

You can check out the source code here: https://github.com/iisgaurav/profileforge. Would love any feedback from this community on the codebase or ideas for optimizing the SVG templating even further!

## 2. OSS Discord (Focus: Collaboration & Contribution)

**Channel:** `#project-showcase` or `#looking-for-contributors`

Hey everyone! If you maintain open-source projects, you know how important a clean GitHub profile is for your brand. I got tired of dealing with rate-limited, broken SVGs on my profile, so I built **ProfileForge** (MIT Licensed).

It's a local-first engine that lets you define your GitHub profile in clean YAML and renders static SVGs via GitHub Actions. It ships with 15 widgets, 14 themes, and a no-code visual builder.

We just launched v1 and are looking to grow the community! If you're looking for an open-source project to contribute to, we have a bunch of `good first issue` tags open for adding new widgets, themes, and API connectors. 
Check it out: https://github.com/iisgaurav/profileforge 🌟

## 3. GitHub Community Discord (Focus: End-User Value)

**Channel:** `#github-showcase` or `#general`

Hey folks! Tired of your GitHub profile README looking like a messy wall of copy-pasted markdown and broken image links? 

I just released **ProfileForge** 🛠️. It's a tool that lets you generate an amazing, dynamic GitHub profile without touching markdown. You just write a simple YAML file (or use our visual drag-and-drop Studio), and it generates beautiful SVG widgets for your top languages, commit graphs, recent blogs, and more. 

Because it runs locally or via GitHub actions, you never have to worry about third-party servers going down and breaking your profile. You can try it out with `pip install profileforge`. 

Repo is here if you want to see some examples: https://github.com/iisgaurav/profileforge. Let me know what you think of the themes!
