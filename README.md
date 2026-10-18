# ML Revision

An iOS-style MCQ revision site for NPTEL **Introduction to Machine Learning** (noc26_cs133): 168 questions from the Week 0–12 assignments and practice sets, with official answers, hints and explanations.

## Features
- Weekly assignments and practice sets, with per-week scores
- Mock test (all graded questions, shuffled), Quick 20, and Review mistakes
- Hints before answering and explanations after
- Study mode to show answers straight away
- Light and dark mode; layout adapts to phone and desktop
- Progress saved in your browser

## Run locally
```bash
python serve.py
```
Then open http://localhost:8000.

## Edit content
- Questions: `data/questions.json`
- Hints and explanations: `data/hints.txt` (`id || hint || explanation`)
- Page: `data/template.html`

After editing, rebuild `index.html`:
```bash
python build.py
```

## App icon
Add the site to your home screen ("Add to Home Screen" on iPhone, "Install app" on Android) to get the ML Revision icon and a full-screen app view. Icons live in `icons/` and are generated with:
```bash
python make_icons.py
```
