/**
 * ProfileForge Studio — app.js
 * Zero-dependency vanilla JS application
 */

'use strict';

// ============================================================
// STATE
// ============================================================
const state = {
  username: 'octocat',
  template: null,
  activeWidgets: new Set(),
  theme: 'github-dark',
  themes: [],
  widgets: [],
  templates: [],
};

// Theme color swatches for display
const THEME_SWATCHES = {
  'github-dark':   ['#58A6FF', '#D2A8FF', '#2EA043'],
  'github-light':  ['#0969DA', '#8250DF', '#1A7F37'],
  'dracula':       ['#FF79C6', '#BD93F9', '#50FA7B'],
  'nord':          ['#88C0D0', '#81A1C1', '#A3BE8C'],
  'modern':        ['#3B82F6', '#8B5CF6', '#10B981'],
  'vercel':        ['#FFFFFF', '#888888', '#3291FF'],
  'minimal':       ['#000000', '#666666', '#00CC00'],
  'apple':         ['#0071E3', '#AF52DE', '#34C759'],
  'catppuccin-mocha':    ['#89B4FA', '#CBA6F7', '#A6E3A1'],
  'catppuccin-frappe':   ['#8CAAEE', '#CA9EE6', '#A6D189'],
  'catppuccin-macchiato':['#8AADF4', '#C6A0F6', '#A6DA95'],
  'catppuccin-latte':    ['#1E66F5', '#8839EF', '#40A02B'],
  'catppuccin-base':     ['#58A6FF', '#D2A8FF', '#2EA043'],
  'showcase':      ['#FFD700', '#FF8C00', '#4CAF50'],
};

// ============================================================
// UTILITIES
// ============================================================
function $(id) { return document.getElementById(id); }

function showToast(message, type = 'success', duration = 3000) {
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const container = $('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type] || '💬'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 250);
  }, duration);
}

function setLoading(visible) {
  const overlay = $('loading-overlay');
  overlay.classList.toggle('hidden', !visible);
}

async function fetchJSON(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
  return response.json();
}

// ============================================================
// INITIALIZATION
// ============================================================
async function init() {
  setLoading(true);
  try {
    const [themes, widgets, templates] = await Promise.all([
      fetchJSON('./gallery/themes.json'),
      fetchJSON('./gallery/widgets.json'),
      fetchJSON('./gallery/templates.json'),
    ]);

    state.themes = themes;
    state.widgets = widgets;
    state.templates = templates;

    renderThemeGrid();
    renderWidgetList();
    renderTemplateSelector();
    setupEventListeners();
    renderPreview();
  } catch (err) {
    console.error('Failed to load gallery data:', err);
    showToast('Could not load gallery data. Make sure gallery/ JSON files are present.', 'error', 6000);
    // Still set up the app with empty data
    setupEventListeners();
    renderEmptyState('Failed to load gallery data. Run `profileforge gallery export --out-dir gallery` first.');
  } finally {
    setLoading(false);
  }
}

// ============================================================
// RENDER: THEME GRID
// ============================================================
function renderThemeGrid() {
  const grid = $('theme-grid');
  grid.innerHTML = '';

  state.themes.forEach(theme => {
    const card = document.createElement('div');
    card.className = `theme-card ${theme.id === state.theme ? 'selected' : ''}`;
    card.dataset.themeId = theme.id;
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', `Select ${theme.name} theme`);

    const swatches = THEME_SWATCHES[theme.id] || ['#58A6FF', '#D2A8FF', '#2EA043'];
    const swatchGradient = `linear-gradient(90deg, ${swatches.join(', ')})`;

    card.innerHTML = `
      <div class="theme-card-name">${theme.id}</div>
      <div class="theme-card-mode">${theme.mode}</div>
      <div class="theme-swatch" style="background:${swatchGradient}"></div>
    `;

    card.addEventListener('click', () => selectTheme(theme.id));
    card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') selectTheme(theme.id); });

    grid.appendChild(card);
  });
}

function selectTheme(themeId) {
  state.theme = themeId;
  document.querySelectorAll('.theme-card').forEach(card => {
    card.classList.toggle('selected', card.dataset.themeId === themeId);
  });
  renderPreview();
}

