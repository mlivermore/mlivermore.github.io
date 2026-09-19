#!/usr/bin/env python3
"""Reads the freerangepodcast.org WordPress export and produces:

  content/podcast/episodes.json        structured episode data used by build.py
  content/podcast/transcripts/SxEy.html transcript fragments used by build.py
  <archive dir>/                        a complete, unstyled archive of the old
                                        site: every post and page as HTML, plus
                                        the export itself and an index

Usage: python tools/extract-podcast.py <export.xml> <archive dir>
"""
import html, json, re, sys, shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XML = Path(sys.argv[1])
ARCHIVE = Path(sys.argv[2])
NS = {"wp": "http://wordpress.org/export/1.2/", "content": "http://purl.org/rss/1.0/modules/content/"}

ch = ET.parse(XML).getroot().find("channel")
items = []
for it in ch.findall("item"):
    items.append(dict(
        title=it.findtext("title") or "",
        link=it.findtext("link") or "",
        date=(it.findtext("wp:post_date", namespaces=NS) or "")[:10],
        type=it.findtext("wp:post_type", namespaces=NS),
        status=it.findtext("wp:status", namespaces=NS),
        slug=it.findtext("wp:post_name", namespaces=NS) or "",
        content=it.findtext("content:encoded", namespaces=NS) or "",
        attachment=it.findtext("wp:attachment_url", namespaces=NS) or "",
    ))


def strip_wp(c):
    c = re.sub(r"<!--.*?-->", "", c, flags=re.S)
    c = re.sub(r"<p>\s*(&nbsp;|\s)*</p>", "", c)
    return c.strip()


# ---------- 1. full archive ----------
ARCHIVE.mkdir(parents=True, exist_ok=True)
(ARCHIVE / "pages").mkdir(exist_ok=True)
(ARCHIVE / "posts").mkdir(exist_ok=True)
shutil.copy(XML, ARCHIVE / "wordpress-export.xml")
index = []
for it in items:
    if it["type"] in ("page", "post") and it["status"] == "publish":
        folder = "posts" if it["type"] == "post" else "pages"
        name = f'{it["slug"] or re.sub(r"[^a-z0-9]+", "-", it["title"].lower())}.html'
        (ARCHIVE / folder / name).write_text(
            f'<!doctype html><meta charset="utf-8"><title>{html.escape(it["title"])}</title>\n'
            f'<h1>{html.escape(it["title"])}</h1>\n<p><small>{it["date"]} — originally at {it["link"]}</small></p>\n'
            + strip_wp(it["content"]), encoding="utf-8")
        index.append(f'- [{it["title"]}]({folder}/{name}) ({it["date"]}, was {it["link"]})')
media = [it["attachment"] for it in items if it["type"] == "attachment" and it["attachment"]]
(ARCHIVE / "README.md").write_text(
    "# freerangepodcast.org archive\n\nComplete export of the WordPress site, taken 2026-09-19.\n"
    "`wordpress-export.xml` is the raw export; `posts/` holds the episode posts and `pages/` every page\n"
    "(episode teaching-materials pages, transcripts, and the site's static pages), as plain HTML.\n\n"
    "## Contents\n\n" + "\n".join(index) +
    "\n\n## Media files\n\nThese were hosted on WordPress and are not included in the export; download any you want to keep:\n\n"
    + "\n".join(f"- {m}" for m in media) + "\n", encoding="utf-8")
print("archive:", len(index), "items,", len(media), "media urls")

