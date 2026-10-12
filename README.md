# SlateCliff

Curated gift guides for the men in your life. Served at https://slatecliff.com by GitHub Pages from `main`.

- All content lives in `_src/site.json` (products, prices, guide text).
- **Affiliate links:** set `affiliate_url` on a product in `_src/site.json`, then run `python3 _src/build.py` and commit. Buy buttons use `affiliate_url` when set and fall back to `url`.
- The previous "Claims desk for public adjusters" page is preserved on the `archive-claims-desk` branch.