// ============================================================
// RENDER: WIDGET LIST
// ============================================================
function renderWidgetList() {
  const container = $('widget-list');
  container.innerHTML = '';

  // Group by category
  const groups = {};
  state.widgets.forEach(w => {
    if (!groups[w.category]) groups[w.category] = [];
    groups[w.category].push(w);
  });

  Object.entries(groups).forEach(([category, widgets]) => {
    const groupEl = document.createElement('div');
    groupEl.className = 'widget-category-group';

    const labelEl = document.createElement('div');
    labelEl.className = 'widget-category-label';
    labelEl.textContent = category;
    groupEl.appendChild(labelEl);

    widgets.forEach(w => {
      const item = document.createElement('label');
      item.className = `widget-check-item ${state.activeWidgets.has(w.id) ? 'active' : ''}`;
      item.htmlFor = `widget-check-${w.id}`;

      const connector = w.required_connectors?.[0] || 'local';
      item.innerHTML = `
        <input type="checkbox" id="widget-check-${w.id}" data-widget-id="${w.id}"
          ${state.activeWidgets.has(w.id) ? 'checked' : ''}
          aria-label="Enable ${w.name} widget">
        <span class="widget-label">${w.id}</span>
        <span class="widget-connector-badge ${connector}">${connector}</span>
      `;

      const checkbox = item.querySelector('input');
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
          state.activeWidgets.add(w.id);
          item.classList.add('active');
        } else {
          state.activeWidgets.delete(w.id);
          item.classList.remove('active');
        }
        updateWidgetCountBadge();
        renderPreview();
      });

      groupEl.appendChild(item);
    });

    container.appendChild(groupEl);
  });
}

function updateWidgetCountBadge() {
  const badge = $('widget-count-badge');
  badge.textContent = state.activeWidgets.size;
}

// ============================================================
// RENDER: TEMPLATE SELECTOR
// ============================================================
function renderTemplateSelector() {
  const select = $('template-select');
  select.innerHTML = '<option value="">— No Template —</option>';

  state.templates.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t.id;
    opt.textContent = t.name;
    select.appendChild(opt);
  });
}