# ---------- 2. transcripts ----------
TR = ROOT / "content" / "podcast" / "transcripts"
TR.mkdir(parents=True, exist_ok=True)
transcripts = {}
for it in items:
    if it["type"] == "page" and "transcription" in it["title"].lower():
        m = re.search(r"s(\d)[es](\d+)", it["slug"], re.I) or re.search(r"S(\d)[ES](\d+)", it["title"])
        code = f"S{int(m.group(1))}E{int(m.group(2))}"
        paras = [html.unescape(re.sub(r"<[^>]+>", "", p)).replace("\xa0", " ").strip()
                 for p in re.findall(r"<p[^>]*>(.*?)</p>", it["content"], flags=re.S)]
        paras = [p for p in paras if p]
        paras = [p_ for p_ in paras if p_ not in ("**", "`")]
        # speaker names seen with timestamps in this transcript, for bare-name lines
        names = set(m_.group(1).strip() for p_ in paras for m_ in [re.match(r"^([A-Za-z][A-Za-z .'\-]{1,60}?)\s+\d+:\d\d(?::\d\d)?\s*$", p_)] if m_)
        fixname = {"Rick Schragger": "Rich Schragger"}
        def turn(name, ts, text):
            name = fixname.get(name.strip(), name.strip())
            ts_html = f' <span class="ts">{ts}</span>' if ts else ""
            return f'<p><span class="spk">{html.escape(name)}</span>{ts_html}<br>{html.escape(text)}</p>'
        def chunks(text, n=160):
            # very long single-speaker paragraphs: split at sentence ends every ~n words
            words = text.split()
            if len(words) <= 400: return [text]
            out_, buf = [], []
            for w in words:
                buf.append(w)
                if len(buf) >= n and re.search(r"[.!?]$", w):
                    out_.append(" ".join(buf)); buf = []
            if buf: out_.append(" ".join(buf))
            return out_
        out, i = [], 0
        while i < len(paras):
            p_ = paras[i]
            m2 = re.match(r"^([A-Za-z][A-Za-z .'\-]{1,60}?)\s+(\d+:\d\d(?::\d\d)?)\s*$", p_)
            m3 = re.match(r"^([A-Za-z][A-Za-z .'\-]{1,60}?)\s+(\d+:\d\d(?::\d\d)?)\s+(\S.*)$", p_)  # name, time and text on one line
            if m2 and i + 1 < len(paras):
                texts = chunks(paras[i + 1])
                out.append(turn(m2.group(1), m2.group(2), texts[0]))
                out += [f"<p>{html.escape(t_)}</p>" for t_ in texts[1:]]
                i += 2
            elif m3 and m3.group(1).strip() in names:
                out.append(turn(m3.group(1), m3.group(2), m3.group(3)))
                i += 1
            elif p_ in names and i + 1 < len(paras):
                out.append(turn(p_, "", paras[i + 1]))
                i += 2
            else:
                out += [f"<p>{html.escape(t_)}</p>" for t_ in chunks(p_)]
                i += 1
        # a transcript with bare timestamps between single sentences and no speaker
        # labels (S2E24): drop the timestamps and group sentences into paragraphs
        if sum(1 for p_ in paras if re.fullmatch(r"\d+:\d\d(?::\d\d)?", p_)) > len(paras) / 3:
            sents = [p_ for p_ in paras if not re.fullmatch(r"\d+:\d\d(?::\d\d)?", p_)]
            out, buf = [], []
            for s_ in sents:
                buf.append(s_)
                if sum(len(b) for b in buf) > 500:
                    out.append("<p>" + html.escape(" ".join(buf)) + "</p>"); buf = []
            if buf: out.append("<p>" + html.escape(" ".join(buf)) + "</p>")
        (TR / f"{code}.html").write_text("\n".join(out) + "\n", encoding="utf-8")
        transcripts[code] = True
# hand-edited transcripts override the generated ones
for f_ in (ROOT / "content" / "podcast" / "transcripts-edited").glob("*.html"):
    shutil.copy(f_, TR / f_.name); transcripts[f_.stem] = True
print("transcripts:", len(transcripts))

# ---------- 3. episodes ----------
episodes = []
for it in items:
    if it["type"] != "post" or it["status"] != "publish":
        continue
    c = it["content"]
    spot = re.search(r"open\.spotify\.com/episode/([A-Za-z0-9]+)", c)
    tlink = re.search(r"/s(\d)[es](\d+)-tr", c, re.I)
    m = re.search(r"S(\d)E(\d+)", it["title"]) or re.search(r"Season (\d), Episode (\d+)", it["title"])
    season, num = int(m.group(1)), int(m.group(2))
    if tlink:  # the transcript link is the reliable numbering where titles drifted
        season, num = int(tlink.group(1)), int(tlink.group(2))
    body = strip_wp(re.sub(r"<figure.*?</figure>|<div class=\"wp-block-buttons\">.*?</div></div>", "", c, flags=re.S))
    paras = [p.strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S)]
    paras = [re.sub(r"(<br\s*/?>\s*)+$", "", p).strip() for p in paras if re.sub(r"<[^>]+>|&nbsp;", "", p).strip()]
    # some posts put several paragraphs in one <p> separated by <br><br>
    split = []
    for p in paras:
        split += [s.strip() for s in re.split(r"(?:<br\s*/?>\s*){2,}", p) if s.strip()]
    text0 = html.unescape(re.sub(r"<[^>]+>", "", split[0])) if split else ""
    g = re.search(r"(?:joined by|speaks with|talks with|talks to|interviews|conversation with|sits down with|welcomes|is joined by|chats with)\s+(?:guest\s+)?([A-Z][\w.'’\-]+(?:\s+(?:[A-Z][\w.'’\-]+|de|van|von|der))*)", text0)
    guest = g.group(1).rstrip(",.") if g else ""
    code = f"S{season}E{num}"
    episodes.append(dict(code=code, season=season, num=num, title=it["title"], guest=guest,
                         date=it["date"], spotify=spot.group(1) if spot else "", slug=it["slug"],
                         transcript=code in transcripts, summary=split, bonus="SFI" in it["title"]))
