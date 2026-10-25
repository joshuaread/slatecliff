#!/usr/bin/env python3
"""Builds the static SlateCliff site from _src/site.json.
To swap in affiliate links: set "affiliate_url" on a product in _src/site.json, then run
    python3 _src/build.py
from the repo root and commit. Nothing else needs to change."""
import json, os, html, hashlib, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, '_src', 'site.json')))
P = {p['id']: p for p in D['products']}
SITE = 'https://slatecliff.com'
TAG = "Small gifts he'll actually keep."
CHECKED = D['price_checked']
PZ_TAG = open(os.path.join(ROOT, '_src', 'partnerize-tag.txt')).read().strip()  # Partnerize Partner Tag, inserted verbatim in every <head>
SOVRN_KEY = '607af82507781c6d11d22bd08343d171'  # Sovrn Commerce (VigLink) key; empty = no tag
SOVRN_TAG = ("<script type=\"text/javascript\"> var vglnk = {key: '" + SOVRN_KEY + "'}; (function(d, t) {var s = d.createElement(t); s.type = 'text/javascript';s.async = true; s.src = '//cdn.viglink.com/api/vglnk.js'; var r = d.getElementsByTagName(t)[0]; r.parentNode.insertBefore(s, r); }(document, 'script')); </script>\n") if SOVRN_KEY else ''
GA4_ID = 'G-LWW3X16HN4'  # Set to SlateCliff's own GA4 Measurement ID (G-XXXXXXXXXX), then rebuild. Empty = no analytics tag; privacy page says no analytics.
GA4_TAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA4_ID + '"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","' + GA4_ID + '");'
           'document.addEventListener("click",function(ev){var a=ev.target.closest&&ev.target.closest("a[href^=\'http\']");if(!a||a.hostname===location.hostname)return;gtag("event","outbound_click",{link_url:a.href,link_domain:a.hostname,transport_type:"beacon"});});</script>\n') if GA4_ID else ''
PRIV_LEDE = "uses Google Analytics only to count visits and clicks." if GA4_ID else "doesn't run analytics."
PRIV_GA = ('We use Google Analytics 4 to count page views and clicks to merchant sites, so we know which guides are useful. Google Analytics sets first-party cookies and receives standard technical information such as your IP address, browser, and pages visited. See <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">how Google uses information from sites that use its services</a>. You can opt out with <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google\'s opt-out browser add-on</a>.') if GA4_ID else "We don't currently run analytics or set cookies of our own."
e = html.escape
OCC = [('christmas', 'Christmas'), ('anniversary', 'Anniversary'), ('birthday', 'Birthday'), ('fathers-day', "Father's Day")]
BUD = [('under-30', 'Under $30'), ('under-100', 'Under $100'), ('under-150', 'Under $150'), ('splurge', 'Worth the splurge')]
GUY = [('husband', 'Husband'), ('boyfriend', 'Boyfriend'), ('dad', 'Dad & father-in-law'), ('coffee', 'Coffee guy'), ('edc', 'Everyday-carry guy'), ('handy', 'Handy guy'), ('bourbon', 'Bourbon guy'), ('outdoors', 'Outdoors guy')]
GUY_EXTRA = {'husband': ['gifts-for-handy-husband'], 'boyfriend': ['edc-gifts-for-boyfriend'], 'dad': ['coffee-gifts-for-dad']}
TONES = ['#e9e5de', '#e2ddd4', '#dcd6cc', '#ece9e3', '#d9d4cb', '#e6e1d8']

_hp = P['maritime-shirt-jacket-in-heather-olive-wool-2610']
HOME_OG = (_hp['image'], f"{_hp['name']}, product photo from {_hp['merchant']}")
def tone(s): return TONES[int(hashlib.md5(s.encode()).hexdigest(), 16) % len(TONES)]
def money(v): return f"${v:,.2f}".replace('.00', '')
def link(p): return p.get('affiliate_url') or p['url']

