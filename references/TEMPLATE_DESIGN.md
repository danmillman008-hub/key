---
name: Swiss Konkur Planner
colors:
  surface: '#faf9f5'
  surface-dim: '#dadad6'
  surface-bright: '#faf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f0'
  surface-container: '#eeeeea'
  surface-container-high: '#e8e8e4'
  surface-container-highest: '#e2e3df'
  on-surface: '#1a1c1a'
  on-surface-variant: '#46464b'
  inverse-surface: '#2f312e'
  inverse-on-surface: '#f1f1ed'
  outline: '#76777b'
  outline-variant: '#c7c6cb'
  surface-tint: '#5e5e62'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1b1b1f'
  on-primary-container: '#848387'
  inverse-primary: '#c7c6ca'
  secondary: '#bc000a'
  on-secondary: '#ffffff'
  secondary-container: '#e2241f'
  on-secondary-container: '#fffbff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#001551'
  on-tertiary-container: '#537aff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e3e2e6'
  primary-fixed-dim: '#c7c6ca'
  on-primary-fixed: '#1b1b1f'
  on-primary-fixed-variant: '#46464a'
  secondary-fixed: '#ffdad5'
  secondary-fixed-dim: '#ffb4aa'
  on-secondary-fixed: '#410001'
  on-secondary-fixed-variant: '#930005'
  tertiary-fixed: '#dce1ff'
  tertiary-fixed-dim: '#b6c4ff'
  on-tertiary-fixed: '#001551'
  on-tertiary-fixed-variant: '#0039b3'
  background: '#faf9f5'
  on-background: '#1a1c1a'
  surface-variant: '#e2e3df'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 36px
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  title-md:
    fontFamily: IBM Plex Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: IBM Plex Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: IBM Plex Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
  mono-metric:
    fontFamily: JetBrains Mono
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 28px
spacing:
  gutter: 1rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system translates the rigorous functionalism and structured purity of the International Typographic Style (Swiss Style) into a high-performance academic planner for Iranian students preparing for the Konkur exam.

Traditional Iranian study planners rely on hyper-saturated fills, clutter, and cramped photocopied grids. In contrast, this design system treats time and cognitive load with radical clarity. The design system emphasizes objective hierarchy, unyielding grid alignment, asymmetric structural tension, and stark typographic contrast paired with purposeful whitespace.

The visual style is **Minimalist Swiss / Neo-Brutalist Grid**:
- Absolute mathematical order: hairline technical borders, structural grid columns, and tabular compartmentalization.
- Asymmetrical anchor points: oversized index numerals and days of the week set against ultra-clean metric fields.
- Utilitarian precision: removing decorative clutter to let subject codes, test counts, target percentages, and elapsed focus timers take center stage with high-legibility Persian/Arabic typography and crisp Latin numerals.

## Colors

The color palette is rooted in a disciplined monochrome foundation inspired by Swiss editorial print, punctuated by tactical primary-grade accents used exclusively for telemetry, status, and focus differentiation:

- **Primary (`#121316` - Stark Ink)**: Deep charcoal-black for core structural borders, high-contrast display text, and authoritative visual anchors.
- **Secondary (`#FF3B30` - Signal Vermilion)**: High-alert accent reserved for urgent Konkur milestones, incomplete target blocks, deficit alerts, and critical exam deadlines.
- **Tertiary (`#0055FF` - Technical Cobalt)**: Focused intellectual hue for live timers, deep study blocks, active subject sessions, and primary data highlights.
- **Neutral (`#F4F4F0` - Newsprint Chalk)**: Warm tactile base surface preventing glare during multi-hour study intervals, with `#FFFFFF` used strictly for card interiors and `#E5E5DF` for hairline architectural cell grids.
- **Functional Semantics**:
  - Emerald Green (`#00875A`): Reached test targets and finished question sets.
  - Cadmium Yellow (`#FFCC00`): In-progress and scheduled review intervals.

## Typography

The typography pairs mechanical Swiss Latin letterforms with dense, clean Persian/Arabic text layouts:

- **Headlines (`Space Grotesk`)**: Geometric, sharp, and structured. Carries the bold authority of Swiss posters for calendar headers, day titles (e.g., *Shanbeh*, *Yekshanbeh*), and subject classifications.
- **Body (`IBM Plex Sans`)**: Systematic and neutral with exceptional legibility at micro scales. Optimized for RTL reading flow, chapter names, exercise notes, and problem set notations.
- **Metrics & Labels (`JetBrains Mono`)**: Strict tabular monospaced sizing for clock timers (07:30 - 09:00), question counts (Test #), percentages (%), and rank calculations, guaranteeing vertical column alignment without numeric drift.

## Layout & Spacing

The layout is built on a modular 7-row timetable grid reflecting the Iranian academic week (Saturday to Friday), intersected by fluid 12-column sub-divisions:

- **Asymmetric Day Anchor**: A fixed lateral column (right-aligned for Persian RTL layout) anchors each day with vertical typography and daily totals.
- **Modular Study Blocks**: Cells span modular increments (e.g., 2 cols for a 90-minute block, 1 col for a break or quick drill).
- **RTL-First Flow**: Horizontal progressions run right-to-left chronologically from early morning sessions to evening review blocks.
- **Breakpoints**:
  - **Desktop (>=1024px)**: Full horizontal 7-day schedule with synchronized time lanes.
  - **Tablet (768px - 1023px)**: Split-week view (3–4 days visible) with horizontal swipe.
  - **Mobile (<768px)**: Single-day stack featuring top-mounted day pills and stacked subject cards with strict 12px structural gutters.

## Elevation & Depth

True to the Swiss ethos, elevation is achieved through **crisp borders and structural planar contrast** rather than ambient drop shadows:

- **Zero Drop Shadows**: Surfaces avoid soft blurs or skeuomorphic bevels.
- **Hairline Bounding Grids**: All container divisions use sharp `1px solid #121316` or `1px solid #D8D8D2` borders.
- **Tonal Contrast Stacking**:
  - Base canvas: `#F4F4F0`.
  - Active time block: `#FFFFFF` encased in a crisp 1.5px border.
  - Focus state: Solid 2px outline in `#0055FF` or `#121316` with zero blur offset.
- **Offset Accent Layers**: High-priority modals and summary flags utilize a hard 3px offset drop (solid black `#121316`, no blur) for deliberate tactile presence.

## Shapes

The design system embraces a **Sharp (`0`)** shape language:
- All cards, timetable cells, metric badges, progress bars, and input controls use `border-radius: 0px`.
- This unyielding rectilinear geometry reinforces the discipline of the Swiss grid, reminiscent of rigorous printed study agendas and archival ledger books.
- Small sub-tags (e.g., "زیست", "شیمی") retain precise right-angled boxes with 1px black stroke perimeters.

## Components

### 1. Timetable Day Row & Study Block
- **Container**: Rectangular box with `1px solid #121316` outer perimeter, divided into modular horizontal segments.
- **Subject Header**: Persian subject label (e.g., ریاضی ۳) set in `IBM Plex Sans` (SemiBold), anchored at top-right.
- **Sub-Metrics**: Two-column micro-grid at the bottom of the cell displaying question count (`تست: ۴۵`) and duration (`۹۰ min`) in `JetBrains Mono`.
- **Status Indicator**: Solid top-border strip (2px) in `#0055FF` (studying), `#00875A` (completed), or `#FF3B30` (missed).

### 2. Tabular Cards (Subject Summary)
- Pure white (`#FFFFFF`) background with a 1px solid black border.
- Flat header bar in neutral light gray (`#EAEAE4`) with an uppercase mono category label.
- Data values set in `mono-metric` typography, vertically aligned with tight internal padding (`space-sm` to `space-md`).

### 3. Metric Trackers & Progress Bars
- Linear horizontal gauges with sharp 0px corners, encased in a 1px border.
- Target completion fills with stark black or signal color without gradient blending.
- Numerical readouts formatted as mono ratios (e.g., `180 / 250 تست`).

### 4. Input Fields & Loggers
- Clean, unrounded input boxes with white canvas and `1px solid #121316` border.
- Active focus state shifts border to 2px solid `#0055FF`.
- RTL placeholder text aligned precisely to the right margin with an 8px inset.

### 5. Buttons & Action Tiles
- **Primary**: Solid `#121316` background, `#FFFFFF` text, 0px radius, accompanied by sharp hover invert (white fill, black text, 2px border).
- **Secondary (Technical)**: `#FFFFFF` fill, 1px border, bold mono lettering.
- **Danger / Reset**: `#FF3B30` text with hairline red perimeter.