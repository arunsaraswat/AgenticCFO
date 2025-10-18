# UX Design Guidelines - Agentic CFO Platform

**Reference Dashboards:** Performance Dashboard, Executive Dashboard (FX Sales Analytics), Patient Costing Overview

This document codifies the design principles, patterns, and aesthetics observed in professional financial and analytics dashboards to ensure consistent, high-quality UI/UX across the Agentic CFO platform.

---

## Design Philosophy

**Core Principles:**
1. **Data-First:** Information hierarchy prioritizes key metrics and insights
2. **Clean & Professional:** Minimalist design with purposeful use of color
3. **Scannable:** Users should grasp key information in < 5 seconds
4. **Contextual:** Related data grouped logically, progressive disclosure of details
5. **Actionable:** Clear CTAs, filtering, and drill-down capabilities

---

## Visual Design System

### Color Palette

**Primary Blues (Data Visualization)**
- Deep Blue: `#1F4E78` - Primary brand, headers, high values
- Medium Blue: `#4472C4` - Standard data bars, primary actions
- Light Blue: `#8AB4F8` - Secondary elements, low values
- Sky Blue: `#B4D4FF` - Backgrounds, hover states

**Accent Colors (Semantic)**
- Red: `#C00000` - Warnings, negative values, over-limit
- Orange/Coral: `#FF7043` - Alerts, medium priority
- Green: `#375623` - Success, positive trends, recommendations
- Grey: `#44546A` - Neutral information, secondary text

**Neutrals**
- Dark Grey: `#2C2C2C` - Primary text
- Medium Grey: `#6B6B6B` - Secondary text
- Light Grey: `#E0E0E0` - Borders, dividers
- Off-White: `#F5F5F5` - Backgrounds, panels
- White: `#FFFFFF` - Cards, content areas

**Usage Rules:**
- Use blue gradient for sequential data (low → high)
- Reserve red for warnings and critical thresholds
- Limit accent colors to < 3 per view
- Maintain 4.5:1 contrast ratio for accessibility (WCAG AA)

### Typography

**Font Stack:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
             'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
```

**Type Scale:**
- **Hero Numbers:** 48px, bold, for KPIs (e.g., "50.8%", "$3,769.0")
- **Page Title:** 24px, regular, for dashboard names
- **Section Headers:** 16px, semi-bold, for chart titles
- **Body Text:** 14px, regular, for labels and descriptions
- **Small Text:** 12px, regular, for metadata and footnotes
- **Micro Text:** 10px, regular, for chart annotations

**Number Formatting:**
- Currency: `$1,234.56` (always 2 decimals)
- Percentages: `12.3%` (1 decimal unless < 1%)
- Large numbers: `1.2M`, `345K`, `2.5B` (use abbreviations > 10,000)
- Trend indicators: `↑ 2.1%` or `+$125K` (with direction)

### Spacing & Layout

**Grid System:**
- 12-column responsive grid
- Gutter: 16px (mobile), 24px (tablet), 32px (desktop)
- Container max-width: 1440px
- Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)

**Spacing Scale (Tailwind-compatible):**
- xs: 4px - Tight spacing within components
- sm: 8px - Component padding
- md: 16px - Card padding, between elements
- lg: 24px - Section spacing
- xl: 32px - Major section breaks
- 2xl: 48px - Page-level spacing

**Card Pattern:**
```
┌─────────────────────────┐
│ [Title]          [Icon] │ ← 16px padding
│                         │
│ [Content Area]          │ ← 24px vertical spacing
│                         │
│ [Footer / Actions]      │
└─────────────────────────┘
```

- Border radius: 8px (cards), 4px (buttons)
- Shadow: `0 2px 8px rgba(0,0,0,0.08)` (subtle elevation)
- Border: `1px solid #E0E0E0` (optional, for definition)

---

## Component Patterns

### KPI Cards (Hero Metrics)