def page(path, title, desc, body, extra_head='', og_type='website', og_img=None, og_alt=''):
    url = SITE + path
    og_img = og_img or HOME_OG[0]; og_alt = og_alt or HOME_OG[1]
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
<meta property="og:image" content="{e(img_src(og_img, 1200))}">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:image" content="{e(img_src(og_img, 1200))}">
<meta name="twitter:image:alt" content="{e(og_alt)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
{PZ_TAG}
<meta name='impact-site-verification' value='73259207-b5dd-481c-9738-ac3da54c5be4'>
{GA4_TAG}{extra_head}
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
    <div><p class="eyebrow">SlateCliff</p><ul><li><a href="/about/">About &amp; how we choose</a></li><li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/contact/">Contact</a></li></ul></div>
  </div>
  <p class="fine">SlateCliff is not a store. We link to merchants and may earn a commission on purchases. Prices were checked {CHECKED} and may change. &copy; 2026 SlateCliff.</p>
</footer>
{SOVRN_TAG}</body>
</html>'''

def newsletter():
    return '''<section class="news" aria-labelledby="news-h">
  <p class="eyebrow">The Short List</p>
  <h2 id="news-h">Get a note before each gift season.</h2>
  <p>A short email before the holidays and other gift seasons with new picks and shipping cutoffs. Email us and we'll add you to the list by hand; ask any time and we'll take you off.</p>
  <a class="btn ghost" href="mailto:hello@slatecliff.com?subject=Add%20me%20to%20The%20Short%20List">Email to join the list</a>
</section>'''

def order(g): return [P[i] for i in (g['best']['order'] if g.get('best') else g['picks'])]
def lead(g): return order(g)[0]
def alt(p): return f"{p['name']}, product photo from {p['merchant']}"
def im(p, w, sizes, lazy=True, cls='', alt_txt=None, hi=False):
    u = p['image']
    a = alt(p) if alt_txt is None else alt_txt
    ld = 'loading="lazy" ' if lazy else ('fetchpriority="high" ' if hi else '')
    return (f'<img{" class=" + chr(34) + cls + chr(34) if cls else ""} src="{e(img_src(u, w))}" srcset="{e(img_src(u, 300))} 300w, {e(img_src(u, 600))} 600w, {e(img_src(u, 900))} 900w" '
            f'sizes="{sizes}" width="{w}" height="{w}" {ld}decoding="async" alt="{e(a)}">')
def collage(ps, sizes, lazy=True, hi=False):
    a, b, c = ps[:3]
    return (f'<div class="clg">{im(a, 600, sizes, lazy, "c1", hi=hi)}{im(b, 300, "(max-width:640px) 45vw, 12vw", lazy, "c2")}{im(c, 300, "(max-width:640px) 45vw, 12vw", lazy, "c3")}</div>')

def card(g, lazy=True):
    ps = [P[i] for i in g['picks']]
    lo, hi = min(p['price'] for p in ps), max(p['price'] for p in ps)
    return f'''<a class="gcard" href="/guides/{g['slug']}/">
  <div class="gimg has-img">{collage(order(g), "(max-width:900px) 46vw, 22vw", lazy)}</div>
  <p class="eyebrow">{len(ps)} picks · {money(lo)}–{money(hi)}</p>
  <h3>{e(g['title'])}</h3>
