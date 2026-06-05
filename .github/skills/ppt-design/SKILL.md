---
name: html Presentation Design Template
description: "Use this file as the complete specification to build a new single-file HTML presentation
from scratch on any topic, matching the look, feel, and interactivity of the
Digital Transformation Roadshow series."
Department: Shared
Author: Moussiaux Jeremy
version: 5132fd35
---
# FDIN Presentation — Design Blueprint

Use this file as the complete specification to build a new single-file HTML presentation
from scratch on any topic, matching the look, feel, and interactivity of the
Digital Transformation Roadshow series.

## Repository Quarto Default

For this repository, prefer a **Quarto revealjs deck** under `Knowledge/presentations/<deck>/`
unless the user explicitly asks for a standalone hand-authored HTML presentation.

Default contract for generated decks in this repo:
- Author must always be `Devashish Jain`
- Opening slide order must be: **title**, then **subtitle**, then **author**
- Default visual direction is **Luminus corporate light theme**, not the dark Roadshow variant
- Generated deck must be renderable with `quarto render <deck>.qmd --to revealjs`
- Keep one top-level `.qmd` render entrypoint per deck folder
- Only add support files when Quarto generates them or when the deck actually needs local assets/includes

### Quarto revealjs frontmatter baseline

Use this as the starting point for repo presentations:

```yaml
---
title: "Presentation Title"
subtitle: "Presentation Subtitle"
author: "Devashish Jain"

format:
  revealjs:
    theme: white
    controls: true
    keyboard: true
    navigation-mode: linear
    hash: true
    history: true
    slide-number: true
    preview-links: auto
    transition: fade
    auto-stretch: false
    center: false
---
```

### Required Quarto structure validation

Before finishing a Quarto deck, verify all of the following:
- The deck has exactly one top-level render entrypoint `.qmd`
- The frontmatter contains `title`, `subtitle`, and `author: "Devashish Jain"`
- The frontmatter includes a `format.revealjs` block
- Any `{{< include ... >}}` paths resolve relative to the render entrypoint
- Any local image or file references exist under the same deck folder
- `quarto render ... --to revealjs` succeeds without path errors
- Rendered HTML contains Reveal.js markup so keyboard navigation works in a normal browser session

### Generated support files: when they are expected

Quarto revealjs often creates a sibling `*_files/` folder next to the rendered HTML.
That is normal and was not specific to the demo deck.

Use this rule:
- If Quarto produces `*_files/`, keep it
- Do not add extra author-managed JS/CSS/image files unless the deck actually needs them
- Prefer inline CSS in the `.qmd` for simple theme customisation
- Only introduce includes or assets when they materially improve the deck

The existing `ai-assisted-coding` deck also uses additional files, but mainly because it
has real slide assets and included content. A simple deck does not need that level of structure.

---

## 1. Architecture Overview

Every presentation is a **single self-contained HTML file**. There are no separate
JS, CSS, or asset bundles. The file is opened directly in a browser, navigated with
keyboard arrow-keys or on-screen buttons, and projected full-screen.

Structure inside the file:
```
<head>
  ├─ Tailwind CDN + custom config
  ├─ Babel standalone (transpiles JSX in-browser)
  ├─ Import map  (React 19, react-dom, lucide-react)
  ├─ Google Fonts (Inter)
  └─ <style> block  (global overrides + keyframes)
<body>
  └─ <div id="root">
       └─ React app (transpiled from <script type="text/babel">)
```

---

## 2. Dependency Versions (pin these exactly)

| Library | CDN / Import | Version |
|---------|-------------|---------|
| Tailwind CSS | `https://cdn.tailwindcss.com` | v3 (CDN build) |
| Babel standalone | `https://unpkg.com/@babel/standalone@7.23.5/babel.min.js` | 7.23.5 |
| React | `https://esm.sh/react@19.0.0` | 19.0.0 |
| react-dom | `https://esm.sh/react-dom@19.0.0` | 19.0.0 |
| lucide-react | `https://esm.sh/lucide-react@0.475.0` | 0.475.0 |
| Inter font | Google Fonts | 300–900 weights |

