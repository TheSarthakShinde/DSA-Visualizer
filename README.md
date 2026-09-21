# DSA Visualizer

Django site. Homepage auto-lists every DSA problem. Each problem = one HTML file.

## Run locally
```
pip install -r requirements.txt
python manage.py runserver
```
Open http://127.0.0.1:8000

## Add a new problem (your workflow)
1. Copy `problems/templates/problems/_template.html`
2. Rename to `problems/templates/problems/<your_slug>.html` (e.g. `valid_parentheses.html`)
3. Fill in: title, solution code, and the JS viz block
4. (Optional) edit the first line comment: `<!-- difficulty: Medium | tags: stack -->`
5. `git add . && git commit -m "add valid parentheses" && git push`

That's it — no urls.py edits, no views.py edits. Homepage scans the
`problems/templates/problems/` folder on every request and lists whatever
`.html` files are in there (except `base.html`, `home.html`, `_template.html`).
The URL for a problem is just `/<slug>/`.

## Deploy — Render (easiest, free tier)
1. Push this repo to GitHub
2. New Web Service on render.com → connect the repo
3. It reads `render.yaml` automatically (build + start commands already set)
4. Deploy. Done — every push auto-redeploys.

## Deploy — Vercel
1. Push this repo to GitHub
2. Import the repo on vercel.com
3. `vercel.json` + `api/index.py` already route everything through Django's WSGI app
4. Deploy. Every push auto-redeploys.

Note: Vercel is serverless — fine for this since there's no database, just
Django rendering templates. Render is the more "normal" fit for Django if
you want zero surprises.
