# michaellivermore.com

Static site, no build tools required. Six HTML pages plus `assets/style.css`.

## Editing

Page text lives in `build.py` (one block per page). After editing, run
`python build.py` to regenerate the HTML. You can also edit the `.html`
files directly if you prefer; the script just keeps the nav and header
consistent across pages.

## First-time setup

1. Run `.\fetch-assets.ps1` in PowerShell from this folder. It downloads the
   portrait, book covers, podcast art, and CV from the current WordPress
   site into `assets/`. (Do this before cancelling the WordPress plan.)
2. Open `index.html` in a browser to check the site locally.

## Publishing on GitHub Pages

1. Create a new GitHub repository (public), e.g. `michaellivermore.com`.
2. Push this folder to it (`git init`, `git add .`, `git commit`, `git push`).
3. In the repo: Settings → Pages → Source: "Deploy from a branch", branch
   `main`, folder `/ (root)`. Save. The site appears at
   `https://<username>.github.io/<repo>/` within a minute or two.
4. Custom domain: in the same Pages settings, enter `michaellivermore.com`
   and tick "Enforce HTTPS". GitHub creates a `CNAME` file in the repo.
5. At the domain registrar (currently WordPress.com; transfer to Cloudflare
   or Porkbun at your leisure), set DNS:
   - Four `A` records for `@` → 185.199.108.153, 185.199.109.153,
     185.199.110.153, 185.199.111.153
   - One `CNAME` record for `www` → `<username>.github.io`
   DNS changes take up to a day to propagate; the WordPress site keeps
   serving until then, so there is no downtime.
6. Once the new site is live on the domain, cancel the WordPress.com plan
   (keep the domain registration until it's transferred).

## Content folders

- The Miscellany page's items are lists in `build.py` (`PAGES["miscellany.html"]`),
  one line per item; add new pieces there. Two YouTube IDs at the top of that
  block choose which talks get embedded players.

- `content/podcast/episodes.json` and `content/podcast/transcripts/` — the
  Free Range archive, extracted from the freerangepodcast.org WordPress export
  by `tools/extract-podcast.py`. `build.py` makes `podcast.html` and one page
  per episode under `podcast/`. Guest names in the JSON are editable.

- `content/owcal/*.html` — one fragment per OWCAL season, pulled from the
  WordPress export; `build.py` assembles them onto the workshop page. Add a
  new season by adding a file named like `2025-26.html`.
