/**
 * ProfileForge Studio — app.js
 * Zero-dependency vanilla JS application
 */

'use strict';

// ============================================================
// STATE
// ============================================================
const state = {
  username: 'iisgaurav',
  template: null,
  activeWidgets: [],
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
// URL STATE SYNC
// ============================================================
function updateUrlState() {
  const params = new URLSearchParams();
  if (state.username !== 'iisgaurav') params.set('username', state.username);
  if (state.theme !== 'github-dark') params.set('theme', state.theme);
  if (state.activeWidgets.length > 0) params.set('widgets', state.activeWidgets.join(','));
  
  const hash = params.toString();
  window.history.replaceState(null, '', hash ? `#${hash}` : window.location.pathname);
}

function loadUrlState() {
  if (!window.location.hash) return false;
  
  const params = new URLSearchParams(window.location.hash.slice(1));
  let changed = false;
  
  if (params.has('username')) {
    state.username = params.get('username');
    $('username-input').value = state.username;
    changed = true;
  }
  
  if (params.has('theme')) {
    state.theme = params.get('theme');
    changed = true;
  }
  
  if (params.has('widgets')) {
    state.activeWidgets = params.get('widgets').split(',').filter(Boolean);
    changed = true;
  }
  
  return changed;
}

// ============================================================
// INITIALIZATION
// ============================================================
async function init() {
  setLoading(true);
  try {
    const [themes, widgets, templates] = await Promise.all([
      fetchJSON('../gallery/themes.json'),
      fetchJSON('../gallery/widgets.json'),
      fetchJSON('../gallery/templates.json'),
    ]);

    state.themes = themes;
    state.widgets = widgets;
    state.templates = templates;

    // If URL has state, load it. Otherwise, load default template.
    if (!loadUrlState()) {
      if (state.templates && state.templates.length > 0) {
        applyTemplate(state.templates[0].id);
      }
    }

    renderThemeGrid();
    renderWidgetList();
    renderTemplateSelector();
    setupEventListeners();
    setupDragAndDrop();
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
  updateUrlState();
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
      item.className = `widget-check-item ${state.activeWidgets.includes(w.id) ? 'active' : ''}`;
      item.htmlFor = `widget-check-${w.id}`;

      const connector = w.required_connectors?.[0] || 'local';
      item.innerHTML = `
        <input type="checkbox" id="widget-check-${w.id}" data-widget-id="${w.id}"
          ${state.activeWidgets.includes(w.id) ? 'checked' : ''}
          aria-label="Enable ${w.name} widget">
        <span class="widget-label">${w.id}</span>
        <span class="widget-connector-badge ${connector}">${connector}</span>
      `;

      const checkbox = item.querySelector('input');
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
          if (!state.activeWidgets.includes(w.id)) state.activeWidgets.push(w.id);
          item.classList.add('active');
        } else {
          state.activeWidgets = state.activeWidgets.filter(id => id !== w.id);
          item.classList.remove('active');
        }
        updateWidgetCountBadge();
        renderPreview();
        updateUrlState();
      });

      groupEl.appendChild(item);
    });

    container.appendChild(groupEl);
  });
}

