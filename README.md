# Slatecliff

False-door / founding-beta landing for public adjuster claims software.

**Live:** https://slatecliff.com (GitHub Pages)

## Setup

1. Enable GitHub Pages on this repo: Settings → Pages → Deploy from branch `main` / root (`/`).
2. In your DNS host for `slatecliff.com`, point the apex to GitHub Pages:

   | Type | Name | Value |
   |------|------|--------|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `joshuaread.github.io` |

3. In Pages settings, set Custom domain to `slatecliff.com` and wait for DNS check + HTTPS.
4. Get a free [Web3Forms](https://web3forms.com) access key (emails go to your inbox). Paste it into `config.js` as `web3formsAccessKey`, commit, and push.

## Local preview

Open `index.html` in a browser, or:

```bash
python3 -m http.server 8080 --directory .
```
