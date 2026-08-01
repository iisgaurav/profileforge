# ProfileForge Demo Screencast Script

This script is for recording the raw screencast (GIF/Video) that will be embedded in the README and Product Hunt page. 

## Preparation
- Terminal resized to 80x24 for good visibility
- IDE (VS Code) open in the background
- Browser window ready with GitHub profile open

## Part 1: CLI Walkthrough (The "Aha" Moment)

1. **Install**
   ```bash
   pip install profileforge
   ```
   *(Wait for installation to complete, clear screen)*

2. **Scaffold New Profile**
   ```bash
   profileforge new my-profile --template backend
   ```
   *(Shows output: ✨ Created profile template 'backend' in ./my-profile)*

3. **Navigate & Verify**
   ```bash
   cd my-profile
   profileforge doctor
   ```
   *(Shows output: 
   ✅ Python 3.9+ found
   ✅ Config valid
   ✅ GitHub Token detected
   ✅ Ready to forge)*

4. **Build**
   ```bash
   profileforge build
   ```
   *(Shows output:
   [1/6] Parsing profile.yaml... Done
   [2/6] Fetching data... Done (0.8s)
   [3/6] Building context... Done
   [4/6] Rendering widgets (15 total)... Done
   [5/6] Assembling layout... Done
   [6/6] Writing outputs... Done
   🚀 Built successfully in 12ms!)*

5. **Show Result**
   - Quickly type `cat profile.yaml` to show how clean it is.
   - Switch to browser and refresh GitHub profile to show the newly generated SVGs perfectly aligned.

## Part 2: ProfileForge Studio (The No-Code Experience)

1. **Open Studio**
   - Open browser to local `file:///d:/WEB/profileforge/web/index.html`
   
2. **Visual Editing Sequence**
   - **Click:** "Templates" dropdown -> Select "Frontend Designer"
     *(Preview instantly updates to a more visual layout)*
   - **Click:** "Widgets" tab -> Toggle ON "Spotify Playing", Toggle OFF "Recent Commits"
     *(Preview adds the Spotify SVG at the bottom)*
   - **Click:** "Themes" palette -> Select "Nord" 
     *(Entire layout instantly switches color scheme)*
   - **Click:** "Export" button -> "Copy YAML Config"
     *(Notification: Copied to clipboard!)*

3. **End on Impact**
   - Paste the YAML back into the VS Code window, hit save.
   - Run `profileforge build` one last time to show the cycle is complete.