function applyTemplate(templateId) {
  if (!templateId) return;

  const template = state.templates.find(t => t.id === templateId);
  if (!template) return;

  // Apply widgets
  state.activeWidgets.clear();
  (template.widgets || []).forEach(w => state.activeWidgets.add(w));

  // Apply theme
  if (template.active_theme) {
    state.theme = template.active_theme;
  }

  // Re-render controls to reflect new state
  renderWidgetList();
  renderThemeGrid();
  updateWidgetCountBadge();
  renderPreview();

  // Smooth scroll to canvas
  $('preview-canvas').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============================================================
// RENDER: PREVIEW CANVAS
// ============================================================
function renderPreview() {
  const canvas = $('preview-canvas');
  const usernameDisplay = $('preview-username-display');
  usernameDisplay.textContent = `@${state.username} · ${state.theme}`;

  updateWidgetCountBadge();

  if (state.activeWidgets.size === 0) {
    renderEmptyState('Select a persona template or enable widgets to preview your profile.');
    return;
  }

  canvas.innerHTML = '';

  state.activeWidgets.forEach(widgetId => {
    const card = buildWidgetPreviewCard(widgetId, state.theme);
    canvas.appendChild(card);
  });
}

function buildWidgetPreviewCard(widgetId, themeId) {
  const card = document.createElement('div');
  card.className = 'preview-widget-card';

  const label = document.createElement('div');
  label.className = 'preview-widget-label';
  label.innerHTML = `
    <span class="preview-widget-label-name">${widgetId}</span>
    <span class="preview-widget-label-theme">${themeId}</span>
  `;
  card.appendChild(label);

  const svgContainer = document.createElement('div');
  svgContainer.className = 'preview-widget-svg-container';

  const assetUrl = `./gallery/assets/${widgetId}_${themeId}.svg`;
  const img = document.createElement('img');
  img.alt = `${widgetId} widget in ${themeId} theme`;
  img.loading = 'lazy';
  img.style.maxWidth = '820px';

  img.onerror = () => {
    // Graceful fallback
    svgContainer.innerHTML = `
      <div class="preview-placeholder">
        <div class="preview-placeholder-icon">🧩</div>
        <div>${widgetId}</div>
        <small style="color:var(--text-muted);font-size:11px;margin-top:4px;display:block;">
          SVG preview not found for theme "${themeId}"<br>
          Run: <code style="font-family:monospace">profileforge gallery export</code>
        </small>
      </div>
    `;
  };

  img.src = assetUrl;
  svgContainer.appendChild(img);
  card.appendChild(svgContainer);

  return card;
}

function renderEmptyState(message) {
  $('preview-canvas').innerHTML = `
    <div id="empty-state">
      <div class="empty-icon">🔮</div>
      <p>${message}</p>
    </div>
  `;
}

// ============================================================
// EXPORT: COPY README MARKDOWN
// ============================================================
function copyReadmeMarkdown() {
  if (state.activeWidgets.size === 0) {
    showToast('Enable at least one widget first!', 'error');
    return;
  }

  const baseUrl = 'https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets';
  let md = `<!-- ProfileForge | Generated by ProfileForge Studio -->\n\n`;
  md += `<div align="center">\n\n`;

  state.activeWidgets.forEach(widgetId => {
    const assetUrl = `${baseUrl}/${widgetId}_${state.theme}.svg`;
    md += `<picture>\n  <img src="${assetUrl}" alt="${widgetId}" width="820" />\n</picture>\n\n`;
  });

  md += `</div>\n\n`;
  md += `---\n\n> 🔥 *Built with [ProfileForge](https://github.com/iisgaurav/profileforge)*\n`;

  navigator.clipboard.writeText(md).then(() => {
    showToast('README markdown copied to clipboard!', 'success');
  }).catch(() => {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = md;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    showToast('README markdown copied!', 'success');
  });
}

// ============================================================
// EXPORT: DOWNLOAD PROFILEFORGE.YAML
// ============================================================
function exportProfileforgeYaml() {
  if (state.activeWidgets.size === 0) {
    showToast('Enable at least one widget first!', 'error');
    return;
  }

  const widgetLines = [...state.activeWidgets].map(w => `  - name: ${w}`).join('\n');

  const yaml = `# profileforge.yaml — Generated by ProfileForge Studio
# https://github.com/iisgaurav/profileforge
version: 1

project:
  name: "My GitHub Profile"
  title: "Developer"

themes:
  active: "${state.theme}"

connectors:
  local:
    root: "./config"
  github:
    username: "${state.username}"

widgets:
${widgetLines}

outputs:
  svg:
    enabled: true
    dir: "assets"
`;

  const blob = new Blob([yaml], { type: 'text/yaml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'profileforge.yaml';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  showToast('profileforge.yaml downloaded!', 'success');
}

// ============================================================
// EXPORT: DOWNLOAD SVG BUNDLE
// ============================================================
async function downloadSVGBundle() {
  if (state.activeWidgets.size === 0) {
    showToast('Enable at least one widget first!', 'error');
    return;
  }

  showToast(`Downloading ${state.activeWidgets.size} SVG files...`, 'info', 4000);

  const downloads = [];
  for (const widgetId of state.activeWidgets) {
    try {
      const url = `./gallery/assets/${widgetId}_${state.theme}.svg`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Not found');
      const svg = await res.text();
      const blob = new Blob([svg], { type: 'image/svg+xml' });
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `${widgetId}_${state.theme}.svg`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(blobUrl);
      // Small delay between downloads
      await new Promise(r => setTimeout(r, 150));
    } catch {
      downloads.push(widgetId);
    }
  }

  if (downloads.length > 0) {
    showToast(`${downloads.length} SVG(s) not found (run gallery export first): ${downloads.join(', ')}`, 'error', 5000);
  } else {
    showToast(`All ${state.activeWidgets.size} SVGs downloaded!`, 'success');
  }
}

// ============================================================
// EVENT LISTENERS
// ============================================================
function setupEventListeners() {
  // Username input
  const usernameInput = $('username-input');
  let debounceTimer;
  usernameInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      state.username = usernameInput.value.trim() || 'octocat';
      renderPreview();
    }, 400);
  });

  // Template selector
  const templateSelect = $('template-select');
  templateSelect.addEventListener('change', () => {
    state.template = templateSelect.value;
    applyTemplate(state.template);
  });

  // Export buttons
  $('btn-copy-readme').addEventListener('click', copyReadmeMarkdown);
  $('btn-export-yaml').addEventListener('click', exportProfileforgeYaml);
  $('btn-download-svg').addEventListener('click', downloadSVGBundle);

  // Keyboard shortcut: Cmd/Ctrl+K → focus username
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      usernameInput.focus();
      usernameInput.select();
    }
  });
}

// ============================================================
// BOOT
// ============================================================
document.addEventListener('DOMContentLoaded', init);
