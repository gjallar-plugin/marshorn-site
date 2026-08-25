# Gjallar — Static Website (Marshorn Technologies Co., Ltd.)

A dependency-free static website (`index.html` + `styles.css` + `script.js`,
no build step) intended for startup-program applications (NVIDIA Inception,
Google for Startups, etc.) that require "a working website."

**Naming convention used on this site:** `Gjallar` is the product/project
name (unchanged); `Marshorn Technologies Co., Ltd.` is the legal entity
behind it (shown in the header suffix, the Contact card, and the footer
copyright line) — similar to "Gemini, by Google."

**Production domain:** `https://marshorn.com` (also `https://www.marshorn.com`
once DNS is configured).

**Pitch deck:** `pitch-deck.html` (10 landscape slides). Open it and use
Print → Save as PDF (layout: landscape, margins: none, backgrounds: on).
A generated `Gjallar-Pitch-Deck.pdf` may also be in this folder for uploads.

## Before you deploy — customize these

1. **Legal entity name** — currently "Marshorn Technologies Co., Ltd."
   Update in `index.html` (`<title>`, `.brand-suffix`, the Contact card's
   "Legal Entity" field, and the footer) if the registered name changes.
2. **Contact email** — currently `scott.fang@marshorn.com` in `index.html`.
   Keep this on the `marshorn.com` domain for startup-program applications.
3. **Founder profiles** — Team card links to
   [github.com/Scottman625](https://github.com/Scottman625) and
   [LinkedIn](https://www.linkedin.com/in/scottfang6a6965753951).
4. **Domain** — apex domain is `marshorn.com` (see `CNAME` in this folder).
   Configure DNS as described below under GitHub Pages.
5. **Team / stage copy** — Company, Product stage, Evidence, and Team sections
   should stay aligned with what is actually frozen vs still unpublished.

## Deploy: GitHub Pages + marshorn.com

A workflow at `.github/workflows/deploy-site.yml` publishes this `site/`
folder automatically on every push to `main` that touches `site/` or the
workflow file.

### 1. Enable GitHub Pages (required once, before deploy succeeds)

The workflow will fail with `Get Pages site failed … Not Found` until Pages
is enabled. The default `GITHUB_TOKEN` cannot turn Pages on for you.

1. Open https://github.com/gjallar-plugin/gjallar-adversarial/settings/pages
2. Under **Build and deployment → Source**, choose **GitHub Actions**
   (not "Deploy from a branch").
3. Re-run the failed workflow: **Actions → Deploy static site → Re-run all
   jobs**, or push any change under `site/`.
4. Temporary URL after the first success:
   `https://gjallar-plugin.github.io/gjallar-adversarial/`

### 2. Attach the custom domain in GitHub

1. Still under **Settings → Pages → Custom domain**, enter `marshorn.com`.
2. Check **Enforce HTTPS** after DNS has propagated (GitHub will provision
   the certificate; this can take a few minutes to a few hours).
3. Optionally also add `www.marshorn.com` as a redirect/alias in the same
   Pages settings once apex DNS is working.

The repo already includes `site/CNAME` with:

```text
marshorn.com
```

GitHub Pages will keep that domain selected across deploys.

### 3. Configure DNS at your registrar (for marshorn.com)

At the DNS panel where you bought `marshorn.com`, create:

| Type | Host / Name | Value | Notes |
|------|-------------|-------|-------|
| **A** | `@` (apex) | `185.199.108.153` | GitHub Pages |
| **A** | `@` | `185.199.109.153` | GitHub Pages |
| **A** | `@` | `185.199.110.153` | GitHub Pages |
| **A** | `@` | `185.199.111.153` | GitHub Pages |
| **CNAME** | `www` | `gjallar-plugin.github.io` | org Pages host for this repo |

Do **not** point the apex `A` records at a random host; use the four GitHub
Pages IPs above (current official values).

Propagation tip: after saving DNS, wait until
`https://marshorn.com` resolves, then turn on **Enforce HTTPS** in GitHub
Pages if it was still greyed out.

### 4. Verify

```bash
# Should show GitHub Pages IPs
nslookup marshorn.com

# Should return HTTP 200 once deploy + DNS + TLS are ready
curl -I https://marshorn.com
```

> Note: if this repository is private and your plan does not include private
> Pages, either make the repo public, publish `site/` from a separate public
> repo, or use Netlify / Cloudflare Pages instead.

## Other deploy options

### Netlify

1. Go to <https://app.netlify.com/drop>.
2. Drag the `site/` folder onto the page.
3. Add `marshorn.com` under **Site settings → Domain management**.

### Vercel

```bash
npm i -g vercel
cd site
vercel --prod
```

### Cloudflare Pages

1. Create a Pages project from this Git repository.
2. Set **Build output directory** to `site` and leave the build command empty.
3. Attach `marshorn.com` under **Custom domains**.

## Local preview

```bash
python -m http.server 8080
```

Then open <http://localhost:8080> in a browser.