function updateWidgetCountBadge() {
  const badge = $('widget-count-badge');
  badge.textContent = state.activeWidgets.length;
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
  state.activeWidgets = [];
  (template.widgets || []).forEach(w => state.activeWidgets.push(w));

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

  if (state.activeWidgets.length === 0) {
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
  card.draggable = true;
  card.dataset.widgetId = widgetId;

  // Drag and Drop Events
  card.addEventListener('dragstart', handleDragStart);
  card.addEventListener('dragend', handleDragEnd);

  const label = document.createElement('div');
  label.className = 'preview-widget-label';
  label.innerHTML = `
    <span class="preview-widget-label-name">${widgetId}</span>
    <span class="preview-widget-label-theme">${themeId}</span>
  `;
  card.appendChild(label);

  const svgContainer = document.createElement('div');
  svgContainer.className = 'preview-widget-svg-container';

  // Add cache-buster to ensure we see newly generated SVGs instead of stale cached ones
  const assetUrl = `../gallery/assets/${widgetId}_${themeId}.svg?v=${Date.now()}`;
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

// ============================================================
// DRAG AND DROP HANDLERS
// ============================================================
function handleDragStart(e) {
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', this.dataset.widgetId);
  setTimeout(() => this.classList.add('dragging'), 0);
}

function handleDragEnd(e) {
  this.classList.remove('dragging');
  // Re-sync state.activeWidgets based on new DOM order
  const newOrder = [];
  document.querySelectorAll('.preview-widget-card').forEach(card => {
    newOrder.push(card.dataset.widgetId);
  });
  
  // Update state and UI
  state.activeWidgets = newOrder;
  renderWidgetList(); // Re-render sidebar to match new order
  updateUrlState(); // Save to URL
}

function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.preview-widget-card:not(.dragging)')];
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function setupDragAndDrop() {
  const container = $('preview-canvas');
  
  container.addEventListener('dragover', e => {
    e.preventDefault();
    const afterElement = getDragAfterElement(container, e.clientY);
    const draggable = document.querySelector('.dragging');
    if (!draggable) return;
    
    if (afterElement == null) {
      container.appendChild(draggable);
    } else {
      container.insertBefore(draggable, afterElement);
    }
  });
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
  if (state.activeWidgets.length === 0) {
    showToast('Enable at least one widget first!', 'error');
    return;
  }

  const baseUrl = 'https://iisgaurav.github.io/profileforge/gallery/assets';
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
  if (state.activeWidgets.length === 0) {
    showToast('Enable at least one widget first!', 'error');
    return;
  }

  const widgetLines = state.activeWidgets.map(w => `  - name: ${w}`).join('\n');

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
  if (state.activeWidgets.length === 0) {
    showToast('Enable at least one widget first!', 'error');
    return;
  }

  showToast(`Downloading ${state.activeWidgets.length} SVG files...`, 'info', 4000);

  const downloads = [];
  for (const widgetId of state.activeWidgets) {
    try {
      const url = `../gallery/assets/${widgetId}_${state.theme}.svg`;
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
    showToast(`All ${state.activeWidgets.length} SVGs downloaded!`, 'success');
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
      state.username = usernameInput.value.trim() || 'iisgaurav';
      renderPreview();
      updateUrlState();
    }, 400);
  });

  // Template selector
  const templateSelect = $('template-select');
  templateSelect.addEventListener('change', () => {
    state.template = templateSelect.value;
    applyTemplate(state.template);
    updateUrlState();
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
// IMPORT: YAML
// ============================================================
function handleYamlImport(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(evt) {
    try {
      const doc = jsyaml.load(evt.target.result);
      if (!doc || !doc.widgets) {
        showToast('Invalid YAML: missing widgets list', 'error');
        return;
      }

      if (doc.profile && doc.profile.username) {
        state.username = doc.profile.username;
        $('username-input').value = state.username;
      }
      
      if (doc.themes && doc.themes.active) {
        state.theme = doc.themes.active;
      } else if (doc.profile && doc.profile.theme) {
        state.theme = doc.profile.theme;
      }

      state.activeWidgets = [];
      doc.widgets.forEach(w => {
        const name = typeof w === 'string' ? w : w.name;
        if (name) state.activeWidgets.push(name);
      });

      renderThemeGrid();
      renderWidgetList();
      renderPreview();
      updateUrlState();
      
      showToast('Profile configuration imported successfully!', 'success');
    } catch (err) {
      console.error(err);
      showToast('Error parsing YAML file', 'error');
    }
  };
  reader.readAsText(file);
  e.target.value = ''; // Reset input
}

// ============================================================
// BOOT
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  $('import-yaml-input').addEventListener('change', handleYamlImport);
  init();
});