</a>'''

def img_src(u, w):
    return u + ('&' if '?' in u else '?') + f'width={w}'

def tile(p):
    if p.get('image'):
        u = p['image']
        return (f'<div class="pimg has-img" style="background:#fff"><img src="{e(img_src(u, 800))}" '
                f'srcset="{e(img_src(u, 400))} 400w, {e(img_src(u, 800))} 800w, {e(img_src(u, 1200))} 1200w" '
                f'sizes="(max-width:640px) 92vw, 46vw" width="800" height="800" loading="lazy" decoding="async" '
                f'alt="{e(p["name"])}, product photo from {e(p["merchant"])}"></div>')
    return f'<div class="pimg" style="background:{tone(p["id"])}" aria-hidden="true"><span class="pm">{e(p["merchant"])}</span><span class="pn">{e(p["name"])}</span></div>'

def write(path, s):
    f = os.path.join(ROOT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(ROOT, path.strip('/'))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    s = re.sub(r'<a ([^>]*href="https://www\.awin1\.com[^"]*"[^>]*)>', lambda m: '<a ' + (m.group(1).replace('class="', 'class="norewrite ', 1) if 'class="' in m.group(1) else 'class="norewrite" ' + m.group(1)) + '>', s)  # keep direct AWIN links out of Sovrn rewriting
    open(f, 'w').write(s)

G = D['guides']; BY = {g['slug']: g for g in G}
TRUST = f'<ul class="trust" aria-label="Why you can trust this list"><li>Hand-picked; merchants can&#x27;t pay to be listed</li><li>Prices checked {CHECKED}</li><li>Links go straight to the merchant</li><li><a href="/affiliate-disclosure/">We may earn a commission</a> · <a href="/about/">How we pick</a></li></ul>'
DISC = f'<p class="ftc"><strong>Disclosure:</strong> SlateCliff may earn a commission if you buy through links on this page, at no extra cost to you. <a href="/affiliate-disclosure/">Learn more</a>.</p>'

def strip(ps, lazy=True, n=None):
    return '<div class="strip">' + ''.join(f'<figure>{im(p, 600, "(max-width:640px) 31vw, 300px", lazy, hi=(not lazy and k==0))}</figure>' for k, p in enumerate(ps)) + '</div>'


from datetime import datetime
def iso(d): return datetime.strptime(d, '%B %d, %Y').date().isoformat()
def guide_ld(g, ps):
    """Structured data for AI Overviews / rich results. Only facts already on the page: no ratings or reviews."""
    url = f"{SITE}/guides/{g['slug']}/"; b = g.get('best') or {}
    name = b.get('h1', g['title']); ordered = order(g)
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "SlateCliff", "url": SITE + "/"}
    items = [{"@type": "ListItem", "position": n, "url": f"{url}#{p['id']}", "name": p['name'],
              "image": img_src(p['image'], 1200) if p.get('image') else None} for n, p in enumerate(ordered, 1)]
    for it in items:
        if not it['image']: del it['image']
    graph = [org,
        {"@type": "Article", "@id": url + "#article", "headline": name, "url": url, "mainEntityOfPage": url,
         "datePublished": iso(b.get('published', CHECKED)), "dateModified": iso(b.get('updated', CHECKED)),
         "author": org, "publisher": org, "image": img_src(ordered[0]['image'], 1200), "about": {"@id": url + "#list"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": g['short'], "item": url}]},
        {"@type": "ItemList", "@id": url + "#list", "name": name, "url": url, "numberOfItems": len(ordered),
         "itemListOrder": "https://schema.org/ItemListOrderAscending", "itemListElement": items}]
    if b.get('faq'):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in b['faq']]})
    return {"@context": "https://schema.org", "@graph": graph}

# "Best X" playbook layout (used when a guide has a "best" block)
def best_body(g):
    b = g['best']; ps = [P[i] for i in b['order']]; top = ps[0]
    crit = ''.join(f'<li><strong>{e(k)}:</strong> {e(v)}</li>' for k, v in b['criteria'])
    items = ''
    for n, p in enumerate(ps, 1):
        note = '<p class="note">Manufacturer-refurbished unit.</p>' if p.get('note') else ''
        items += f'''<li class="pick" id="{e(p['id'])}">
  {tile(p)}
  <div class="pbody">
    <p class="eyebrow">{e(p['merchant'])}</p>
    <h3>{n}. {e(p['name'])}, best for {e(b['best_for'][p['id']])}</h3>
    <p class="price">{money(p['price'])} <span>as of {CHECKED}; prices may change</span></p>
    <p>{e(p['why'])}</p>
    <p><strong>Best suited for:</strong> {e(b['best_for'][p['id']][0].upper() + b['best_for'][p['id']][1:])}. {e(b['dim'])}: {e(b['table'][p['id']][0].lower())}; used {e(b['table'][p['id']][1].lower())}.</p>{note}
    <a class="btn" href="{e(link(p))}" target="_blank" rel="sponsored nofollow noopener">Buy at {e(p['merchant'])}<span class="sr"> (opens in a new tab)</span></a>
  </div>