**Structure:**
```
┌──────────────────────┐
│ Label (12px grey)    │
│ VALUE (48px bold)    │
│ Δ +2.3% ↑ (14px)    │ ← Trend vs. prior period
└──────────────────────┘
```

**Example:**
- Current Exposure: `3,769.0`
- % Utilization: `50.8%`
- Return on Assets: `1.80%`

**Design Rules:**
- 4-6 KPIs maximum per dashboard
- Left-to-right hierarchy (most → least important)
- Use semantic colors for trends (green +, red -)
- Include comparison period label (e.g., "vs Prior MTD")

### Bar Charts (Horizontal)

**Use Cases:**
- Categorical comparisons (exposure by market, revenue by client)
- Rankings (top 10 customers, regions)

**Design Specs:**
- Bar height: 24-32px
- Spacing between bars: 8px
- Value labels: Inside bar (if fits) or right-aligned outside
- Axis labels: 12px grey
- Grid lines: Light grey, dashed, minimal

**Color Strategy:**
- Single category: Blue gradient (light → dark by value)
- Multiple categories: Categorical palette (max 6 colors)
- Highlight: Use full saturation for selection, 40% opacity for others

### Treemap (Region/Industry Exposure)

**Design Specs:**
- Minimum tile size: 40x40px (readability threshold)
- Label hierarchy: Category > Value > Percentage
- Color intensity: Maps to utilization % (light = low, dark = high)
- Border: 2px white separator between tiles
- Hover: 8px elevation shadow, tooltip with full details

**Label Format:**
```
[Category Name]
$XXX.X
```

### Line Charts (Time Series)

**Use Cases:**
- Trends over time (monthly revenue, daily cash balance)
- Comparison of multiple series (actual vs forecast)

**Design Specs:**
- Line weight: 2px (primary), 1px (secondary)
- Point markers: 4px radius, show on hover only
- Grid lines: Horizontal only, light grey
- X-axis: Rotate labels 45° if crowded
- Y-axis: Start at 0 (unless all values > 1000)
- Tooltip: Show date + value on hover

**Multi-Series:**
- Max 4 lines per chart (readability)
- Use distinct colors + line styles (solid, dashed)
- Legend: Top-right, horizontal layout

### Tables (Detailed Data)