# names the heuristic could not get from the summaries
GUESTS = {'S1E1':'Deborah Lawrence','S1E2':'Camilo Sánchez','S1E3':'Lee Buchheit and Mitu Gulati','S1E5':'Madison Condon','S1E6':'Karen McGlathery','S1E7':'Jonathan Cannon','S1E14':'Elizabeth Kolbert','S1E29':'Rich Schragger','S1E30':'Solo episode: on interdisciplinary engagement','S2E2':'Matt Disandro and Elizabeth Putfark','S2E10':'Ganesh Sitaraman and Shelley Welton','S2E11':'Quinn Curtis, Mitu Gulati, and Mark Weidemaier','S2E12':'Richard Lazarus','S2E20':'Nicholas Allen','S2E22':'Solo episode: remembering Dick Stewart','S2E23':'Roundtable: SFI working group on biodiversity'}
for e in episodes:
    e["guest"] = GUESTS.get(e["code"], e["guest"])
# ---------- 4. merge the SoundCloud feed (titles, air dates, audio, newer episodes) ----------
from email.utils import parsedate_to_datetime
feed_path = ROOT / "content" / "podcast" / "feed.json"
feed = json.loads(feed_path.read_text(encoding="utf-8")) if feed_path.exists() else []
bycode = {e["code"]: e for e in episodes}
for f in feed:
    m = re.match(r"S([12I])E(\d+)[.:]\s*(.*)", f["t"])   # "SIE10" is a feed typo for S1E10
    if not m:
        continue
    season, num, title = (1 if m.group(1) == "I" else int(m.group(1))), int(m.group(2)), m.group(3).strip()
    code = f"S{season}E{num}"
    extra = dict(feed_title=title, aired=parsedate_to_datetime(f["d"]).date().isoformat(),
                 duration=f["dur"], soundcloud=f["link"], mp3=f["u"])
    if code in bycode:
        bycode[code].update(extra)
    else:  # an episode published after the WordPress site stopped being updated
        paras = [p_.strip() for p_ in re.split(r"\n\s*\n", f["desc"]) if p_.strip()]
        g = re.match(r"(.*?) on ", title)
        episodes.append(dict(code=code, season=season, num=num, title=f["t"], guest=g.group(1) if g else title,
                             date=extra["aired"], spotify="", slug="", transcript=code in transcripts,
                             summary=[html.escape(p_) for p_ in paras], bonus=False, **extra))
SPOTIFY_EXTRA = {"S2E25": "0TLr9k85OPU3hKsb6NT5Gr"}
for e in episodes:
    e["spotify"] = e["spotify"] or SPOTIFY_EXTRA.get(e["code"], "")
    e["series"] = "free-range"
# the Intercontinental Academia 4 interviews (2021), a separate series in the same feed
for f in feed:
    m = re.match(r"ICA4\.(\d+)\s+(.*)", f["t"])
    if not m:
        continue
    num, title = int(m.group(1)), m.group(2).strip()
    paras = [p_.strip() for p_ in re.split(r"\n\s*\n", f["desc"]) if p_.strip()]
    g = re.match(r"(.*?) (?:on|Interviews) ", title)
    episodes.append(dict(code=f"ICA4E{num}", series="ica4", season=0, num=num, title=f["t"], guest=g.group(1) if g else title,
                         date=parsedate_to_datetime(f["d"]).date().isoformat(), spotify="", slug="", transcript=False,
                         summary=[html.escape(p_) for p_ in paras], bonus=False, feed_title=title,
                         aired=parsedate_to_datetime(f["d"]).date().isoformat(), duration=f["dur"], soundcloud=f["link"], mp3=f["u"]))
episodes.sort(key=lambda e: (e["season"], e["num"], e["bonus"]))
(ROOT / "content" / "podcast" / "episodes.json").write_text(json.dumps(episodes, indent=1, ensure_ascii=False), encoding="utf-8")
print("episodes:", len(episodes))
for e in episodes:
    print(f'{e["code"]:6} {"T" if e["transcript"] else "-"} {"sp" if e["spotify"] else "--"} {e["guest"]!r:40} {e["summary"][0][:70] if e["summary"] else ""}')