Script tag for the React component:
```html
<script type="text/babel" data-type="module" data-presets="react">
  import React, { useState, useEffect, useCallback } from 'react';
  import { createRoot } from 'react-dom/client';
  import { /* icons */ } from 'lucide-react';
  ...
  const container = document.getElementById('root');
  createRoot(container).render(<App />);
</script>
```

---

## 3. Brand Color System

Defined as a custom Tailwind config block in the `<head>`:

### Primary brand palette

| name | Tailwind alias | Hex | Usage |
|------|---------------|-----|-------|
| Luminus Green | `emerald-500` / `emerald-600` | `#4EA72E` / `#3f8722` | Primary CTA, topic labels, dividers, icon backgrounds, progress bar fill |
| Luminus Deep Green | `emerald-700` | `#2d621f` | Team card backgrounds (primary), hover states, Industrial card bg |
| Luminus Navy | `indigo-500` | `#093670` | Secondary accent (rarely used directly; mostly via decorative blobs) |
| Luminus Orange | `orange-500` | `#FE5815` | Warning accent, lifecycle Ideation stage, gradient endpoints |
| Slate 900 | `slate-900` | `#0f172a` | All primary text, headlines |
| Slate 600 | `slate-600` | `#475569` | Body paragraph text, descriptions |
| Slate 500 | `slate-500` | `#64748b` | Secondary body text (use sparingly, always at normal weight — no `font-light`) |
| Page BG | custom | `#fcfdfe` | `body` background — near-white, not pure white |

### Lifecycle stage palette (slide 8)

| Stage | Color |
|-------|-------|
| Ideation | `#E94B3C` (red) |
| Experimentation | `#FF6600` (orange) |
| Industrialisation | `#B8D432` (yellow-green) |
| Maintenance | `emerald-600` |

### Contrast requirements (projector / bright room rule)

> **Never place light text on a light background.** Minimum requirements:
- White text: only on `emerald-600` or darker, `#E94B3C`, `#FF6600`, `#B8D432`, or `emerald-700`.
- `text-slate-500` or `text-slate-600`: acceptable on pure white cards only. **Never use `font-light`** on body text that will be projected.
- `text-slate-400`: reserved for purely decorative elements (slide number watermarks, disabled states). Do not use for any readable content.
- Card borders must be at minimum `border-slate-200` (`#e2e8f0`) on white backgrounds to stay visible under projection.
- Recommended global CSS override for projector safety: `.border-slate-100 { border-color: #e2e8f0 !important; }`

---

## 4. Typography Scale

Font family: `Inter` (sans-serif system fallback).

| Role | Classes | Weight |
|------|---------|--------|
| Main slide title | `text-5xl font-extrabold tracking-tight text-slate-900` | 800 |
| Hero / CTA title | `text-7xl font-black tracking-tight text-slate-900 leading-[1.1]` | 900 |
| Section title inside cards | `text-3xl font-black text-slate-900` | 900 |
| Sub-card heading | `text-2xl font-bold text-slate-900` | 700 |
| Topic eyebrow label | `text-sm font-black uppercase tracking-[0.3em] text-emerald-600` | 900 |
| Slide subtitle | `text-xl text-slate-600 max-w-3xl leading-relaxed` | 400 |
| Card description / body | `text-base text-slate-600 leading-relaxed` | 400 |
| Small label / tag | `text-[10px] font-black uppercase tracking-widest text-slate-500` | 900 |
| Process step sub-label | `text-[10px] text-slate-500 font-medium uppercase tracking-wider` | 500 |
| Bullet item | `text-base text-slate-700` or `text-lg text-slate-600` | 400 |
| Navigation meta | `text-[10px] font-bold text-slate-400 uppercase tracking-widest` | 700 |

