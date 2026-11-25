#!/usr/bin/env python3
"""Small Hours · genera il sito statico in dist/.

Uso:  python3 tools/build.py
Legge site.config.json, i18n/*.json, games/*/manifest.json e il design system.
Nessuna dipendenza esterna.
"""
import json, shutil, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
CFG = json.loads((ROOT / "site.config.json").read_text())
LANGS = {l: json.loads((ROOT / f"i18n/{l}.json").read_text()) for l in ("it", "en")}

# ---------- giochi ----------
games, soon = [], []
for m in sorted(ROOT.glob("games/*/manifest.json")):
    g = json.loads(m.read_text())
    if g.get("status") == "live":
        games.append(g)
for m in sorted(ROOT.glob("games/*.json")):
    g = json.loads(m.read_text())
    if g.get("status") == "soon":
        soon.append(g)
games.sort(key=lambda g: g.get("order", 99))
soon.sort(key=lambda g: g.get("order", 99))

e = html.escape


def t(L, key, **kw):
    s = LANGS[L][key]
    for k, v in kw.items():
        s = s.replace("{" + k + "}", str(v))
    return s


def url(L, page, slug=None):
    """Percorso relativo alla radice del sito, senza / iniziale."""
    p = LANGS[L]["paths"][page]
    parts = [L] + ([p] if p else []) + ([slug] if slug else [])
    return "/".join(parts) + "/index.html"


def depth_of(path):
    return path.count("/")


ICON = {
    "games": '<rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="7" height="7" rx="2"/><rect x="13" y="13" width="7" height="7" rx="2"/>',
    "daily": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "progress": '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
}


def moons(n, label):
    return f'<span class="moons" aria-label="{e(label)} {n}/5">{"●" * n}<span class="off">{"●" * (5 - n)}</span></span>'


def badge(kind, text):
    return f'<span class="badge badge--{kind}">{e(text)}</span>'


def page(L, path, title, body, *, key, slug=None, tab=None, desc=None, game=None, bare=False, og=None):
    """Una pagina completa. path = percorso relativo della cartella (es. 'it/giochi/x/')."""
    R = "../" * depth_of(path)
    other = LANGS[L]["other"]
    alt = url(other, key, slug)
    desc = desc or t(L, "tagline")
    og = og or "assets/brand/og-1200x630.jpg"
    data_game = f' data-game="{game}"' if game else ""
    head = f"""<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#07080b">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{R}{og}">
<link rel="alternate" hreflang="{other}" href="{R}{alt}">
<link rel="icon" type="image/png" href="{R}assets/brand/favicon-32.png">
<link rel="apple-touch-icon" href="{R}assets/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/tokens.css">
<link rel="stylesheet" href="{R}assets/css/components.css">
<link rel="stylesheet" href="{R}assets/css/site.css">
</head>
<body{data_game} data-root="{R}" data-lang="{L}" data-page="{key}">
"""
    if bare:
        return head + body + feedback_sheet(L) + script(L, R) + "</body>\n</html>\n"
    top = f"""<header class="topbar{' topbar--over' if key == 'home' else ''}">
  <a class="logo" href="{R}{url(L, 'home')}"><img class="logo__mark" src="{R}assets/brand/mark-96.webp" alt="">Small Hours</a>
  <div class="lang" role="group" aria-label="Language">
    <a role="button" aria-pressed="{str(L == 'it').lower()}" href="{R}{url('it', key, slug)}" data-setlang="it">IT</a>
    <a role="button" aria-pressed="{str(L == 'en').lower()}" href="{R}{url('en', key, slug)}" data-setlang="en">EN</a>
  </div>
</header>
"""
    tabs = '<nav class="tabbar" aria-label="Small Hours">'
    for k, page_key in (("games", "home"), ("daily", "daily"), ("progress", "progress")):
        cur = ' aria-current="page"' if tab == k else ""
        tabs += f'<a href="{R}{url(L, page_key)}"{cur}><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">{ICON[k]}</svg>{t(L, "nav." + k)}</a>'
    tabs += "</nav>\n"
    foot = f"""<footer class="foot">
  <a href="{R}{url(L, 'about')}">{t(L, 'footer.about')}</a>
  <button type="button" class="linklike" data-feedback>{t(L, 'footer.feedback')}</button>
  <span>© Small Hours</span>
</footer>
"""
    return head + top + f'<main class="page">\n{body}\n{foot}</main>\n' + tabs + feedback_sheet(L) + script(L, R) + "</body>\n</html>\n"


