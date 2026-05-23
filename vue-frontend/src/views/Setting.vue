<template>
  <div class="settings-page">
    <div class="settings-container">

      <div class="settings-header">
        <h1>Settings</h1>
        <p class="subtitle">Manage your account and preferences</p>
      </div>

      <div class="settings-body">

        <!-- Sidebar nav -->
        <nav class="settings-nav">
          <button
            v-for="section in sections"
            :key="section.id"
            class="nav-item"
            :class="{ active: activeSection === section.id }"
            @click="activeSection = section.id"
          >
            <component :is="section.icon" class="nav-icon" />
            {{ section.label }}
          </button>
        </nav>

        <!-- Content panels -->
        <div class="settings-content">

          <!-- ══════════════════════════════════════
               APPEARANCE
          ══════════════════════════════════════ -->
          <section v-if="activeSection === 'appearance'" class="panel">
            <div class="panel-header">
              <h2>Appearance</h2>
              <p>Customise how the interface looks and feels</p>
            </div>

            <!-- ── Theme & Contrast ── -->
            <div class="setting-group">
              <div class="group-title">Theme &amp; contrast</div>

              <!-- Theme -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Theme</span>
                  <span class="setting-desc">Reduce glare and eye strain with dark mode</span>
                </div>
                <div class="theme-toggle">
                  <button class="theme-btn" :class="{ active: theme === 'light' }" @click="setTheme('light')">
                    <SunIcon class="btn-icon" /> Light
                  </button>
                  <button class="theme-btn" :class="{ active: theme === 'dark' }" @click="setTheme('dark')">
                    <MoonIcon class="btn-icon" /> Dark
                  </button>
                  <button class="theme-btn" :class="{ active: theme === 'system' }" @click="setTheme('system')">
                    <MonitorIcon class="btn-icon" /> System
                  </button>
                </div>
              </div>

              <!-- High contrast -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">High contrast</span>
                  <span class="setting-desc">Enforces 7:1 contrast ratio — true black background with white or yellow text</span>
                </div>
                <button
                  class="toggle-switch"
                  :class="{ on: highContrast }"
                  role="switch"
                  :aria-checked="highContrast"
                  @click="highContrast = !highContrast"
                >
                  <span class="toggle-thumb" />
                </button>
              </div>

              <!-- Color filter -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Color blindness filter</span>
                  <span class="setting-desc">Adjusts the color palette for different types of color vision deficiency</span>
                </div>
                <div class="segmented">
                  <button
                    v-for="cf in colorFilters"
                    :key="cf.value"
                    class="seg-btn"
                    :class="{ active: colorFilter === cf.value }"
                    @click="colorFilter = cf.value"
                  >
                    {{ cf.label }}
                  </button>
                </div>
              </div>
            </div>

            <!-- ── Typography ── -->
            <div class="setting-group">
              <div class="group-title">Typography</div>

              <!-- Font size slider -->
              <div class="setting-row setting-row--col">
                <div class="setting-info">
                  <span class="setting-label">Font size scale</span>
                  <span class="setting-desc">Scale all text from 100% up to 200% without breaking layout</span>
                </div>
                <div class="slider-row">
                  <span class="slider-label">100%</span>
                  <input
                    type="range"
                    min="100"
                    max="200"
                    step="5"
                    v-model.number="fontScale"
                    class="range-input"
                    aria-label="Font size scale"
                  />
                  <span class="slider-label">200%</span>
                  <span class="slider-value">{{ fontScale }}%</span>
                </div>
              </div>

              <!-- Font family -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Font family</span>
                  <span class="setting-desc">Atkinson Hyperlegible has distinct character shapes that resist blurring</span>
                </div>
                <div class="segmented">
                  <button
                    v-for="ff in fontFamilies"
                    :key="ff.value"
                    class="seg-btn"
                    :class="{ active: fontFamily === ff.value }"
                    @click="fontFamily = ff.value"
                  >
                    {{ ff.label }}
                  </button>
                </div>
              </div>

              <!-- Line spacing -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Line spacing</span>
                  <span class="setting-desc">Extra leading prevents letters from merging during blurred vision episodes</span>
                </div>
                <div class="segmented">
                  <button
                    v-for="ls in lineSpacings"
                    :key="ls.value"
                    class="seg-btn"
                    :class="{ active: lineSpacing === ls.value }"
                    @click="lineSpacing = ls.value"
                  >
                    {{ ls.label }}
                  </button>
                </div>
              </div>

              <!-- Letter spacing -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Letter spacing</span>
                  <span class="setting-desc">Wider tracking gives each character more visual separation</span>
                </div>
                <div class="segmented">
                  <button
                    v-for="ls in letterSpacings"
                    :key="ls.value"
                    class="seg-btn"
                    :class="{ active: letterSpacing === ls.value }"
                    @click="letterSpacing = ls.value"
                  >
                    {{ ls.label }}
                  </button>
                </div>
              </div>
            </div>

            <!-- ── Interface Layout ── -->
            <div class="setting-group">
              <div class="group-title">Interface layout</div>

              <!-- Touch target size -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Touch target size</span>
                  <span class="setting-desc">Large targets (48×48 dp minimum) help users relying on peripheral vision</span>
                </div>
                <div class="segmented">
                  <button
                    v-for="ts in targetSizes"
                    :key="ts.value"
                    class="seg-btn"
                    :class="{ active: targetSize === ts.value }"
                    @click="targetSize = ts.value"
                  >
                    {{ ts.label }}
                  </button>
                </div>
              </div>

              <!-- Layout density -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Layout density</span>
                  <span class="setting-desc">Single-column view aids screen readers and central vision loss navigation</span>
                </div>
                <div class="segmented">
                  <button class="seg-btn" :class="{ active: layoutDensity === 'default' }" @click="layoutDensity = 'default'">Default</button>
                  <button class="seg-btn" :class="{ active: layoutDensity === 'simplified' }" @click="layoutDensity = 'simplified'">Simplified</button>
                </div>
              </div>

              <!-- Magnification lens -->
              <div class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">Magnification lens</span>
                  <span class="setting-desc">Hover or tap a card to magnify it without zooming the whole screen</span>
                </div>
                <button
                  class="toggle-switch"
                  :class="{ on: magLens }"
                  role="switch"
                  :aria-checked="magLens"
                  @click="magLens = !magLens"
                >
                  <span class="toggle-thumb" />
                </button>
              </div>
            </div>

            <!-- Preview chip -->
            <div class="preview-strip">
              <span class="preview-label">Preview</span>
              <p class="preview-text">
                The quick brown fox jumps over the lazy dog. Blood glucose: 7.4 mmol/L
              </p>
            </div>

          </section>

          <!-- ══════════════════════════════════════
               PROFILE
          ══════════════════════════════════════ -->
          <section v-if="activeSection === 'profile'" class="panel">
            <div class="panel-header">
              <h2>Profile</h2>
              <p>Update your personal information</p>
            </div>
            <div class="setting-group">
              <div class="field-row">
                <label class="field-label">Display name</label>
                <input type="text" class="field-input" placeholder="Your name" v-model="profile.name" />
              </div>
              <div class="field-row">
                <label class="field-label">Email</label>
                <input type="email" class="field-input" placeholder="you@example.com" v-model="profile.email" />
              </div>
              <div class="field-row">
                <label class="field-label">Bio</label>
                <textarea class="field-input field-textarea" placeholder="A short bio…" v-model="profile.bio" rows="3" />
              </div>
              <div class="panel-actions">
                <button class="btn-primary">Save changes</button>
              </div>
            </div>
          </section>

          <!-- ══════════════════════════════════════
               NOTIFICATIONS
          ══════════════════════════════════════ -->
          <section v-if="activeSection === 'notifications'" class="panel">
            <div class="panel-header">
              <h2>Notifications</h2>
              <p>Choose what you want to be notified about</p>
            </div>
            <div class="setting-group">
              <div v-for="notif in notifications" :key="notif.id" class="setting-row">
                <div class="setting-info">
                  <span class="setting-label">{{ notif.label }}</span>
                  <span class="setting-desc">{{ notif.desc }}</span>
                </div>
                <button
                  class="toggle-switch"
                  :class="{ on: notif.enabled }"
                  role="switch"
                  :aria-checked="notif.enabled"
                  @click="notif.enabled = !notif.enabled"
                >
                  <span class="toggle-thumb" />
                </button>
              </div>
            </div>
          </section>

          <!-- ══════════════════════════════════════
               SECURITY
          ══════════════════════════════════════ -->
          <section v-if="activeSection === 'security'" class="panel">
            <div class="panel-header">
              <h2>Security</h2>
              <p>Keep your account safe</p>
            </div>
            <div class="setting-group">
              <div class="field-row">
                <label class="field-label">Current password</label>
                <input type="password" class="field-input" placeholder="••••••••" />
              </div>
              <div class="field-row">
                <label class="field-label">New password</label>
                <input type="password" class="field-input" placeholder="••••••••" />
              </div>
              <div class="field-row">
                <label class="field-label">Confirm password</label>
                <input type="password" class="field-input" placeholder="••••••••" />
              </div>
              <div class="panel-actions">
                <button class="btn-primary">Update password</button>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