Key rule: **compress whitespace for projection** — use `tracking-tight` or `tracking-[0.3em]` at opposite ends to control density, never `font-light` on content.

---

## 5. Layout & Spacing Conventions

### Slide wrapper
```jsx
<div className="min-h-screen bg-[#fcfdfe] overflow-hidden relative selection:bg-emerald-100 selection:text-emerald-900">
```

### SlideLayout component (reusable wrapper for content slides)
```jsx
const SlideLayout = ({ children, title, subtitle, topic, className = "" }) => (
  <div className={`w-full h-full flex flex-col pt-12 md:pt-16 px-12 md:px-20 pb-16 md:pb-20 text-slate-900 ${className}`}>
    <div className="max-w-7xl w-full mx-auto h-full flex flex-col">
      {title && (
        <div className="mb-8 shrink-0">
          {topic && <p className="text-sm font-black uppercase tracking-[0.3em] text-emerald-600 mb-2">{topic}</p>}
          <h1 className="text-5xl font-extrabold tracking-tight text-slate-900 mb-2">{title}</h1>
          {subtitle && <p className="text-xl text-slate-600 max-w-3xl leading-relaxed">{subtitle}</p>}
          <div className="h-1.5 w-20 bg-emerald-500 mt-6 rounded-full"></div>
        </div>
      )}
      <div className="flex-1 min-h-0 relative flex flex-col justify-center no-scrollbar">
        {children}
      </div>
    </div>
  </div>
);
```

### Padding guide
| Zone | Value |
|------|-------|
| Slide outer padding (desktop) | `px-20 pt-16 pb-20` |
| Slide outer padding (mobile) | `px-12 pt-12 pb-16` |
| Card inner padding (large) | `p-10` or `p-8` |
| Card inner padding (medium) | `p-7` or `p-6` |
| Card inner padding (small) | `p-5` or `p-4` |
| Gap between cards | `gap-8` (default) · `gap-6` (compact) |

### Grid patterns used

| Slide type | Grid |
|-----------|------|
| 3-column equal | `grid-cols-1 md:grid-cols-3 gap-8` |
| 2-column equal | `grid-cols-1 md:grid-cols-2 gap-8` |
| 4-column lifecycle | `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6` |
| Team member grid | `grid-cols-2 md:grid-cols-4 gap-6` |

### Max widths
- Content area: `max-w-7xl mx-auto`
- Text-heavy content: `max-w-6xl mx-auto`
- Single paragraph / quote: `max-w-3xl` or `max-w-2xl`

---

## 6. Slide Types & Templates

### 6.1 Title Slide (slide 1 and final CTA)

Full-height centred layout — no `SlideLayout` wrapper:

```jsx
<div className="flex flex-col items-center justify-center h-full text-center space-y-10 animate-fadeIn px-6">
  {/* Icon badge */}
  <div className="inline-block p-6 bg-white rounded-[2.5rem] border border-slate-200 shadow-2xl shadow-emerald-100/50">
    <TopicIcon className="text-emerald-500 w-16 h-16" />
  </div>
  {/* Headline */}
  <div className="space-y-4">
    <h1 className="text-7xl font-black tracking-tight text-slate-900 leading-[1.1]">
      Primary <span className="text-emerald-500">Keyword</span> <br />
      <span className="text-slate-400 font-light"> secondary descriptor</span>
    </h1>
    <p className="text-2xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
      Supporting one-liner describing the presentation's purpose.
    </p>
    <p className="text-sm font-bold uppercase tracking-[0.25em] text-slate-500">
      Devashish Jain
    </p>
  </div>
  {/* CTA button */}
  <button onClick={nextSlide} className="group px-10 py-5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-2xl font-bold flex items-center gap-3 transition-all hover:scale-105 hover:shadow-2xl hover:shadow-emerald-500/30 active:scale-95">
    <PlayCircle size={24} className="group-hover:animate-pulse" /> Start Presentation
  </button>
</div>
```