def feedback_sheet(L):
    return f"""<div class="sheet-backdrop" data-sheet="fb" hidden></div>
<div class="sheet" data-sheet="fb" role="dialog" aria-modal="true" aria-labelledby="fbT" hidden>
  <div class="sheet__grip"></div>
  <h2 class="t-h2" id="fbT">{t(L, 'fb.title')}</h2>
  <p class="t-small" style="margin:6px 0 14px">{t(L, 'fb.body')}</p>
  <label class="field"><span class="sr-only">{t(L, 'fb.title')}</span>
    <textarea class="input textarea" id="fbText" rows="5" placeholder="{e(t(L, 'fb.placeholder'))}"></textarea></label>
  <p class="t-small" id="fbMsg" role="status" style="min-height:20px;margin:8px 0"></p>
  <div class="stack" style="gap:var(--sp-2)">
    <button type="button" class="btn btn--primary btn--lg btn--block" id="fbSend">{t(L, 'fb.send') if CFG.get('feedbackEmail') else t(L, 'fb.copy')}</button>
    <button type="button" class="btn btn--ghost btn--block" data-close>{t(L, 'fb.later')}</button>
  </div>
</div>
"""


def script(L, R):
    data = {
        "lang": L,
        "root": R,
        "launch": CFG["launch"],
        "email": CFG.get("feedbackEmail", ""),
        "games": [{"slug": g["slug"], "title": g["title"][L], "minutes": g["minutes"], "chapters": g.get("chapters", 0),
                   "play": url(L, "play", g["slug"]), "page": url(L, "game", g["slug"])} for g in games],
        "t": {k: LANGS[L][k] for k in ("home.today", "fb.copied", "progress.resetConfirm", "game.chapter", "days", "daily.body", "daily.eyebrow", "game.stars")},
    }
    return f'<script>window.SH={json.dumps(data, ensure_ascii=False)};</script>\n<script src="{R}assets/js/site.js"></script>\n'


def trial_card(L):
    if CFG.get("payments"):
        return ""
    return f"""<section class="trial">
  <div><p class="t-caps" style="color:var(--lamp-300)">{t(L, 'trial.title')}</p>
  <p class="t-body" style="margin-top:4px">{t(L, 'trial.body')}</p></div>
  <button type="button" class="btn btn--secondary" data-feedback>{t(L, 'trial.cta')}</button>
</section>"""


def game_card(L, g, R):
    b = []
    if g.get("new"):
        b.append(badge("new", t(L, "badge.new")))
    b.append(badge("free", t(L, "badge.free")))
    if L not in g.get("lang", ["it", "en"]):
        b.append(badge("soon", t(L, "badge.itonly")))
    return f"""<a class="game-card" data-game="{g['slug']}" href="{R}{url(L, 'game', g['slug'])}">
  <img class="game-card__art" src="{R}games/{g['slug']}/cover.webp" alt="" loading="lazy">
  <div class="game-card__shade"></div>
  <div class="game-card__top">{''.join(b)}</div>
  <div class="game-card__body">
    <h3 class="game-card__title">{e(g['title'][L])}</h3>
    <p class="game-card__hook">{e(g['hook'][L])}</p>
    <div class="meta"><span>◷ {g['minutes'][0]}–{g['minutes'][1]} {t(L, 'game.min')}</span>{moons(g['difficulty'], t(L, 'game.diff'))}</div>
  </div>
</a>"""