</li>'''
    rows = ''.join(f'<tr><td>{n}</td><td><a href="#{e(p["id"])}">{e(p["name"])}</a></td><td>{money(p["price"])}</td>' + ''.join(f'<td>{e(c)}</td>' for c in b['table'][p['id']]) + '</tr>' for n, p in enumerate(ps, 1))
    uc = ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in r) + '</tr>' for r in b['usecase'])
    faq = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in b['faq'])
    return f'''{DISC}
<section class="ghero">
  <p class="eyebrow"><a href="/guides/">Guides</a> / {e(g['short'])}</p>
  <h1>{e(b['h1'])}</h1>
  <p class="dek">Skip the guesswork: {len(ps)} well-made gifts he'll actually use, ranked, with the one we'd buy first right up top.</p>
  <p class="muted small">By the SlateCliff editors · <a href="/about/">How we choose</a> · Published <time datetime="{iso(b.get('published', CHECKED))}">{e(b.get('published', CHECKED))}</time> · Updated <time datetime="{iso(b['updated'])}">{e(b['updated'])}</time></p>
  <p class="lede">{e(b['intro'])}</p>
  <p class="cta1"><span class="eyebrow">Our #1 pick</span><a class="btn" href="{e(link(top))}" target="_blank" rel="sponsored nofollow noopener">Get the {e(top['name'])}: {money(top['price'])} at {e(top['merchant'])}<span class="sr"> (opens in a new tab)</span></a></p>
  {TRUST}
  {strip(ps[:3], lazy=False)}
</section>
<article class="prose">
<h2>Key takeaways</h2><ul>{''.join(f'<li>{e(t)}</li>' for t in b['takeaways'])}</ul>
<h2>{e(b['whatis_h'])}</h2>{''.join(f'<p>{e(t)}</p>' for t in b['whatis'])}
<h2>How we ranked these gifts</h2><p>We ranked each pick on four criteria. We don't publish ratings, review counts, or stats we haven't verified.</p><ul>{crit}</ul>
<h2>{e(b['list_h'])}</h2><p>{e(b['list_intro'])} Every price is the maker's listed price as of {CHECKED}.</p>
</article>
<ol class="picks">{items}</ol>
<article class="prose">
<h2>Side-by-side comparison</h2><p>The same four criteria: {e(b['dim'].lower())}, price, where he uses it, and how often.</p>
<div class="tbl"><table><thead><tr><th>#</th><th>Gift</th><th>Price</th><th>{e(b['dim'])}</th><th>Where</th><th>How often</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>{e(b['fit_h'])}</h2>
<div class="tbl"><table><thead><tr><th>If he…</th><th>Get</th><th>Or</th></tr></thead><tbody>{uc}</tbody></table></div>
<h2>Frequently asked questions</h2>{faq}
<h2>Get him the #1 pick</h2><p>{e(b['cta'])} It's {money(top['price'])}. It ships straight from {e(top['merchant'])}. </p><p><a class="btn" href="{e(link(top))}" target="_blank" rel="sponsored nofollow noopener">Get the {e(top['name'])} at {e(top['merchant'])}<span class="sr"> (opens in a new tab)</span></a></p>{TRUST}
</article>'''

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
    head = f'<script type="application/ld+json">{json.dumps(guide_ld(g, ps), ensure_ascii=False)}</script>'
    others = ''.join(card(BY[s]) for s in [x['slug'] for x in G if x['slug'] != g['slug']][:3])
    body = best_body(g) + f'''
{newsletter()}
<section class="wrap"><p class="eyebrow">Keep browsing</p><div class="ggrid">{others}</div></section>''' if g.get('best') else f'''{DISC}
<section class="ghero">
  <p class="eyebrow"><a href="/guides/">Guides</a> / {e(g['short'])}</p>
  <h1>{e(g['title'])}</h1>
  <p class="lede">{e(g['intro'])}</p>
  <p class="muted small">{len(ps)} picks · Prices checked {CHECKED} · Every link goes straight to the merchant.</p>
  {strip(ps[:3], lazy=False)}
