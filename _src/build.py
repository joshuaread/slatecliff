#!/usr/bin/env python3
"""Builds the static SlateCliff site from _src/site.json.
To swap in affiliate links: set "affiliate_url" on a product in _src/site.json, then run
    python3 _src/build.py
from the repo root and commit. Nothing else needs to change."""
import json, os, html, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, '_src', 'site.json')))
P = {p['id']: p for p in D['products']}
SITE = 'https://slatecliff.com'
TAG = "Small gifts he'll actually keep."
CHECKED = D['price_checked']
e = html.escape
OCC = [('christmas', 'Christmas'), ('anniversary', 'Anniversary'), ('birthday', 'Birthday'), ('fathers-day', "Father's Day")]
BUD = [('under-30', 'Under $30'), ('under-100', 'Under $100'), ('under-150', 'Under $150'), ('splurge', 'Worth the splurge')]
GUY = [('husband', 'Husband'), ('boyfriend', 'Boyfriend'), ('dad', 'Dad & father-in-law'), ('coffee', 'Coffee guy'), ('edc', 'Everyday-carry guy'), ('handy', 'Handy guy'), ('bourbon', 'Bourbon guy'), ('outdoors', 'Outdoors guy')]
GUY_EXTRA = {'husband': ['gifts-for-handy-husband'], 'boyfriend': ['edc-gifts-for-boyfriend'], 'dad': ['coffee-gifts-for-dad']}
TONES = ['#e9e5de', '#e2ddd4', '#dcd6cc', '#ece9e3', '#d9d4cb', '#e6e1d8']

def tone(s): return TONES[int(hashlib.md5(s.encode()).hexdigest(), 16) % len(TONES)]
def money(v): return f"${v:,.2f}".replace('.00', '')
def link(p): return p.get('affiliate_url') or p['url']

def page(path, title, desc, body, extra_head='', og_type='website'):
    url = SITE + path
    nav = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in [('/guides/#occasion', 'Occasion'), ('/guides/#budget', 'Budget'), ('/guides/#guy', 'By Guy'), ('/guides/', 'All Guides')])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="SlateCliff">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">

<meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="bar">Hand-picked gifts for the men in your life. Free to read, no account needed.</div>
<header class="hd">
  <a class="logo" href="/" aria-label="SlateCliff home">SLATECLIFF</a>
  <nav aria-label="Primary"><ul>{nav}</ul></nav>
</header>
<main id="main">
{body}
</main>
<footer class="ft">
  <div class="ft-in">
    <div><p class="logo sm">SLATECLIFF</p><p class="muted">{TAG}<br>A small, opinionated gift guide.</p></div>
    <div><p class="eyebrow">Guides</p><ul>{''.join(f'<li><a href="/guides/{g["slug"]}/">{e(g["short"])}</a></li>' for g in D["guides"][:5])}</ul></div>
    <div><p class="eyebrow">More</p><ul>{''.join(f'<li><a href="/guides/{g["slug"]}/">{e(g["short"])}</a></li>' for g in D["guides"][5:])}</ul></div>
    <div><p class="eyebrow">SlateCliff</p><ul><li><a href="/about/">About &amp; how we choose</a></li><li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="mailto:hello@slatecliff.com">Contact</a></li></ul></div>
  </div>
  <p class="fine">SlateCliff is not a store. We link to merchants and may earn a commission on purchases. Prices were checked {CHECKED} and may change. &copy; 2026 SlateCliff.</p>
</footer>
</body>
</html>'''

def newsletter():
    return '''<section class="news" aria-labelledby="news-h">
  <p class="eyebrow">The Short List</p>
  <h2 id="news-h">A newsletter is coming soon.</h2>
  <p>A short note before each gift season with new picks and shipping cutoffs. We aren't collecting sign-ups on the site yet. If you'd like a heads-up when it launches, email us and we'll add you by hand.</p>
  <a class="btn ghost" href="mailto:hello@slatecliff.com?subject=Add%20me%20to%20The%20Short%20List">Email to join the list</a>
</section>'''

def card(g):
    ps = [P[i] for i in g['picks']]
    lo, hi = min(p['price'] for p in ps), max(p['price'] for p in ps)
    return f'''<a class="gcard" href="/guides/{g['slug']}/">
  <div class="gimg" style="background:{tone(g['slug'])}"><span>{e(g['short'])}</span></div>
  <p class="eyebrow">{len(ps)} picks · {money(lo)}–{money(hi)}</p>
  <h3>{e(g['title'])}</h3>