**Design Specs:**
- Header: 14px semi-bold, grey background (#F5F5F5)
- Row height: 40px (comfortable scanning)
- Zebra striping: Alternate rows (#FAFAFA)
- Borders: Bottom only (1px #E0E0E0)
- Alignment: Numbers right, text left, dates center
- Pagination: Bottom center, show "X-Y of Z items"

**Interactive Features:**
- Sortable columns: Caret icon in header
- Row hover: Light blue background
- Selected row: Blue border-left (4px)
- Inline actions: Icon buttons, right-aligned

### Filters & Controls

**Filter Bar:**
```
[PD ⌄] [Credit Manager ⌄] [Customer Name ⌄]  [Values] [Clear]
```

**Design Specs:**
- Height: 40px
- Border: 1px grey
- Icon: Chevron-down for dropdowns, magnifying glass for search
- Spacing: 8px between filters
- Clear button: Ghost style, right-aligned

**Dropdown Menu:**
- Max height: 320px (scroll if more)
- Item height: 36px
- Selected: Blue background
- Checkbox: For multi-select

### Navigation & Layout

**Top Bar:**
- Height: 56px
- Logo: Left, 120px max width
- Navigation: Center (Analysis, Story tabs)
- Actions: Right (Selections, Insights, user menu)
- Divider: 1px bottom border

**Sidebar (if used):**
- Width: 240px (collapsed: 64px)
- Background: Dark grey (#2C2C2C)
- Text: White
- Active item: Blue left border (4px)
- Icons: 20x20px, left-aligned

**Dashboard Grid:**
- 2-column layout for main content
- 1/3 - 2/3 split for detail + summary
- Full-width for charts requiring horizontal space
- Sticky headers on scroll

---

## Interaction Patterns

### States

**Hover:**
- Elevation: Add 2px shadow
- Background: Lighten 5%
- Cursor: Pointer for clickable

**Active/Selected:**
- Border: 2px blue
- Background: Light blue (#F0F7FF)
- Icon: Blue fill

**Disabled:**
- Opacity: 40%
- Cursor: not-allowed
- Grey out text/icons

**Loading:**
- Skeleton screens (grey pulse animation)
- Spinners: Only for < 2 second loads
- Progress bars: For long operations (> 5 sec)

### Transitions

**Animation Durations:**
- Micro: 100ms (hover, ripple)
- Standard: 200ms (expand/collapse, modal)
- Complex: 300ms (page transitions, charts)

**Easing:**
- Default: `cubic-bezier(0.4, 0.0, 0.2, 1)` (Material Design)
- Enter: `cubic-bezier(0.0, 0.0, 0.2, 1)`
- Exit: `cubic-bezier(0.4, 0.0, 1, 1)`

**No Animation:**
- Chart data updates (instant snap)
- Number changes (CountUp.js for big deltas)

### Tooltips

**Trigger:** Hover (desktop), tap (mobile)
**Position:** Above element (flip to below if clipped)
**Delay:** 200ms show, 0ms hide
**Content:**
```
[Label]
Value: $X,XXX.XX
Trend: +X.X% vs prior
```
**Style:** Dark background (#2C2C2C), white text, 8px padding, 4px border-radius

---

## Responsive Design

### Mobile (< 768px)

**Layout:**
- Single column
- KPI cards: Stack vertically
- Charts: Full width, reduce height 30%
- Tables: Horizontal scroll OR card layout
- Filters: Collapse into drawer

**Touch Targets:**
- Minimum: 44x44px (iOS guideline)
- Spacing: 8px between tappable elements

### Tablet (768px - 1024px)

**Layout:**
- 2-column grid for KPIs
- Charts: 2 per row (if small), 1 per row (if complex)
- Sidebar: Collapsible hamburger menu

### Desktop (> 1024px)

**Layout:**
- 3-4 column grid for KPIs
- Dashboard grid: 2-3 charts per row
- Sidebar: Persistent (if used)
- Filters: Persistent horizontal bar

---

## Accessibility (WCAG 2.1 AA)

### Color & Contrast
- Text contrast: 4.5:1 (normal), 3:1 (large text)
- Don't rely on color alone (use icons + labels)
- Colorblind-safe palettes (avoid red/green only)

### Keyboard Navigation
- Tab order: Logical (left-to-right, top-to-bottom)
- Focus indicators: 2px blue outline
- Skip links: "Skip to main content"
- Escape: Close modals/dropdowns

### Screen Readers
- ARIA labels: For icons, charts
- Role attributes: `role="navigation"`, `role="main"`
- Live regions: For dynamic updates (`aria-live="polite"`)
- Alt text: Descriptive, not redundant

### Motion
- Respect `prefers-reduced-motion`
- Provide static alternatives for animations

---

## Performance Guidelines

### Loading Strategy
- Critical CSS: Inline for above-the-fold
- Lazy load: Charts, images below fold
- Code splitting: Route-based chunks
- Skeleton screens: For async data

### Chart Rendering
- SVG: < 1000 data points
- Canvas: > 1000 data points
- Virtualization: For large tables (react-window)
- Debounce: Filter/search inputs (300ms)

### Bundle Size
- Initial load: < 200KB (gzipped)
- Route chunks: < 100KB each
- Tree shaking: Remove unused code
- Image optimization: WebP, lazy load

---

## Example Implementations

### Dashboard Header
```tsx
<div className="flex items-center justify-between h-14 px-6 border-b border-grey-200 bg-white">
  <h1 className="text-2xl font-normal text-grey-800">Performance Dashboard</h1>
  <div className="flex gap-4">
    <button className="px-4 py-2 text-sm">Selections</button>
    <button className="px-4 py-2 text-sm">Insights</button>
  </div>
</div>
```

### KPI Card
```tsx
<div className="p-6 bg-white rounded-lg shadow-sm border border-grey-200">
  <div className="text-xs text-grey-600 mb-1">% Utilization</div>
  <div className="text-5xl font-bold text-grey-900">50.8%</div>
  <div className="text-sm text-green-600 mt-2">
    <span className="mr-1">↑</span>
    <span>2.3% vs Prior Month</span>
  </div>
</div>
```

### Filter Bar
```tsx
<div className="flex gap-2 p-4 bg-grey-50 border-b border-grey-200">
  <select className="px-3 py-2 border border-grey-300 rounded-md text-sm">
    <option>PD</option>
  </select>
  <input
    type="search"
    placeholder="Customer Name"
    className="px-3 py-2 border border-grey-300 rounded-md text-sm flex-1"
  />
  <button className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700">
    Filter
  </button>
</div>
```

---

## Anti-Patterns (Avoid)

❌ **Chart Junk:** 3D effects, excessive gradients, decorative elements
❌ **Rainbow Charts:** > 6 colors in single visualization
❌ **Tiny Text:** < 10px font size
❌ **Mystery Meat:** Icons without labels or tooltips
❌ **Dense Tables:** < 32px row height, no zebra striping
❌ **Neon Colors:** High saturation primaries (hurt eyes)
❌ **Auto-play:** Carousels, animations
❌ **Modal Overload:** > 2 modals deep
❌ **Busy Backgrounds:** Patterns, textures behind data
❌ **Truncation:** Ellipsis without tooltip

---

## Review Checklist

**Visual Design:**
- [ ] Color palette uses approved blues + semantic accents
- [ ] Typography follows scale (48/24/16/14/12/10px)
- [ ] Spacing uses 8px grid
- [ ] Shadows are subtle (< 8px blur)
- [ ] Border radius consistent (8px cards, 4px buttons)

**Layout:**
- [ ] KPI cards at top, scannable in < 5 sec
- [ ] Related charts grouped logically
- [ ] White space separates sections clearly
- [ ] Responsive breakpoints implemented
- [ ] No horizontal scroll (except tables)

**Components:**
- [ ] Numbers formatted with thousands separators
- [ ] Charts have clear titles and axis labels
- [ ] Filters accessible and clearable
- [ ] Tables sortable and paginated
- [ ] Tooltips provide context on hover

**Interaction:**
- [ ] Hover states for all clickable elements
- [ ] Loading states for async operations
- [ ] Error states with recovery options
- [ ] Animations < 300ms duration
- [ ] Keyboard navigation works

**Accessibility:**
- [ ] Color contrast 4.5:1 minimum
- [ ] Focus indicators visible
- [ ] ARIA labels on interactive elements
- [ ] Works with screen reader
- [ ] Touch targets ≥ 44px (mobile)

**Performance:**
- [ ] Initial load < 3 seconds
- [ ] Charts render < 500ms
- [ ] No layout shift (CLS < 0.1)
- [ ] Images lazy loaded
- [ ] Code split by route

---

## Resources

**Design Tools:**
- Figma: https://figma.com
- Tailwind UI: https://tailwindui.com
- Chart.js: https://chartjs.org
- D3.js: https://d3js.org (complex visualizations)

**Accessibility:**
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Contrast Checker: https://webaim.org/resources/contrastchecker/

**Performance:**
- Lighthouse: Chrome DevTools
- Bundle Analyzer: webpack-bundle-analyzer

**Reference Dashboards:**
- Tableau Public: https://public.tableau.com
- Observable: https://observablehq.com
- Financial dashboards: Bloomberg Terminal, FactSet