</section>
<ol class="picks">{items}</ol>
{newsletter()}
<section class="wrap"><p class="eyebrow">Keep browsing</p><div class="ggrid">{others}</div></section>'''
    desc = (g['best']['intro'] if g.get('best') else g['intro'])[:155].rsplit(' ', 1)[0] + '…'
    write(f"/guides/{g['slug']}/", page(f"/guides/{g['slug']}/", g.get('best', {}).get('title_tag') or f"{g.get('best', {}).get('h1', g['title'])} | SlateCliff", desc, body, head, 'article', lead(g)['image'], alt(lead(g))))

# Guides index
def section(id_, label, opts, key):
    rows = ''
    for k, t in opts:
        gs = [g for g in G if g[key] == k] + [BY[s] for s in (GUY_EXTRA.get(k, []) if key == 'guy' else [])]
        if not gs: continue
        rows += f'<h3 class="subh" id="{key}-{k}">{e(t)}</h3><ul class="list">' + ''.join(f'<li><a href="/guides/{x["slug"]}/">{e(x["title"])}</a></li>' for x in gs) + '</ul>'
    return f'<section class="wrap idx" id="{id_}"><p class="eyebrow">Browse</p><h2>{label}</h2>{rows}</section>'
body = f'''<section class="ghero"><p class="eyebrow">All guides</p><h1>The guides</h1><p class="lede">Ten short lists, each built around one kind of guy or one occasion. No 100-item roundups.</p></section>
<section class="wrap"><div class="ggrid">{''.join(card(g, k >= 4) for k, g in enumerate(G))}</div></section>
{section('occasion', 'By occasion', OCC, 'occasion')}{section('budget', 'By budget', BUD, 'budget')}{section('guy', 'By type of guy', GUY, 'guy')}
{newsletter()}'''
write('/guides/', page('/guides/', 'All Gift Guides for Him | SlateCliff', 'Every SlateCliff gift guide for him, by occasion, budget, and type of guy. Short, curated lists that link straight to the maker.', body, og_img=lead(G[0])['image'], og_alt=alt(lead(G[0]))))

# Home
HERO_PS = [lead(BY[s]) for s in ['cozy-winter-gifts-for-him', 'leather-anniversary-gifts', 'coffee-gifts-for-dad', 'edc-gifts-for-boyfriend']]
HERO = '<div class="hgrid">' + ''.join(im(p, 600, '(max-width:640px) 50vw, 27vw', False, hi=(k == 0)) for k, p in enumerate(HERO_PS)) + '</div><p class="hcap">Gifts he\'ll reach for every day, not stash in a drawer.</p>'
feat = ['first-christmas-gifts-new-boyfriend', 'stocking-stuffers-under-30', 'coffee-gifts-for-dad', 'cozy-winter-gifts-for-him']
def chips(opts, key):
    return ''.join(f'<li><a href="/guides/#{key}-{k}">{e(t)}</a></li>' for k, t in opts if any(g[key] == k for g in G) or (key == 'guy' and k in GUY_EXTRA))
body = f'''<section class="hero">
  <div class="hero-img has-img">{HERO}</div>
  <div class="hero-txt">
    <p class="eyebrow">{TAG}</p>
    <h1>Find a gift he'll actually use, in five minutes.</h1>
    <p class="lede">Short, ranked lists for husbands, boyfriends, dads, and the guy who's impossible to shop for. Well-made things from makers we trust, with real prices, and our #1 pick at the top of every guide.</p>
    <p><a class="btn" href="/guides/">Find his gift</a></p>
    {TRUST}
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
write('/', page('/', "SlateCliff | Small gifts he'll actually keep", 'Curated gift guides for husbands, boyfriends, and dads: short lists of well-made gifts from trusted makers, by occasion, budget, and type of guy.', body))