def build_lang(L):
    out = []
    # HOME
    path = url(L, "home")
    R = "../" * depth_of(path)
    feat = games[0]
    body = f"""<section class="hero hero--art">
  <span class="t-caps" data-today></span>
  <h1 class="t-title">{t(L, 'home.title1')}<br><span class="t-italic" style="color:var(--lamp-300)">{t(L, 'home.title2')}</span></h1>
  <a class="btn btn--primary btn--lg btn--block" data-featured href="{R}{url(L, 'play', feat['slug'])}">{t(L, 'home.cta')}</a>
  <span class="t-small" style="text-align:center" data-featured-text>{t(L, 'home.today', game=e(feat['title'][L]), min=feat['minutes'][1])}</span>
</section>
{trial_card(L)}
<section class="section" data-continue hidden>
  <div class="section__head"><h2 class="t-h2">{t(L, 'home.continue')}</h2></div>
  <div class="stack" data-continue-list></div>
</section>
<section class="section">
  <div class="section__head"><h2 class="t-h2">{t(L, 'home.games')}</h2><span class="t-small">{len(games)}</span></div>
  {''.join(game_card(L, g, R) for g in games)}
</section>"""
    if soon:
        body += f"""<section class="section"><div class="section__head"><h2 class="t-h2">{t(L, 'home.soon')}</h2></div>
  {''.join(f'<div class="game-card game-card--soon soon-card"><span class="badge badge--soon">{t(L, "badge.soon")}</span><p class="t-h2">{e(s["title"][L])}</p></div>' for s in soon)}
</section>"""
    out.append((path, page(L, path, f"Small Hours · {t(L, 'tagline')}", body, key="home", tab="games")))

    # GIOCHI: scheda + gioca
    for g in games:
        s = g["slug"]
        path = url(L, "game", s)
        R = "../" * depth_of(path)
        itonly = L not in g.get("lang", ["it", "en"])
        badges = (badge("new", t(L, "badge.new")) if g.get("new") else "") + badge("free", t(L, "badge.free")) + (badge("soon", t(L, "badge.itonly")) if itonly else "")
        body = f"""<div class="game-hero">
  <img src="{R}games/{s}/key.webp" alt="">
  <a class="btn btn--icon game-hero__back" href="{R}{url(L, 'home')}" aria-label="{t(L, 'game.back')}">←</a>
</div>
<div class="stack game-head">
  <div style="display:flex;gap:8px;flex-wrap:wrap">{badges}</div>
  <h1 class="t-title" style="font-size:40px">{e(g['title'][L])}</h1>
  <p class="t-lead">{e(g['lead'][L])}</p>
  <div class="meta"><span>◷ {g['minutes'][0]}–{g['minutes'][1]} {t(L, 'game.min')}</span><span>{t(L, 'game.diff')} {moons(g['difficulty'], t(L, 'game.diff'))}</span></div>
  <a class="btn btn--primary btn--lg btn--block" href="{R}{url(L, 'play', s)}">{t(L, 'game.play')}</a>
</div>
<section class="section"><h2 class="t-h2">{t(L, 'game.howto')}</h2>
  <ul class="checklist" style="margin:0">{''.join(f'<li>{e(x)}</li>' for x in g['howto'][L])}</ul></section>
<section class="section"><h2 class="t-h2">{t(L, 'game.campaign')}</h2><p class="t-body">{e(g['campaign'][L])}</p></section>
<section class="section"><h2 class="t-h2">{t(L, 'game.yours')}</h2><div data-mine="{s}" class="t-body">{t(L, 'game.none')}</div></section>
{trial_card(L)}"""
        out.append((path, page(L, path, f"{g['title'][L]} · Small Hours", body, key="game", slug=s, tab="games", desc=g["hook"][L], game=s, og=f"games/{s}/cover.webp")))

        path = url(L, "play", s)
        R = "../" * depth_of(path)
        body = f"""<div class="play">
  <div class="play__bar">
    <button type="button" class="play__exit" aria-label="{t(L, 'play.exit')}" data-exit><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <span class="play__title">{e(g['title'][L])}</span>
    <button type="button" class="play__fb" data-feedback>{t(L, 'trial.cta')}</button>
  </div>
  <iframe class="play__frame" src="{R}games/{s}/index.html?play" title="{e(g['title'][L])}" allow="clipboard-write"></iframe>
</div>
<div class="sheet-backdrop" data-sheet="exit" hidden></div>
<div class="sheet" data-sheet="exit" role="dialog" aria-modal="true" aria-labelledby="exT" hidden>
  <div class="sheet__grip"></div>
  <h2 class="t-h2" id="exT">{t(L, 'play.exitTitle')}</h2>
  <p class="t-body" style="margin:var(--sp-2) 0 var(--sp-5)">{t(L, 'play.exitBody')}</p>
  <div class="stack" style="gap:var(--sp-2)">
    <button type="button" class="btn btn--primary btn--lg btn--block" data-close>{t(L, 'play.stay')}</button>
    <a class="btn btn--secondary btn--block" href="{R}{url(L, 'game', s)}">{t(L, 'play.leave')}</a>
  </div>
</div>"""
        out.append((path, page(L, path, f"{g['title'][L]} · Small Hours", body, key="play", slug=s, game=s, bare=True)))

    # SFIDA
    path = url(L, "daily")
    R = "../" * depth_of(path)
    rows = "".join(f"""<a class="row-card" data-game="{g['slug']}" href="{R}{url(L, 'play', g['slug'])}">
  <img src="{R}games/{g['slug']}/icon.webp" alt="">
  <div><p class="row-card__title">{e(g['title'][L])}</p><div class="t-small">{g['minutes'][0]}–{g['minutes'][1]} {t(L, 'game.min')}</div></div>
  <span class="btn btn--primary">{t(L, 'daily.play')}</span></a>""" for g in games)
    body = f"""<div class="stack" style="margin-top:var(--sp-4)">
  <span class="t-caps" data-daily-n></span>
  <h1 class="t-title">{t(L, 'daily.title')}</h1>
  <p class="t-small" data-countdown></p>
</div>
<section class="section">{rows}</section>
<p class="t-small" style="margin-top:var(--sp-6)">{t(L, 'daily.note')}</p>"""
    out.append((path, page(L, path, f"{t(L, 'daily.title')} · Small Hours", body, key="daily", tab="daily")))

    # PROGRESSI
    path = url(L, "progress")
    R = "../" * depth_of(path)
    rows = "".join(f"""<div class="row-card" data-game="{g['slug']}">
  <img src="{R}games/{g['slug']}/icon.webp" alt="">
  <div><p class="row-card__title">{e(g['title'][L])}</p><div class="t-small" data-mine="{g['slug']}">{t(L, 'progress.nostore') if not g.get('chapters') else t(L, 'game.none')}</div></div>
  <span class="stars" data-mine-stars="{g['slug']}"></span></div>""" for g in games)
    body = f"""<div class="stack" style="margin-top:var(--sp-4)">
  <h1 class="t-title">{t(L, 'progress.title')}</h1>
  <div style="display:flex;gap:var(--sp-8)">
    <div class="stat"><b data-total-stars>0</b><span>{t(L, 'progress.stars')}</span></div>
    <div class="stat"><b data-total-chapters>0</b><span>{t(L, 'progress.chapters')}</span></div>
  </div>
</div>
<section class="section"><h2 class="t-h2">{t(L, 'progress.games')}</h2>{rows}</section>
<section class="section"><p class="t-small">{t(L, 'progress.data')}</p>
  <button type="button" class="btn btn--ghost" style="color:var(--danger-400);justify-self:start;padding:0" data-reset>{t(L, 'progress.reset')}</button></section>"""
    out.append((path, page(L, path, f"{t(L, 'progress.title')} · Small Hours", body, key="progress", tab="progress")))

    # INFO
    path = url(L, "about")
    body = f"""<div class="stack" style="margin-top:var(--sp-4)">
  <h1 class="t-title">{t(L, 'about.title')}</h1>
  <p class="t-lead">{t(L, 'about.body')}</p>
</div>
<section class="section"><h2 class="t-h2">{t(L, 'about.privacy')}</h2><p class="t-body">{t(L, 'about.privacyBody')}</p></section>
{trial_card(L)}"""
    out.append((path, page(L, path, f"{t(L, 'footer.about')} · Small Hours", body, key="about")))
    return out


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets/css").mkdir(parents=True)
    (DIST / "assets/js").mkdir(parents=True)
    shutil.copy(ROOT / "design-system/tokens.css", DIST / "assets/css/tokens.css")
    comp = (ROOT / "design-system/components.css").read_text().replace('url("../assets/', 'url("../')
    (DIST / "assets/css/components.css").write_text(comp)
    shutil.copy(ROOT / "src/site.css", DIST / "assets/css/site.css")
    shutil.copy(ROOT / "src/site.js", DIST / "assets/js/site.js")
    shutil.copytree(ROOT / "assets/brand", DIST / "assets/brand")
    for g in games:
        shutil.copytree(ROOT / "games" / g["slug"], DIST / "games" / g["slug"])
    for L in LANGS:
        for path, doc in build_lang(L):
            f = DIST / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(doc)
    # radice: sceglie la lingua
    (DIST / "index.html").write_text("""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Small Hours</title><meta name="theme-color" content="#07080b"><style>body{background:#07080b}</style>
<script>(function(){var l;try{l=JSON.parse(localStorage.getItem('sh:v1:profile')||'{}').lang}catch(e){}
if(!l){l=(navigator.languages||[navigator.language||'en']).some(function(x){return /^it/i.test(x)})?'it':'en'}
location.replace(l+'/index.html');})();</script></head><body><a href="it/index.html">Italiano</a> · <a href="en/index.html">English</a></body></html>
""")
    (DIST / ".nojekyll").write_text("")
    n = sum(1 for _ in DIST.rglob("index.html"))
    print(f"dist/ pronto: {n} pagine, {len(games)} giochi, pagamenti {'accesi' if CFG.get('payments') else 'spenti'}")


if __name__ == "__main__":
    main()