For Quarto title slides in this repository, keep the visible order the same:
1. Title
2. Subtitle
3. Author (`Devashish Jain`)

Do not place the author above the subtitle.

### 6.2 Standard Content Slide with SlideLayout

Data driven — use `AGENDA_ITEMS`, `TEAM_MEMBERS`, or your own constant arrays:

```jsx
<SlideLayout topic="SECTION NAME" title="Slide Title" subtitle="Supporting description.">
  <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl mx-auto">
    {ITEMS.map((item, i) => (
      <CardComponent key={i} data={item} />
    ))}
  </div>
</SlideLayout>
```

### 6.3 Two-Column Detail Slide

Best for showing feature list + a highlight/roadmap concept side by side:

```jsx
<SlideLayout topic="WHAT WE DO" title="Feature Area" subtitle="...">
  <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full h-full py-2">
    {/* Left: white card with list */}
    <div className="bg-white p-7 rounded-[2rem] border border-slate-200 shadow-md flex flex-col">
      ...
    </div>
    {/* Right: coloured highlight card */}
    <div className="bg-amber-100 text-slate-900 rounded-[2.5rem] p-10 flex flex-col relative overflow-hidden">
      ...
    </div>
  </div>
</SlideLayout>
```

### 6.4 Final Collaboration / Summary Slide

Full-height centred with a 2×2 grid of role-split cards below a large headline:

```jsx
<div className="flex flex-col items-center justify-center h-full text-center space-y-8 animate-fadeIn p-16 max-w-6xl mx-auto">
  <h2 className="text-7xl font-black tracking-tighter text-slate-900">Slide Title</h2>
  <p className="text-2xl text-slate-600 max-w-3xl mx-auto leading-relaxed">Supporting message</p>
  <div className="grid grid-cols-2 gap-6 w-full">
    <div className="p-8 bg-gradient-to-br from-[#E94B3C]/10 to-[#FF6600]/10 rounded-3xl border-2 border-[#FF6600]/20">
      ...
    </div>
    <div className="p-8 bg-gradient-to-br from-[#B8D432]/10 to-[#34A853]/10 rounded-3xl border-2 border-[#34A853]/20">
      ...
    </div>
  </div>
  {/* Gradient CTA banner */}
  <div className="p-10 bg-gradient-to-r from-[#FF6600] to-[#B8D432] rounded-[3rem] w-full shadow-xl">
    <h3 className="text-white font-black text-3xl mb-3">What's Next</h3>
    <p className="text-white/90 text-lg leading-relaxed">Call to action text.</p>
  </div>
  <button onClick={() => setCurrentSlide(0)} className="text-slate-400 hover:text-[#34A853] flex items-center gap-3 transition-all uppercase tracking-[0.4em] font-black text-xs group">
    <Compass size={20} className="group-hover:rotate-45 transition-transform" /> Restart
  </button>
</div>
```

---

## 7. Card Components

### 7.1 Primary highlight card (dark green)

Use for the featured / "recommended" option in a comparison:

```jsx
<div className="p-8 md:p-10 rounded-[2.5rem] bg-emerald-700 border border-emerald-600 shadow-2xl shadow-emerald-100 relative overflow-hidden flex flex-col">
  <h3 className="text-3xl font-black mb-6 text-white">Card Title</h3>
  <ul className="space-y-4 text-emerald-50 text-lg">
    <li className="flex items-start gap-3">
      <div className="w-5 h-5 rounded-full bg-white/10 text-white flex items-center justify-center shrink-0 mt-1">•</div>
      <span>Bullet point text</span>
    </li>
  </ul>
</div>
```

### 7.2 Secondary card (white)

Use for alternative options, supplemental information:

```jsx
<div className="p-8 rounded-[2.5rem] bg-white border border-slate-200 shadow-md flex flex-col hover:shadow-xl hover:border-emerald-200 transition-all group">
  <div className="flex items-center gap-3 mb-4">
    <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center">
      <IconName size={24} />
    </div>
    <h3 className="text-2xl font-bold text-slate-900">Title</h3>
  </div>
  <p className="text-slate-600 text-base leading-relaxed mb-6">Description text.</p>
  <ul className="space-y-3 text-slate-700 text-base">
    <li className="flex items-start gap-3">
      <span className="text-emerald-600 font-bold mt-1">→</span>
      <span><strong>Label:</strong> description</span>
    </li>
  </ul>
</div>
```

### 7.3 Elevated green tinted card (AI / roadmap concepts)

```jsx
<div className="bg-emerald-50 p-8 rounded-[2.5rem] border border-emerald-200 shadow-2xl shadow-emerald-100 flex flex-col relative overflow-hidden">
  {/* Decorative background icon */}
  <div className="absolute top-0 right-0 p-8 pointer-events-none opacity-10">
    <LargeIcon size={180} />
  </div>
  <div className="relative z-10">
    ...content...
  </div>
</div>
```

### 7.4 Lifecycle / Process step card (coloured)

```jsx
<div className={`${bgColor} p-8 pb-16 rounded-[2.5rem] flex flex-col items-center text-center shadow-lg hover:-translate-y-3 transition-all duration-300 text-white relative group`}>
  <div className="mb-6 p-5 rounded-2xl bg-white/20 backdrop-blur-lg border border-white/20 shadow-xl group-hover:scale-110 transition-transform">
    <StepIcon size={32} />
  </div>
  <h3 className="text-lg font-black mb-3 uppercase tracking-wider">{label}</h3>
  <p className="text-white/95 text-xs leading-relaxed font-medium">{description}</p>
  {/* Step number watermark */}
  <div className="absolute bottom-4 opacity-20 text-[36px] font-black select-none pointer-events-none">0{i+1}</div>
</div>
```

### 7.5 Team member card

```jsx
{/* isCore = permanent team member; intern cards are white */}
const cardClass = isCore
  ? 'bg-emerald-700 text-white border-emerald-600 shadow-xl shadow-emerald-200'
  : 'bg-white text-slate-900 border-slate-200 shadow-md';

<div className={`p-6 md:p-8 rounded-[2rem] border transition-all duration-300 flex flex-col items-center text-center group ${cardClass} hover:-translate-y-2`}>
  {/* Photo or placeholder */}
  {member.image
    ? <img src={member.image} alt={member.name} className="w-20 h-20 md:w-24 md:h-24 rounded-[1.5rem] shadow-lg mb-6" />
    : <div className="w-20 h-20 md:w-24 md:h-24 rounded-[1.5rem] bg-white/10 flex items-center justify-center mb-6">
        <UserPlus className="text-white/40" size={32} />
      </div>
  }
  <h4 className="font-bold text-lg mb-1">{member.name}</h4>
  <p className={`text-xs font-medium uppercase tracking-widest ${isCore ? 'text-white' : 'text-slate-600'}`}>
    {member.role}
  </p>
</div>
```

---

## 8. Iconography

Use **lucide-react** exclusively. Common icons used:

| Context | Icon |
|---------|------|
| Topic: work / processes | `Layers`, `Cog`, `Factory` |
| Topic: data / analytics | `Database`, `FileSpreadsheet`, `BarChart3` |
| Topic: AI / intelligence | `Brain`, `Cpu`, `FlaskConical` |
| Topic: people | `Users`, `User`, `UserPlus` |
| Topic: ideas / strategy | `Lightbulb`, `Compass` |
| Topic: security / health | `ShieldCheck` |
| Navigation | `ChevronLeft`, `ChevronRight`, `PlayCircle`, `ArrowRight` |
| Misc energy | `Zap` |