/* ── Inline icon components ── */
const PaletteIcon  = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>` }
const UserIcon     = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>` }
const BellIcon     = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>` }
const LockIcon     = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>` }
const SunIcon      = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>` }
const MoonIcon     = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/></svg>` }
const MonitorIcon  = { template: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/></svg>` }

/* ── Nav sections ── */
const sections = [
  { id: 'appearance',    label: 'Appearance',    icon: PaletteIcon },
  { id: 'profile',       label: 'Profile',       icon: UserIcon },
  { id: 'notifications', label: 'Notifications', icon: BellIcon },
  { id: 'security',      label: 'Security',      icon: LockIcon },
]
const activeSection = ref('appearance')

/* ══════════════════════════════════════
   APPEARANCE STATE
══════════════════════════════════════ */

/* Theme */
const theme = ref('light')
const setTheme = (val) => { theme.value = val }

watch(theme, (val) => {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const resolved = val === 'system' ? (prefersDark ? 'dark' : 'light') : val
  document.documentElement.setAttribute('data-theme', resolved)
}, { immediate: true })

/* High contrast */
const highContrast = ref(false)
watch(highContrast, (val) => {
  document.documentElement.setAttribute('data-high-contrast', val ? 'true' : 'false')
})

/* Color blindness filter */
const colorFilters = [
  { label: 'None',    value: 'none'    },
  { label: 'Protan',  value: 'protan'  },
  { label: 'Deutan',  value: 'deutan'  },
  { label: 'Tritan',  value: 'tritan'  },
]
const colorFilter = ref('none')

const filterMatrix = {
  none:   'none',
  protan: 'url(#protan)',
  deutan: 'url(#deutan)',
  tritan: 'url(#tritan)',
}
watch(colorFilter, (val) => {
  document.documentElement.style.filter = filterMatrix[val] ?? 'none'
})

/* Font scale (100–200%) */
const fontScale = ref(100)
watch(fontScale, (val) => {
  document.documentElement.style.fontSize = `${val}%`
})

/* Font family */
const fontFamilies = [
  { label: 'Standard',      value: 'standard'      },
  { label: 'Hyperlegible',  value: 'hyperlegible'  },
  { label: 'OpenDyslexic',  value: 'opendyslexic'  },
]
const fontFamily = ref('standard')

const fontFamilyMap = {
  standard:     `'DM Sans', system-ui, sans-serif`,
  hyperlegible: `'Atkinson Hyperlegible', sans-serif`,
  opendyslexic: `'OpenDyslexic', sans-serif`,
}
watch(fontFamily, (val) => {
  document.documentElement.style.setProperty('--app-font', fontFamilyMap[val])
})

/* Line spacing */
const lineSpacings = [
  { label: 'Standard',   value: 'standard'   },
  { label: 'Loose',      value: 'loose'      },
  { label: 'Extra Loose',value: 'extraloose' },
]
const lineSpacing = ref('standard')

const lineHeightMap = { standard: '1.5', loose: '1.9', extraloose: '2.3' }
watch(lineSpacing, (val) => {
  document.documentElement.style.setProperty('--app-line-height', lineHeightMap[val])
})

/* Letter spacing */
const letterSpacings = [
  { label: 'Normal',  value: 'normal'  },
  { label: 'Wide',    value: 'wide'    },
  { label: 'Wider',   value: 'wider'   },
]
const letterSpacing = ref('normal')

const trackingMap = { normal: '0em', wide: '0.04em', wider: '0.1em' }
watch(letterSpacing, (val) => {
  document.documentElement.style.setProperty('--app-letter-spacing', trackingMap[val])
})

/* Touch target size */
const targetSizes = [
  { label: 'Normal', value: 'normal' },
  { label: 'Large',  value: 'large'  },
]
const targetSize = ref('normal')
watch(targetSize, (val) => {
  document.documentElement.setAttribute('data-target-size', val)
})

/* Layout density */
const layoutDensity = ref('default')
watch(layoutDensity, (val) => {
  document.documentElement.setAttribute('data-layout', val)
})

/* Magnification lens */
const magLens = ref(false)

/* ══════════════════════════════════════
   OTHER PANELS STATE
══════════════════════════════════════ */
const profile = ref({ name: '', email: '', bio: '' })

const notifications = ref([
  { id: 'email',   label: 'Email alerts',       desc: 'Receive updates via email',          enabled: true  },
  { id: 'push',    label: 'Push notifications', desc: 'In-app alerts for activity',         enabled: true  },
  { id: 'weekly',  label: 'Weekly digest',      desc: 'A summary of activity each week',    enabled: false },
  { id: 'product', label: 'Product news',       desc: 'New features and announcements',     enabled: false },
])
</script>

<style scoped>
/* ══ SVG filter defs for CVD simulation ══
   Injected as a hidden element; filter IDs referenced via url(#...) */
.cvd-filters { position: absolute; width: 0; height: 0; overflow: hidden; }

.settings-page {
  min-height: 100vh;
  background-color: var(--background);
  color: var(--foreground);
  font-family: var(--app-font, 'DM Sans', system-ui, sans-serif);
  font-size: inherit;
  line-height: var(--app-line-height, 1.5);
  letter-spacing: var(--app-letter-spacing, 0em);
  padding: 2.5rem 1.5rem;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.settings-container { max-width: 900px; margin: 0 auto; }

/* ── Header ── */
.settings-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}
.settings-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--foreground);
  margin: 0 0 0.25rem;
}
.subtitle { font-size: 0.875rem; color: var(--muted-foreground); margin: 0; }

/* ── Body layout ── */
.settings-body { display: flex; gap: 2rem; align-items: flex-start; }

/* ── Sidebar ── */
.settings-nav { display: flex; flex-direction: column; gap: 2px; min-width: 180px; flex-shrink: 0; }

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border: none;
  background: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--muted-foreground);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s, color 0.15s;
  width: 100%;
  min-height: 40px;
}
.nav-item:hover { background: var(--muted); color: var(--foreground); }
.nav-item.active {
  background: color-mix(in srgb, var(--primary) 10%, transparent);
  color: var(--primary);
}
.nav-icon { width: 16px; height: 16px; flex-shrink: 0; }

/* ── Panel shell ── */
.settings-content { flex: 1; min-width: 0; }

.panel {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}
.panel-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
}
.panel-header h2 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.2rem;
  color: var(--foreground);
}
.panel-header p { font-size: 0.8125rem; color: var(--muted-foreground); margin: 0; }

/* ── Group title ── */
.setting-group { padding: 0.25rem 0; }

.group-title {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted-foreground);
  padding: 0.875rem 1.5rem 0.25rem;
}

.setting-group + .setting-group {
  border-top: 1px solid var(--border);
}

/* ── Setting rows ── */
.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}
.setting-row + .setting-row { border-top: 1px solid var(--border); }

.setting-row--col { flex-direction: column; align-items: flex-start; gap: 0.75rem; }

.setting-info { display: flex; flex-direction: column; gap: 3px; flex: 1; min-width: 0; }
.setting-label { font-size: 0.875rem; font-weight: 500; color: var(--foreground); }
.setting-desc  { font-size: 0.8rem; color: var(--muted-foreground); line-height: 1.45; }

/* ── Theme toggle ── */
.theme-toggle {
  display: flex;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}
.theme-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  font-size: 0.8125rem;
  font-weight: 500;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--muted-foreground);
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
}
.theme-btn.active { background: var(--primary); color: var(--primary-foreground); }
.theme-btn:not(.active):hover { background: var(--muted); color: var(--foreground); }
.btn-icon { width: 14px; height: 14px; }

/* ── Segmented control ── */
.segmented {
  display: flex;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  flex-wrap: wrap;
}
.seg-btn {
  padding: 7px 14px;
  font-size: 0.8125rem;
  font-weight: 500;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--muted-foreground);
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
}
.seg-btn + .seg-btn { border-left: 1px solid var(--border); }
.seg-btn.active { background: var(--primary); color: var(--primary-foreground); }
.seg-btn:not(.active):hover { background: var(--muted); color: var(--foreground); }

/* ── Range slider ── */
.slider-row {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}
.range-input { flex: 1; cursor: pointer; accent-color: var(--primary); }
.slider-label { font-size: 0.8rem; color: var(--muted-foreground); white-space: nowrap; }
.slider-value {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--primary);
  min-width: 42px;
  text-align: right;
}

/* ── Toggle switch ── */
.toggle-switch {
  width: 44px;
  height: 26px;
  border-radius: 999px;
  background: var(--border);
  border: none;
  cursor: pointer;
  padding: 3px;
  flex-shrink: 0;
  transition: background 0.2s ease;
}
.toggle-switch.on { background: var(--primary); }
.toggle-thumb {
  display: block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  transition: transform 0.2s ease;
}
.toggle-switch.on .toggle-thumb { transform: translateX(18px); }

/* ── Preview strip ── */
.preview-strip {
  margin: 0;
  padding: 1rem 1.5rem;
  background: var(--muted);
  border-top: 1px solid var(--border);
}
.preview-label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted-foreground);
  display: block;
  margin-bottom: 6px;
}
.preview-text {
  margin: 0;
  font-size: 1rem;
  color: var(--foreground);
  font-family: var(--app-font, inherit);
  line-height: var(--app-line-height, 1.5);
  letter-spacing: var(--app-letter-spacing, 0em);
}

/* ── Form fields ── */
.field-row { display: flex; flex-direction: column; gap: 6px; padding: 1rem 1.5rem; }
.field-row + .field-row { border-top: 1px solid var(--border); }
.field-label { font-size: 0.8125rem; font-weight: 500; color: var(--foreground); }
.field-input {
  width: 100%;
  padding: 9px 12px;
  font-size: 0.875rem;
  color: var(--foreground);
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 8px;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  font-family: inherit;
}
.field-input:focus { border-color: var(--primary); }
.field-textarea { resize: vertical; min-height: 80px; }

/* ── Actions ── */
.panel-actions { padding: 1rem 1.5rem; border-top: 1px solid var(--border); }
.btn-primary {
  background: var(--primary);
  color: var(--primary-foreground);
  border: none;
  border-radius: 8px;
  padding: 9px 20px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.15s;
  font-family: inherit;
}
.btn-primary:hover { opacity: 0.88; }

/* ── Responsive ── */
@media (max-width: 640px) {
  .settings-body { flex-direction: column; }
  .settings-nav { flex-direction: row; flex-wrap: wrap; min-width: unset; width: 100%; }
  .nav-item { flex: 1; justify-content: center; min-width: 72px; }
  .theme-toggle, .segmented { flex-wrap: wrap; }
}
</style>

<template>
  <svg class="cvd-filters" aria-hidden="true" focusable="false">
    <defs>
      <filter id="protan">
        <feColorMatrix type="matrix" values="
          0.567 0.433 0     0 0
          0.558 0.442 0     0 0
          0     0.242 0.758 0 0
          0     0     0     1 0"/>
      </filter>
      <filter id="deutan">
        <feColorMatrix type="matrix" values="
          0.625 0.375 0     0 0
          0.7   0.3   0     0 0
          0     0.3   0.7   0 0
          0     0     0     1 0"/>
      </filter>
      <filter id="tritan">
        <feColorMatrix type="matrix" values="
          0.95  0.05  0     0 0
          0     0.433 0.567 0 0
          0     0.475 0.525 0 0
          0     0     0     1 0"/>
      </filter>
    </defs>
  </svg>
</template>