# Static pages
def simple(path, title, desc, h1, html_body):
    extra = strip([lead(g) for g in G[:4]], lazy=True) if path in ('/about/', '/contact/') else ''
    write(path, page(path, title + ' | SlateCliff', desc, f'<section class="ghero"><h1>{h1}</h1></section><article class="prose">{html_body}{extra}</article>'))
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
<p class="lede">Short version: SlateCliff doesn't ask for your personal information, doesn't use accounts, and {PRIV_LEDE}</p>
<h2>What we collect</h2>
<p>The site is static pages hosted on GitHub Pages. GitHub may log standard technical information, such as IP addresses, to operate and secure its service. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub's privacy statement</a>. {PRIV_GA}</p>
<h2>Affiliate tracking</h2>
<p>Our pages include the Partnerize partner tag and the Sovrn Commerce script, which helps credit purchases you make through our merchant links. We may also use other affiliate networks, such as impact.com, for merchant links. These networks and the merchants may set cookies or use similar technologies to credit a purchase. See <a href="https://partnerize.com/privacy-policy" rel="noopener">Partnerize's privacy policy</a>, <a href="https://www.sovrn.com/legal/privacy-policy/" rel="noopener">Sovrn's privacy policy</a> and <a href="https://impact.com/privacy-policy/" rel="noopener">impact.com's privacy policy</a>.</p>
<h2>Newsletter</h2>
<p>We don't collect newsletter sign-ups on the site yet. If you email us to join, we use your address only to send the newsletter, and you can ask us to remove it at any time.</p>
<h2>Merchant links</h2>
<p>When you click through to a merchant, that merchant's own privacy policy applies, along with any affiliate network involved. Those parties may use cookies to credit a purchase.</p>
<h2>Your choices</h2>
<p>You can block or clear cookies in your browser settings. To ask about or remove any email address you've sent us, write to <a href="mailto:hello@slatecliff.com">hello@slatecliff.com</a>.</p>
<h2>Changes and contact</h2>
<p>If this policy changes, we'll update this page. Last updated {CHECKED}. Questions: <a href="mailto:hello@slatecliff.com">hello@slatecliff.com</a>.</p>''')
simple('/contact/', 'Contact', 'How to reach SlateCliff: questions about a gift, a broken link, corrections, or partnership inquiries.', 'Contact', '''
<p class="lede">The best way to reach us is email: <a href="mailto:hello@slatecliff.com">hello@slatecliff.com</a>.</p>
<p>Write to us about:</p>
<ul><li>A question about a gift or a guide</li>
<li>A broken link, a price that has changed, or a correction</li>
<li>Brand and affiliate partnership inquiries</li>
<li>Joining or leaving our seasonal email list</li></ul>
<p>We read every message and usually reply within a few business days. SlateCliff isn't a store, so for orders, shipping, or returns, please contact the merchant you bought from.</p>
<p>See also: <a href="/about/">About &amp; how we choose</a> · <a href="/affiliate-disclosure/">Affiliate disclosure</a> · <a href="/privacy/">Privacy</a></p>''')
write('/404.html', page('/404.html', 'Page not found | SlateCliff', 'Page not found.', '<section class="ghero"><h1>Page not found</h1><p class="lede">That page doesn\'t exist. <a href="/guides/">Browse the guides</a> instead.</p></section><section class="wrap"><p class="eyebrow">Popular guides</p><div class="ggrid">' + ''.join(card(BY[s]) for s in ['first-christmas-gifts-new-boyfriend', 'stocking-stuffers-under-30', 'coffee-gifts-for-dad', 'cozy-winter-gifts-for-him']) + '</div></section>'))

# sitemap / robots
urls = ['/', '/guides/'] + [f"/guides/{g['slug']}/" for g in G] + ['/about/', '/contact/', '/affiliate-disclosure/', '/privacy/']
LM = {f"/guides/{g['slug']}/": iso(g.get('best', {}).get('updated', CHECKED)) for g in G}
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{LM.get(u, iso(CHECKED))}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('built', len(urls), 'pages')