Icon sizes: `24px` (list items), `28px` (card icons in icon boxes), `32px` (lifecycle steps), `36–40px` (featured section icons), `16–18px` (icon in small pill).

Icon container pattern:
```jsx
<div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
  <IconName size={24} />
</div>
```

---

## 9. Animations

### 9.1 Defined in `<style>` block

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn { animation: fadeIn 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
.animate-spin-slow { animation: spin-slow 12s linear infinite; }
```

### 9.2 Slide transition (applied per slide `<div>`)

```jsx
className={`absolute inset-0 transition-all duration-1000 transform ${
  index === currentSlide
    ? 'opacity-100 translate-x-0 scale-100'
    : index < currentSlide
      ? 'opacity-0 -translate-x-[20%] scale-95 pointer-events-none'
      : 'opacity-0 translate-x-[20%] scale-105 pointer-events-none'
}`}
```

### 9.3 Hover micro-interactions used throughout

```
hover:-translate-y-2   ← team cards, main cards
hover:-translate-y-3   ← lifecycle step cards
hover:scale-105        ← CTA buttons
hover:scale-110        ← icon boxes, nav arrows
hover:shadow-xl        ← secondary cards
group-hover:scale-110  ← icon inside a parent group
group-hover:rotate-45  ← Compass restart icon
```

---

## 10. Navigation System

### 10.1 State & keyboard handler

```jsx
const [currentSlide, setCurrentSlide] = useState(0);
const totalSlides = N;  // set to total number of slides

const nextSlide = useCallback(() => setCurrentSlide(p => (p + 1) % totalSlides), []);
const prevSlide = useCallback(() => setCurrentSlide(p => (p - 1 + totalSlides) % totalSlides), []);

useEffect(() => {
  const onKey = (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
    if (e.key === 'ArrowLeft') prevSlide();
  };
  window.addEventListener('keydown', onKey);
  return () => window.removeEventListener('keydown', onKey);
}, [nextSlide, prevSlide]);
```

### 10.2 Top progress bar

```jsx
<div className="fixed top-0 left-0 w-full h-2 bg-slate-200 z-[100]">
  <div className="h-full bg-emerald-500 transition-all duration-700 ease-out shadow-[0_0_15px_rgba(16,185,129,0.4)]"
       style={{ width: `${((currentSlide + 1) / totalSlides) * 100}%` }}
  ></div>
</div>
```

### 10.3 Logo (fixed top-right, z-[200])

```jsx
<div className="fixed top-4 right-6 z-[200] pointer-events-none">
  <img src="LOGO_URL" alt="Company logo" className="h-10 md:h-12 object-contain" />
</div>
```

### 10.4 Bottom nav bar

```jsx
<div className="absolute bottom-10 left-0 w-full px-12 z-20 flex items-center justify-between">
  {/* Left: prev/next buttons */}
  <div className="flex gap-5">
    <button onClick={prevSlide} disabled={currentSlide === 0}
      className="p-4 bg-white border border-slate-300 rounded-2xl text-slate-600 hover:text-emerald-600 hover:border-emerald-300 transition-all shadow-xl shadow-slate-200/50 disabled:opacity-0 hover:scale-110 active:scale-95">
      <ChevronLeft size={24} strokeWidth={2.5} />
    </button>
    <button onClick={nextSlide} disabled={currentSlide === totalSlides - 1}
      className="p-4 bg-white border border-slate-300 rounded-2xl text-slate-600 hover:text-emerald-600 hover:border-emerald-300 transition-all shadow-xl shadow-slate-200/50 disabled:opacity-0 hover:scale-110 active:scale-95">
      <ChevronRight size={24} strokeWidth={2.5} />
    </button>
  </div>
  {/* Right: meta info */}
  <div className="flex items-center gap-10">
    <div className="hidden lg:flex flex-col items-end">
      <span className="text-[10px] font-black text-emerald-600 tracking-[0.3em] uppercase mb-0.5">Department Name</span>
      <div className="flex items-center gap-2">
        <div className="h-1 w-1 rounded-full bg-slate-300"></div>
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
          Slide {String(currentSlide + 1).padStart(2, '0')} — {totalSlides}
        </span>
      </div>
    </div>
    <div className="h-10 w-[1px] bg-slate-200 hidden lg:block"></div>
    <div className="hidden lg:block">
      <div className="text-slate-900 text-[10px] font-black tracking-[0.2em] uppercase">Organisation Year</div>
    </div>
  </div>
</div>
```

---

## 11. Decorative Background

Kept minimal — too prominent, these blur-blobs wash out projected content:

```jsx
<div className="absolute top-0 left-0 w-full h-full pointer-events-none overflow-hidden">
  <div className="absolute -top-40 -left-40 w-96 h-96 bg-indigo-50 rounded-full blur-[100px] opacity-20"></div>
  <div className="absolute top-1/2 -right-40 w-80 h-80 bg-blue-50 rounded-full blur-[100px] opacity-15"></div>
  <div className="absolute -bottom-20 left-1/4 w-60 h-60 bg-indigo-100 rounded-full blur-[120px] opacity-10"></div>
</div>
```

> **Rule**: keep blur blob opacities ≤ 20% for projector use. Never exceed 30% or they compete with slide content on bright screens.

---

## 12. Accessibility & Security Patterns

### Accessibility
- `body` background: `#fcfdfe` (not pure white — eases eye strain under projection)
- `selection:bg-emerald-100 selection:text-emerald-900` on root div
- `:focus-visible { outline: 2px solid #4EA72E; outline-offset: 2px; }` in CSS
- `@media (prefers-reduced-motion: reduce)` block disables all animations
- `alt` text on all `<img>` tags
- Images get `loading="lazy" decoding="async"` via post-load JS enhance

### Security
- All external `<a target="_blank">` links must include `rel="noopener noreferrer"`  
  (the post-render JS enhance block handles this automatically — include it in every file):

```html
<script>
  (function () {
    function enhance() {
      document.querySelectorAll('a[target="_blank"]').forEach(a => {
        try {
          if (new URL(a.href, location.href).hostname !== location.hostname) {
            const rel = (a.getAttribute('rel') || '').toLowerCase();
            if (!/\bnoopener\b/.test(rel) || !/\bnoreferrer\b/.test(rel))
              a.setAttribute('rel', (rel + ' noopener noreferrer').trim());
          }
        } catch (_) {}
      });
      document.querySelectorAll('img').forEach(img => {
        if (!img.hasAttribute('loading'))  img.setAttribute('loading', 'lazy');
        if (!img.hasAttribute('decoding')) img.setAttribute('decoding', 'async');
      });
    }
    if (document.readyState === 'complete' || document.readyState === 'interactive') setTimeout(enhance, 0);
    else document.addEventListener('DOMContentLoaded', enhance, { once: true });
    window.addEventListener('load', enhance, { once: true });
  })();
</script>
```

---

## 13. Content Writing Patterns

### Topic eyebrow (appears above slide title)
- ALL CAPS, 2–3 words, maps to the Agenda section: `"WHO ARE WE"`, `"WHAT WE DO"`, `"HOW CAN WE COLLABORATE"`

### Slide title
- Title case, 3–6 words, specific: `"The Team"`, `"Focus Areas"`, `"The Lifecycle"`

### Slide subtitle
- One sentence, lowercase (sentence case), ends without period, max ~80 chars: `"A multi-disciplinary team driving the digital agenda."`

### Bullet points inside cards
- Pattern: `<strong>Label:</strong> short descriptor phrase`
- Arrow prefix: `→` in emerald-600 for white cards; `•` in white/10 for dark cards

### Highlight / quote block
- `bg-emerald-50/80 p-7 rounded-[2rem] border border-emerald-100 relative` container
- Small lightbulb icon badge floated top-left: `absolute -top-4 -left-4 w-10 h-10 bg-white rounded-xl`
- Text: `text-emerald-900 font-medium italic text-lg leading-relaxed`

### Demo link pattern
```jsx
<div className="mt-4 pt-4 border-t border-slate-100">
  <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-1">Demo</span>
  <a href="URL" target="_blank" rel="noopener noreferrer"
     className="text-sm font-bold text-slate-800 hover:underline hover:text-emerald-600 transition-all cursor-pointer">
    Demo Display Name
  </a>
</div>
```

### Gradient CTA banner (end of last slide)
```jsx
<div className="p-10 bg-gradient-to-r from-[#FF6600] to-[#B8D432] rounded-[3rem] w-full shadow-xl">
  <h3 className="text-white font-black text-3xl mb-3">Next step headline 🚀</h3>
  <p className="text-white/90 text-lg leading-relaxed">Supporting invitation text.</p>
</div>
```

---

## 14. Checklist: Creating a New Presentation From Scratch

Follow this sequence to produce a working presentation file in one session.

### Step 1 — Define content skeleton
- [ ] Choose presentation topic and audience
- [ ] Define 3 agenda sections (matching the `AGENDA_ITEMS` pattern)
- [ ] List all slides (recommended: 8–10 for a 20-minute session)
- [ ] Assign each slide a type: title / agenda / team / two-column detail / process flow / lifecycle / final CTA

### Step 2 — Bootstrap the file
- [ ] Copy the `<head>` section verbatim (Tailwind config, Babel, importmap, fonts, style block)
- [ ] Adjust `tailwind.config` colours only if your brand palette differs
- [ ] Keep the `<style>` block including the `border-slate-100` CSS override

### Step 3 — Define constants at top of the React script
```js
const AGENDA_ITEMS = [ ... ];   // 3 items with id, title, icon, description
const TEAM_MEMBERS = [ ... ];   // name, role, image, isIntern flag
// add domain-specific data arrays here
```

### Step 4 — Build slide array
- [ ] Slide 1: Title slide  
- [ ] Slide 2: Agenda (use `SlideLayout` + map `AGENDA_ITEMS`)  
- [ ] Slide 3: Team (use `SlideLayout` + map `TEAM_MEMBERS`)  
- [ ] Slides 4–7: Content slides using `SlideLayout` with 2-col or grid layouts  
- [ ] Slide 8: Lifecycle / Process steps  
- [ ] Slide 9: Collaboration / CTA (full-height centred)

### Step 5 — Fill navigation constants
- [ ] Set `const totalSlides = N` to match the number of slide entries in the array

### Step 6 — Contrasts review (before presenting)
- [ ] No `font-light` on any body text visible in a slide
- [ ] No `text-slate-400` on readable content (only decorative/disabled use)
- [ ] All card borders are `border-slate-200` or stronger
- [ ] White text only appears on `emerald-600`+, `#E94B3C`, `#FF6600`, `#B8D432`
- [ ] Blur blob opacities ≤ 20%
- [ ] Navigation buttons have `border-slate-300 text-slate-600` (visible when prev/next appear)
- [ ] Progress bar background is `bg-slate-200`

### Step 7 — Security review
- [ ] All `<a target="_blank">` links have `rel="noopener noreferrer"`
- [ ] The post-render JS enhance block is present at bottom of `<body>`
- [ ] No credentials, API keys, or internal paths exposed in the HTML source

### Step 8 — Test
- [ ] Open in browser, press **F11** for full-screen
- [ ] Navigate with `← →` arrow keys through every slide
- [ ] Test on a projector or bright monitor to verify contrast holds

---

*Design system documented from RoadshowPresentation V7.html — Luminus FDIN Digital Support Services, 2026.*