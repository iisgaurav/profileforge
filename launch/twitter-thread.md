# ProfileForge Twitter Launch Thread

**Tweet 1/12**
Your GitHub profile is your developer landing page. 
But maintaining it is a nightmare of copy-pasted Markdown and rate-limited API widgets. 

Today I'm launching ProfileForge 🛠️
A declarative GitHub Profile & SVG Widget Engine built in Python.

Thread 🧵👇

**Tweet 2/12**
ProfileForge changes how you build your profile. 
Instead of hacking together 10 different web services, you define what you want in a clean `profile.yaml` file. 

Run `profileforge build` and it generates beautiful, dynamic SVGs instantly.

**Tweet 3/12**
How it works:
1️⃣ Define your layout in YAML
2️⃣ Our engine fetches your GitHub/external data
3️⃣ Generates lightweight, optimized SVGs locally
4️⃣ Updates your README automatically

Zero external dependencies. Zero rate limits on your profile.

**Tweet 4/12**
Out of the box, you get 15 rich widgets. 
📊 Top Languages
📈 Contribution Graph
🎵 Spotify Currently Playing
📝 Recent Blog Posts
⭐ Starred Repos
...and more. All rendered beautifully as SVGs.

**Tweet 5/12**
Design matters. ProfileForge ships with 14 stunning color themes built-in. 
Whether you love Dracula, Nord, Monokai, or a clean Light mode, changing your entire profile's aesthetic is as easy as:
`theme: dracula` in your config.

**Tweet 6/12**
Don't want to write YAML? I get it.
Meet ProfileForge Studio 🎨
A visual, no-code builder. Pick templates, toggle widgets, change themes, and instantly preview your profile in the browser. It spits out the exact YAML you need.

**Tweet 7/12**
Let's talk performance. ⚡️
ProfileForge is incredibly fast. The Python engine hits sub-15ms build times and handles 100+ ops/sec. 
It uses a 6-layer declarative pipeline with `render_safe()` isolation—so if one API fails, your profile never breaks.

**Tweet 8/12**
Automation is key. 
ProfileForge plugs seamlessly into GitHub Actions. Set it up once, and your profile updates dynamically every day (or hour!) with your latest code, stats, and content. 
Set and forget.

**Tweet 9/12**
Not sure where to start? 
We've included 9 persona templates out of the box:
- The OSS Maintainer 🛠️
- The Frontend Designer 🎨
- The Data Scientist 📊
- The Backend Engineer ⚙️
Just run `profileforge new --template backend` to start.

**Tweet 10/12**
Technical Architecture 🏗️
Built with Python 3.9+. 
The core is a 6-layer pipeline: Config Parse → Data Fetch → Context Build → Widget Render → Layout Assembly → Output.
Everything is modular, making it ridiculously easy to write your own custom widgets.

**Tweet 11/12**
ProfileForge is 100% Open Source (MIT License). 
I built this to give developers control over their own brand. No locked-in platforms, no premium tiers. 
Just clean code and beautiful profiles.

**Tweet 12/12**
Stop copy-pasting SVG templates. Forge your GitHub profile. ⚒️

Install it now: `pip install profileforge`
Star the repo on GitHub: https://github.com/iisgaurav/profileforge

Would love your feedback! Let me know what widgets you want to see next. #Python #GitHub #OpenSource #DeveloperTools