</a>'''

def tile(p):
    return f'<div class="pimg" style="background:{tone(p["id"])}" aria-hidden="true"><span class="pm">{e(p["merchant"])}</span><span class="pn">{e(p["name"])}</span></div>'

def write(path, s):
    f = os.path.join(ROOT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(ROOT, path.strip('/'))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w').write(s)

G = D['guides']; BY = {g['slug']: g for g in G}
DISC = f'<p class="ftc"><strong>Disclosure:</strong> SlateCliff may earn a commission if you buy through links on this page, at no extra cost to you. <a href="/affiliate-disclosure/">Learn more</a>.</p>'

# Guides
for g in G:
    ps = [P[i] for i in g['picks']]
    items = ''
    for n, p in enumerate(ps, 1):
        note = '<p class="note">Manufacturer-refurbished unit.</p>' if p.get('note') else ''
        items += f'''<li class="pick" id="{e(p['id'])}">
  {tile(p)}
  <div class="pbody">
    <p class="eyebrow">{n:02d} · {e(p['merchant'])}</p>
    <h2>{e(p['name'])}</h2>
    <p class="price">{money(p['price'])} <span>as of {CHECKED}; prices may change</span></p>
    <p>{e(p['why'])}</p>{note}
    <a class="btn" href="{e(link(p))}" target="_blank" rel="sponsored nofollow noopener">Buy at {e(p['merchant'])}<span class="sr"> (opens in a new tab)</span></a>
  </div>
</li>'''
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": g['title'], "url": f"{SITE}/guides/{g['slug']}/", "numberOfItems": len(ps),
          "itemListElement": [{"@type": "ListItem", "position": n, "name": p['name'], "url": link(p)} for n, p in enumerate(ps, 1)]}
    head = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    others = ''.join(card(BY[s]) for s in [x['slug'] for x in G if x['slug'] != g['slug']][:3])
    body = f'''{DISC}
<section class="ghero">
  <p class="eyebrow"><a href="/guides/">Guides</a> / {e(g['short'])}</p>
  <h1>{e(g['title'])}</h1>
  <p class="lede">{e(g['intro'])}</p>
  <p class="muted small">{len(ps)} picks · Prices checked {CHECKED} · Every link goes straight to the merchant.</p>
</section>
<ol class="picks">{items}</ol>
{newsletter()}
<section class="wrap"><p class="eyebrow">Keep browsing</p><div class="ggrid">{others}</div></section>'''
    desc = g['intro'][:155].rsplit(' ', 1)[0] + '…'
    write(f"/guides/{g['slug']}/", page(f"/guides/{g['slug']}/", f"{g['title']} | SlateCliff", desc, body, head, 'article'))

# Guides index
def section(id_, label, opts, key):
    rows = ''
    for k, t in opts:
        gs = [g for g in G if g[key] == k] + [BY[s] for s in (GUY_EXTRA.get(k, []) if key == 'guy' else [])]
        if not gs: continue
        rows += f'<h3 class="subh" id="{key}-{k}">{e(t)}</h3><ul class="list">' + ''.join(f'<li><a href="/guides/{x["slug"]}/">{e(x["title"])}</a></li>' for x in gs) + '</ul>'
    return f'<section class="wrap idx" id="{id_}"><p class="eyebrow">Browse</p><h2>{label}</h2>{rows}</section>'
body = f'''<section class="ghero"><p class="eyebrow">All guides</p><h1>The guides</h1><p class="lede">Ten short lists, each built around one kind of guy or one occasion. No 100-item roundups.</p></section>
<section class="wrap"><div class="ggrid">{''.join(card(g) for g in G)}</div></section>
{section('occasion', 'By occasion', OCC, 'occasion')}{section('budget', 'By budget', BUD, 'budget')}{section('guy', 'By type of guy', GUY, 'guy')}
{newsletter()}'''
write('/guides/', page('/guides/', 'All Gift Guides for Him | SlateCliff', 'Every SlateCliff gift guide for him, by occasion, budget, and type of guy. Short, curated lists that link straight to the maker.', body))

# Home
feat = ['first-christmas-gifts-new-boyfriend', 'stocking-stuffers-under-30', 'coffee-gifts-for-dad', 'cozy-winter-gifts-for-him']
def chips(opts, key):
    return ''.join(f'<li><a href="/guides/#{key}-{k}">{e(t)}</a></li>' for k, t in opts if any(g[key] == k for g in G) or (key == 'guy' and k in GUY_EXTRA))
body = f'''<section class="hero">
  <div class="hero-img" aria-hidden="true"></div>
  <div class="hero-txt">
    <p class="eyebrow">Gift guides for the men in your life</p>
    <h1>{TAG}</h1>
    <p class="lede">Short, curated lists for husbands, boyfriends, dads, and the guy who's impossible to shop for. Well-made things from makers we trust, with real prices.</p>
    <a class="btn" href="/guides/">Browse the guides</a>
  </div>
</section>
<section class="wrap"><div class="row-h"><h2>Featured guides</h2><a class="more" href="/guides/">View all</a></div><div class="ggrid">{''.join(card(BY[s]) for s in feat)}</div></section>
<section class="wrap browse">
  <div><p class="eyebrow">Browse by</p><h2>Occasion</h2><ul class="chips">{chips(OCC, 'occasion')}</ul></div>
  <div><p class="eyebrow">Browse by</p><h2>Budget</h2><ul class="chips">{chips(BUD, 'budget')}</ul></div>
  <div><p class="eyebrow">Browse by</p><h2>Type of guy</h2><ul class="chips">{chips(GUY, 'guy')}</ul></div>
</section>
<section class="wrap how">
  <div><p class="eyebrow">01</p><h3>Short lists</h3><p>Each guide has roughly ten picks, not a hundred. Fewer, better choices.</p></div>
  <div><p class="eyebrow">02</p><h3>Real makers</h3><p>Every link goes straight to an established merchant, not a reseller or a dropshipper.</p></div>
  <div><p class="eyebrow">03</p><h3>Honest prices</h3><p>We checked every price on {CHECKED}. Prices change, so confirm at checkout.</p></div>
</section>
{newsletter()}'''
write('/', page('/', "SlateCliff | Small gifts he'll actually keep", 'Curated gift guides for the men in your life: husbands, boyfriends, dads. Short lists of well-made gifts from trusted makers, by occasion, budget, and type of guy.', body))

# Static pages
def simple(path, title, desc, h1, html_body):
    write(path, page(path, title + ' | SlateCliff', desc, f'<section class="ghero"><h1>{h1}</h1></section><article class="prose">{html_body}</article>'))
simple('/about/', 'About & How We Choose', 'What SlateCliff is, who it is for, and how we choose the gifts in our guides.', 'About SlateCliff', f'''
<p class="lede">SlateCliff is a small gift guide for women buying for the men in their lives: husbands, boyfriends, dads, fathers-in-law, brothers.</p>
<p>Most gift lists are endless roundups. We'd rather give you a short list of well-made things for one specific guy or one specific occasion, say plainly who each one suits, and send you straight to the maker.</p>
<h2>How we choose</h2>
<ul><li>Every pick comes from an established merchant with reliable shipping. We don't list dropshipped items.</li>
<li>We favor things he'll use and keep over novelty gifts.</li>
<li>We checked every price and link on {CHECKED}. Prices change, so the merchant's checkout is always the final word.</li>
<li>Our descriptions are our own opinions about who a gift suits. We don't publish made-up reviews, ratings, or statistics.</li>
<li>When a product is refurbished, we say so.</li></ul>
<h2>How we make money</h2>
<p>Some links may earn us a commission, at no extra cost to you. That never decides what goes on a list. See our <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p>
<h2>Contact</h2><p>Email <a href="mailto:hello@slatecliff.com">hello@slatecliff.com</a>.</p>''')
simple('/affiliate-disclosure/', 'Affiliate Disclosure', 'How SlateCliff makes money and how affiliate links work on this site.', 'Affiliate disclosure', f'''
<p class="lede">SlateCliff is reader-supported. When you buy something through a link on our site, we may earn a commission from the merchant, at no extra cost to you.</p>
<p>This disclosure is provided in line with the U.S. Federal Trade Commission's guidance on endorsements. Links to merchants on SlateCliff may be affiliate links, and we mark them as sponsored links in our code.</p>
<ul><li>Commissions never change the price you pay.</li>
<li>Merchants don't pay to be included, and they don't review or approve our picks.</li>
<li>We aren't a store. Orders, shipping, returns, and warranties are handled by the merchant you buy from.</li>
<li>Prices on our pages were checked on the date shown ({CHECKED}) and may have changed since then.</li></ul>
<p>Questions? Email <a href="mailto:hello@slatecliff.com">hello@slatecliff.com</a>.</p>''')
simple('/privacy/', 'Privacy Policy', 'SlateCliff privacy policy: what we collect (very little) and how links to merchants work.', 'Privacy', f'''
<p class="lede">Short version: SlateCliff doesn't ask for your personal information, doesn't use accounts, and doesn't run advertising trackers.</p>
<h2>What we collect</h2>
<p>The site is static pages hosted on GitHub Pages. GitHub may log standard technical information, such as IP addresses, to operate and secure its service. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub's privacy statement</a>. We don't currently run analytics or set cookies of our own.</p>
<h2>Newsletter</h2>
<p>We don't collect newsletter sign-ups on the site yet. If you email us to join, we use your address only to send the newsletter, and you can ask us to remove it at any time.</p>
<h2>Merchant links</h2>
<p>When you click through to a merchant, that merchant's own privacy policy applies, along with any affiliate network involved. Those parties may use cookies to credit a purchase.</p>
<h2>Changes and contact</h2>
<p>If this policy changes, we'll update this page. Last updated {CHECKED}. Questions: <a href="mailto:hello@slatecliff.com">hello@slatecliff.com</a>.</p>''')
write('/404.html', page('/404.html', 'Page not found | SlateCliff', 'Page not found.', '<section class="ghero"><h1>Page not found</h1><p class="lede">That page doesn\'t exist. <a href="/guides/">Browse the guides</a> instead.</p></section>'))

# sitemap / robots
urls = ['/', '/guides/'] + [f"/guides/{g['slug']}/" for g in G] + ['/about/', '/affiliate-disclosure/', '/privacy/']
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>2026-10-12</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('built', len(urls), 'pages')
