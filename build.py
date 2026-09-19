#!/usr/bin/env python3
"""Generates the HTML pages for michaellivermore.com from one shared shell.

Run `python3 build.py` after editing page content below. The output is plain
HTML in this folder, which GitHub Pages serves directly. No dependencies.
"""
from pathlib import Path

ROOT = Path(__file__).parent

NAV = [
    ("index.html", "Home"),
    ("scholarship.html", "Scholarship"),
    ("books.html", "Books"),
    ("podcast.html", "Podcast"),
    ("owcal.html", "Workshop"),
    ("miscellany.html", "Miscellany"),
]

LINKS = {
    "faculty": "https://www.law.virginia.edu/faculty/profile/mal5un/2457619",
    "scholar": "https://scholar.google.com/citations?user=rKv_MJ4AAAAJ&amp;hl=en",
    "ssrn": "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=360665",
    "amazon": "http://amazon.com/author/michaellivermore",
    "cv": "assets/livermore-cv.pdf",
}

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="rail">
  <a class="name" href="{base}index.html"><span>Michael A.</span> <span>Livermore</span></a>
  <nav aria-label="Site">
    <ul>
{nav}
    </ul>
  </nav>
  <div class="links">
    <a href="{faculty}">UVA Law faculty page</a>
    <a href="{scholar}">Google Scholar</a>
    <a href="{ssrn}">SSRN</a>
    <a href="{base}{cv}">CV</a>
  </div>
</header>
<main>
{body}
</main>
<script src="{base}assets/net.js" defer></script>
<script src="{base}assets/marks.js" defer></script>
</body>
</html>
"""


def nav_html(current, base=""):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'      <li><a href="{base}{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


def pub(year, title, venue, cite="", co="", book=False):
    """One publication row. venue is italicised; cite is volume/page."""
    t = f"<em>{title}</em>" if book else f"“{title},”"
    v = f" <i>{venue}</i>" if venue else ""
    c = f" {cite}" if cite else ""
    w = f' <span class="co">with {co}</span>' if co else ""
    return f'    <li><span class="yr">{year}</span><span>{t}{v}{c}.{w}</span></li>'


PAGES = {}

PAGES["index.html"] = dict(
    title="Michael A. Livermore",
    description="Michael A. Livermore is a professor of law at the University of Virginia working on environmental law, regulation, and computational legal studies.",
    body="""
<section class="hero">
  <canvas class="net" id="net" aria-hidden="true"></canvas>
  <div class="hero-text">
    <h1>Law, politics, and the environment, through the lens of ethics, economics, and data.</h1>
    <p class="role">Professor of Law, University of Virginia</p>
  </div>
</section>

<ul class="areas">
  <li class="a-env">
    <canvas class="mark" data-kind="env" aria-hidden="true"></canvas>
    <a href="scholarship.html#environment">Environmental law, ethics, and economics</a>
    <p>Cost-benefit analysis in regulatory decision making, nature's rights, ecocentrism, and the value of diversity.</p>
  </li>
  <li class="a-reg">
    <canvas class="mark" data-kind="reg" aria-hidden="true"></canvas>
    <a href="scholarship.html#regulation">Regulation and administrative law</a>
    <p>How governments balance expertise, evidence, and analysis against legality and democratic accountability.</p>
  </li>
  <li class="a-comp">
    <canvas class="mark" data-kind="comp" aria-hidden="true"></canvas>
    <a href="scholarship.html#computational">Computational legal studies</a>
    <p>Law as data: computational text analysis, natural language processing, and artificial intelligence applied to law and legal institutions.</p>
  </li>
</ul>

<section class="about" id="about">
  <div class="about-text">
    <h2>About</h2>
    <p>Michael A. Livermore is a professor of law at the University of Virginia. His research focuses on regulation, environmental law, and the application of artificial intelligence to the law, often in collaboration with researchers in economics, computer science, neurology, and the humanities. His work has appeared in leading law journals, including the <em>Yale Law Journal</em> and the <em>University of Chicago Law Review</em>, as well as peer-reviewed legal, scientific, and social science journals.</p>
    <p>Much of his environmental work has centered on cost-benefit analysis in regulatory decision making. When used properly, this tool can clarify difficult tradeoffs and integrate analysis, expertise, and evidence into environmental policy. For the past decade he has complemented this normative work with empirical scholarship in law-as-data, a research paradigm with roots in empirical legal studies, pragmatism, and legal realism that treats the law as a living social and political practice. His current book project, <em>Varieties of Being</em>, develops a theory of moral value that seeks to bridge traditional divides between environmental and economic perspectives.</p>
  </div>
  <dl class="facts">
    <dt>Position</dt><dd>Professor of Law, University of Virginia School of Law</dd>
    <dt>Before UVA</dt><dd>Founding executive director of the <a href="http://policyintegrity.org">Institute for Policy Integrity</a> at NYU School of Law; law clerk to Judge Harry T. Edwards, U.S. Court of Appeals for the D.C. Circuit</dd>
    <dt>Education</dt><dd>New York University School of Law</dd>
    <dt>Books</dt><dd><a href="books.html"><em>Reviving Rationality</em>, <em>Law as Data</em>, <em>The Globalization of Cost-Benefit Analysis</em>, <em>Retaking Rationality</em></a></dd>
    <dt>Elsewhere</dt><dd><a href="{faculty}">UVA Law</a>, <a href="{scholar}">Google Scholar</a>, <a href="{ssrn}">SSRN</a>, <a href="{amazon}">Amazon</a>, <a href="{cv}">CV (PDF)</a></dd>
  </dl>
</section>
""",
)

PAGES["scholarship.html"] = dict(
    title="Scholarship — Michael A. Livermore",
    description="Representative publications by Michael A. Livermore in environmental law, regulation, and computational legal studies.",
    body="""
<h1 class="quiet">Scholarship</h1>
<p class="intro">Representative publications by area. The full list is in the <a href="{cv}">CV</a>; papers are on <a href="{ssrn}">SSRN</a> and <a href="{scholar}">Google Scholar</a>.</p>

<section class="field a-env" id="environment">
  <header><canvas class="mark" data-kind="env" aria-hidden="true"></canvas><h2>Environmental law, ethics, and economics</h2></header>
  <ul class="pubs">
""" + "\n".join([
    pub(2024, "Valuing Diversity", "Journal of Ethics and Social Philosophy", "28: 264"),
    pub(2021, "Where Nature's Rights Go Wrong", "Virginia Law Review", "107: 1347", "Mauricio Guim"),
    pub(2019, "Sociopolitical Feedbacks and Climate Change", "Harvard Environmental Law Review", "43: 119", "Peter Howard"),
    pub(2014, "Rethinking Health-Based Environmental Standards", "New York University Law Review", "89: 1184", "Richard L. Revesz"),
]) + """
  </ul>
</section>

<section class="field a-reg" id="regulation">
  <header><canvas class="mark" data-kind="reg" aria-hidden="true"></canvas><h2>Regulation and administrative law</h2></header>
  <ul class="pubs">
""" + "\n".join([
    pub(2024, "Presidential Transitions and Interest Group Participation in the Notice and Comment Process", "American Review of Public Administration", "54: 648", "Vladimir Eidelman, Anastassia Kornilova, and Onyi Lam"),
    pub(2020, "Reviving Rationality: Saving Cost-Benefit Analysis for the Sake of the Environment and Our Health", "", "Oxford University Press", "Richard L. Revesz", book=True),
    pub(2019, "Administrative Law in an Era of Partisan Volatility", "Emory Law Journal", "69: 1", "Daniel Richardson"),
    pub(2018, "Computationally Assisted Participatory Rulemaking", "Notre Dame Law Review", "93: 977", "Vladimir Eidelman and Brian Grom"),
]) + """
  </ul>
</section>

<section class="field a-comp" id="computational">
  <header><canvas class="mark" data-kind="comp" aria-hidden="true"></canvas><h2>Computational legal studies</h2></header>
  <ul class="pubs">
""" + "\n".join([
    pub(2024, "Judicial Dark Matter", "University of Chicago Law Review", "91: 1949", "Nina Varsava, Keith Carlson, and Daniel N. Rockmore"),
    pub(2023, "Are Lawyers' Case Selection Decisions Biased? A Field Experiment on Access to Justice", "Journal of Legal Studies", "52: 273", "Jens Frankenreiter"),
    pub(2021, "Modeling Law Search as Prediction", "Artificial Intelligence and Law", "29: 3", "Faraz Dadgostari, Mauricio Guim, Peter A. Beling, and Daniel N. Rockmore"),
    pub(2020, "The Problem of Data Bias in the Pool of Published U.S. Appellate Court Opinions", "Journal of Empirical Legal Studies", "17: 224", "Keith Carlson and Daniel N. Rockmore"),
    pub(2019, "Law as Data: Computation, Text, and the Future of Legal Analysis", "", "Santa Fe Institute Press", "Daniel N. Rockmore (editors)", book=True),
    pub(2017, "The U.S. Supreme Court and the Judicial Genre", "Arizona Law Review", "59: 837", "Allen B. Riddell and Daniel N. Rockmore"),
]) + """
  </ul>
</section>
""",
)

def row(year, html_):
    return f'    <li><span class="yr">{year}</span><span>{html_}</span></li>'


def piece(year, title, url, outlet, co=""):
    w = f' <span class="co">with {co}</span>' if co else ""
    return row(year, f'<a href="{url}">{title}</a>, <i>{outlet}</i>.{w}')


def yt(id_, title):
    return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{id_}" title="{title}" '
            f'loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>')


PAGES["miscellany.html"] = dict(
    title="Miscellany — Michael A. Livermore",
    description="Selected public writing, recorded appearances, and film.",
    body="""
<h1 class="quiet">Miscellany</h1>
<p class="intro">Selected writing for general readers, recorded appearances, and one film.</p>

<section class="field a-comp" id="talks">
  <h2>Appearances</h2>
  <ul class="pubs">
""" + "\n".join([
    row(2026, '<a href="https://youtu.be/Jb3Co5JW9m4">Should a River Have Rights?</a> Panel with Chuck Sams, moderated by Samuel Kimbriel. <i>Aspen Ideas Festival</i>, July 1. <a href="https://www.aspenideas.org/sessions/should-a-river-have-rights">Session page</a>.'),
    row(2026, '<a href="https://www.law.virginia.edu/news/video-audio/202604/admissible-s8-e6-ai-and-future-legal-practice">AI and the Future of Legal Practice</a>. Interview with Natalie Blazer on <i>Admissible</i>, the UVA Law admissions podcast, April 17. Also on <a href="https://soundcloud.com/admissiblepodcast/s8-e6-ai-and-the-future-of">SoundCloud</a> and <a href="https://www.youtube.com/watch?v=U0K6dU0Gza8">YouTube</a>.'),
    row(2024, '<a href="https://youtu.be/dOuyZqXzEsA">Where Will Artificial Intelligence Take Us?</a> Talk to the UVA Law Alumni Board and Council, November 8. <a href="https://www.law.virginia.edu/news/video-audio/202411/where-will-artificial-intelligence-take-us">UVA Law page</a>.'),
    row(2021, '<a href="https://administrativestate.gmu.edu/event/the-future-of-white-house-regulatory-oversight-in-the-biden-administration/">The Future of White House Regulatory Oversight in the Biden Administration</a>. Panel with Jennifer Nou and Stuart Shapiro, <i>C. Boyden Gray Center, George Mason University</i>, January 12.'),
    row(2020, '<a href="https://youtu.be/1fCsaobLoTs">Exploring <em>Reviving Rationality</em></a>. Book panel with Richard Revesz, Jonathan Adler, and Amy Sinden, moderated by Jonathan Cannon, <i>UVA Law</i>, November 17. Also discussed on <a href="https://www.resources.org/resources-radio/future-cost-benefit-analysis-michael-livermore-and-richard-revesz/">Resources Radio</a> and the Gray Center\'s <a href="https://ricochet.com/podcast/arbitrary-capricious/reviving-rationality-with-michael-livermore-and-richard-revesz/">Gray Matters</a> podcast.'),
    row(2019, '<a href="https://youtu.be/GLpboenw4eU">Michael Livermore Discusses <em>Law as Data</em></a>. <i>UVA Law</i>, June 3.'),
    row(2019, '<a href="https://docs.house.gov/meetings/IF/IF02/20190521/109556/HHRG-116-IF02-Wstate-LivermoreM-20190521.pdf">Testimony</a> before the House Committee on Energy and Commerce, Subcommittee on Environment and Climate Change, May 21.'),
    row(2019, '<a href="https://www.law.virginia.edu/news/201905/lawyer-your-computer">The Lawyer in Your Computer</a>. <i>Common Law</i> podcast, UVA Law, May 21.'),
]) + """
  </ul>
</section>

<section class="field a-reg" id="writing">
  <h2>Writing</h2>
  <ul class="pubs">
""" + "\n".join([
    piece(2026, "What We Lose When a Species Disappears", "https://engagement.virginia.edu/learn/thoughts-from-the-lawn/20260904-Livermore", "Thoughts from the Lawn, University of Virginia"),
    piece(2025, "The Political Limits of Algorithmic Governance", "https://www.theregreview.org/2025/12/15/livermore-the-political-limits-of-algorithmic-governance/", "The Regulatory Review"),
    piece(2025, "Escalating Flawed Deregulatory Math", "https://www.theregreview.org/2025/03/10/cecot-livermore-escalating-flawed-deregulatory-math/", "The Regulatory Review", "Caroline Cecot"),
    piece(2021, "Rejecting the Trump Anticanon of Regulatory Mismanagement", "https://www.theregreview.org/2021/02/17/livermore-rejecting-trump-anticanon-regulatory-mismanagement/", "The Regulatory Review"),
    piece(2019, "France Kicks Data Scientists Out of Its Courts", "https://slate.com/technology/2019/06/france-has-banned-judicial-analytics-to-analyze-the-courts.html", "Slate", "Daniel Rockmore"),
    piece(2018, "Tainted Review", "https://www.theregreview.org/2018/08/29/livermore-tainted-review/", "The Regulatory Review"),
    piece(2018, "Judge Kavanaugh and the Environment", "https://www.scotusblog.com/2018/07/kavanaugh-and-the-environment/", "SCOTUSblog"),
    piece(2018, "Why Cities Are Suing Oil Giants", "https://www.usnews.com/news/national-news/articles/2018-06-26/why-cities-are-suing-oil-giants", "U.S. News &amp; World Report"),
    piece(2018, "How Technology and Artificial Intelligence Can Improve Regulation", "https://thehill.com/opinion/technology/384476-how-technology-and-artificial-intelligence-can-improve-regulation/", "The Hill", "Vladimir Eidelman"),
    piece(2018, "The Keys to Our Coastal Kingdom", "https://www.usnews.com/opinion/economic-intelligence/articles/2018-01-10/oil-wins-american-coast-and-people-lose-under-offshore-drilling-expansion", "U.S. News &amp; World Report", "Jayni Hein"),
    piece(2017, "Why Shifting Regulatory Power to the States Won't Improve the Environment", "https://theconversation.com/why-shifting-regulatory-power-to-the-states-wont-improve-the-environment-78245", "The Conversation"),
    piece(2017, "Is the Supreme Court Acting Less Like a Court?", "https://theconversation.com/is-the-supreme-court-acting-less-like-a-court-75910", "The Conversation", "Daniel Rockmore"),
    piece(2016, "Offshore Drilling: Why It Makes Economic Sense to Wait", "https://theconversation.com/offshore-drilling-why-it-makes-economic-sense-to-wait-56534", "The Conversation"),
    piece(2015, "When Economics Get Lost in the Smog", "https://thehill.com/blogs/pundits-blog/energy-environment/255750-when-economics-get-lost-in-the-smog/", "The Hill", "Richard L. Revesz"),
    piece(2015, "What Is Nature Worth to You?", "https://www.nytimes.com/2015/08/09/opinion/sunday/what-is-nature-worth-to-you.html", "The New York Times", "Paul Glimcher"),
    piece(2015, "EPA's Ozone Standard Is Insufficiently Stringent, Not Overly Expensive", "https://www.theregreview.org/2015/02/16/livermore-revesz-epa-ozone-standard/", "The Regulatory Review", "Richard L. Revesz"),
    piece(2013, "The Anti-Capture Justification for Regulatory Review", "https://www.theregreview.org/2013/12/02/01-livermore-revesz-regulatory-review/", "The Regulatory Review", "Richard L. Revesz"),
    piece(2013, "A Supreme Victory for Climate Rules", "https://www.huffpost.com/author/richard-l-revesz-and-michael-a-livermore", "Huffington Post", "Richard L. Revesz"),
    piece(2013, "Can We Cap-and-Trade Our Way Out of the Debt Ceiling Crisis?", "https://www.fastcompany.com/1681176/can-we-cap-and-trade-our-way-out-of-the-debt-ceiling-crisis", "Fast Company"),
    piece(2011, "Putting Economics on the Side of the Environment", "https://www.fastcompany.com/1678991/putting-economics-on-the-side-of-the-environment", "Fast Company"),
    piece(2009, "Cass Sunstein for Regulation Czar", "https://www.forbes.com/2009/05/12/cass-sunstein-regulation-czar-opinions-contributors-senate.html", "Forbes", "Richard L. Revesz"),
    piece(2008, "A Truly Green Economics", "https://www.forbes.com/2008/12/02/environment-supreme-court-oped-cx_rr_ml_1202reveszlivermore.html", "Forbes", "Richard L. Revesz"),
    row("2009–14", 'Contributions with Richard L. Revesz to the <a href="https://www.huffpost.com/author/richard-l-revesz-and-michael-a-livermore"><i>Huffington Post</i></a> on regulation, climate policy, and cost-benefit analysis.'),
    row("2010–12", 'Regular contributor to <a href="https://grist.org/author/michael-a-livermore/"><i>Grist</i></a> on EPA rulemaking and the economics of environmental protection.'),
]) + """
  </ul>
</section>

<section class="field a-env" id="film">
  <h2>Film</h2>
  <ul class="pubs">
""" + row(2024, '<a href="https://pinegrovefilm.org/"><em>Pine Grove: More Than a School</em></a>, executive producer. A short documentary on the Pine Grove Rosenwald School in Cumberland County, Virginia, and the community fighting to preserve it, produced with UVA Law\'s Program on Law, Communities and the Environment. Official selection of the Virginia Film Festival, Justice Film Festival, Sidewalk Film Festival, and Social Impact Film Festival. <a href="https://www.law.virginia.edu/news/202410/clinic-client-featured-virginia-film-festival-flick">UVA Law\'s story on the film</a>.') + """
  </ul>
</section>

""",
)


PAGES["books.html"] = dict(
    title="Books — Michael A. Livermore",
    description="Books by Michael A. Livermore.",
    body="""
<h1 class="quiet">Books</h1>
<ul class="shelf">
  <li>
    <a class="cover" href="https://global.oup.com/academic/product/reviving-rationality-9780197539446"><img src="assets/img/reviving.png" alt="" loading="lazy"></a>
    <div>
      <h2><a href="https://global.oup.com/academic/product/reviving-rationality-9780197539446">Reviving Rationality</a></h2>
      <p class="sub">Saving Cost-Benefit Analysis for the Sake of the Environment and Our Health</p>
      <p class="by">with Richard L. Revesz. Oxford University Press, 2020</p>
      <p>For decades, administrations of both parties used cost-benefit analysis to evaluate and improve federal policy on health and the environment. The book traces how the Trump administration undermined that bipartisan practice by sidelining expertise and evidence, with policy incoherence, court defeats, and eroded public confidence as the result, and argues that restoring rigorous analysis is a precondition for effective policy on climate change and public health.</p>
    </div>
  </li>
  <li>
    <a class="cover" href="https://www.sfipress.org/books/law-as-data"><img src="assets/img/lawasdata.png" alt="" loading="lazy"></a>
    <div>
      <h2><a href="https://www.sfipress.org/books/law-as-data">Law as Data</a></h2>
      <p class="sub">Computation, Text, and the Future of Legal Analysis</p>
      <p class="by">edited with Daniel N. Rockmore. Santa Fe Institute Press, 2019</p>
      <p>The digitization of legal texts, together with advances in statistics, computer science, and data analytics, has opened new approaches to the study of law. This volume treats the text and underlying data of legal documents as the direct objects of quantitative analysis and collects research that breaks methodological ground, whether by bringing computational techniques to traditional legal questions or by pursuing questions that new data makes possible.</p>
    </div>
  </li>
  <li>
    <a class="cover" href="https://global.oup.com/academic/product/the-globalization-of-cost-benefit-analysis-in-environmental-policy-9780199934386"><img src="assets/img/globalization.png" alt="" loading="lazy"></a>
    <div>
      <h2><a href="https://global.oup.com/academic/product/the-globalization-of-cost-benefit-analysis-in-environmental-policy-9780199934386">The Globalization of Cost-Benefit Analysis in Environmental Policy</a></h2>
      <p class="by">edited with Richard L. Revesz. Oxford University Press, 2013</p>
      <p>Cost-benefit analysis is a standard tool of government in advanced economies, but most developing and emerging nations have yet to build it into their policymaking. Because those countries face the tightest budget constraints, the ability to identify which policies deliver the greatest benefits matters most to them. The volume pairs theory with case studies from the Americas, Africa, the Middle East, and Asia, and takes up the institutional questions of doing this analysis where resources are limited.</p>
    </div>
  </li>
  <li>
    <a class="cover" href="https://global.oup.com/academic/product/retaking-rationality-9780199768950"><img src="assets/img/retaking.png" alt="" loading="lazy"></a>
    <div>
      <h2><a href="https://global.oup.com/academic/product/retaking-rationality-9780199768950">Retaking Rationality</a></h2>
      <p class="sub">How Cost-Benefit Analysis Can Better Protect the Environment and Our Health</p>
      <p class="by">with Richard L. Revesz. Oxford University Press, 2008</p>
      <p>Progressive groups long treated cost-benefit analysis as the enemy of environmental protection and stayed away from the proceedings where it is done, leaving the field to industry. The book argues that economic analysis of regulation is necessary, that it need not conflict with a more compassionate approach to environmental policy, and that a reformed version of the tool can support stronger protections than the alternatives.</p>
    </div>
  </li>
</ul>
""",
)

import json

EPISODES = json.loads((ROOT / "content" / "podcast" / "episodes.json").read_text(encoding="utf-8"))


def ep_label(e):
    if e.get("series") == "ica4":
        return f'Intercontinental Academia 4, Interview {e["num"]}'
    return f'Season {e["season"]}, Episode {e["num"]}' + (" (bonus)" if e["bonus"] else "")


def ep_title(e):
    return e.get("feed_title") or e["guest"]


def nice_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def ep_file(e):
    return f'{e["code"].lower()}{"b" if e["bonus"] else ""}.html'


def podcast_index():
    out = []
    for season in (2, 1, 0):
        eps = [e for e in EPISODES if e["season"] == season]
        eps.sort(key=lambda e: (-e["num"], e["bonus"]))
        if season == 0:
            out.append('<section class="season-eps" id="ica4"><h2>Intercontinental Academia 4</h2>\n'
                       '<p class="intro">Before Free Range, a series of nine interviews recorded in 2021 for the fourth Intercontinental Academia, a program of the UBIAS network of university-based institutes for advanced study, organized that year by the Paris Institute for Advanced Study and the Institute of Advanced Transdisciplinary Studies at the Federal University of Minas Gerais on the theme of intelligence and artificial intelligence. The guests are ICA4 fellows: mathematicians, neuroscientists, philosophers, economists, and computer scientists from ten countries. In one, fellow Henry Taylor turns the microphone around.</p>\n<ul class="eps">')
        else:
            out.append(f'<section class="season-eps" id="season{season}"><h2>Season {season}</h2>\n<ul class="eps">')
        for e in eps:
            first = e["summary"][0] if e["summary"] else ""
            when = f'<span class="when">{nice_date(e["aired"])}</span>' if e.get("aired") else ""
            out.append(f'  <li><span class="num">{e["num"]}{"b" if e["bonus"] else ""}</span><div>'
                       f'<a class="guest" href="podcast/{ep_file(e)}">{ep_title(e)}</a>{when}'
                       f'<p>{first}</p></div></li>')
        out.append("</ul></section>")
    return "\n".join(out)


PAGES["podcast.html"] = dict(
    title="Free Range — Michael A. Livermore",
    description="Free Range with Mike Livermore: an archive of the podcast's two seasons, with episode summaries and transcripts.",
    body="""
<h1 class="quiet">Free Range</h1>
<div class="podcast">
  <img src="assets/img/podcast.jpg" alt="Free Range podcast artwork">
  <div>
    <p>Free Range ran for two seasons, from 2021 to 2024: fifty-five conversations with guests from journalism, law, politics, science, economics, philosophy, and environmental science. Environmental law and policy are never easy or uncontroversial, but they can be better understood through multiple perspectives. The show was produced with support from the Program on Law, Communities and the Environment at the University of Virginia School of Law.</p>
    <p>Every episode is archived here with its summary, and most with a transcript. Audio is on the usual platforms. Below the two seasons is an earlier series of interviews recorded for the Intercontinental Academia in 2021.</p>
    <ul class="linkrow">
      <li><a href="https://open.spotify.com/show/2iSYoYzF3V6pMwNAXNzxH2">Spotify</a></li>
      <li><a href="https://podcasts.apple.com/us/podcast/free-range-with-mike-livermore/id1588749945">Apple Podcasts</a></li>
      <li><a href="https://soundcloud.com/user-311970225">SoundCloud</a></li>
    </ul>
  </div>
</div>

""" + podcast_index() + """
""",
)


def episode_pages():
    pages = {}
    order = sorted(EPISODES, key=lambda e: (e["season"], e["num"], e["bonus"]))
    for i, e in enumerate(order):
        same = lambda x: x is not None and x.get("series") == e.get("series")
        prev_e = order[i - 1] if i > 0 and same(order[i - 1]) else None
        next_e = order[i + 1] if i + 1 < len(order) and same(order[i + 1]) else None
        tr = ROOT / "content" / "podcast" / "transcripts" / f'{e["code"]}.html'
        note = ("Machine transcription; speaker attribution added editorially." if e["code"] == "S2E24"
                else "Machine transcription, lightly edited; timestamps are approximate.")
        transcript = (f'<section class="transcript" id="transcript"><h2>Transcript</h2>\n'
                      f'<p class="note">{note}</p>\n'
                      + tr.read_text(encoding="utf-8") + "</section>") if (e["transcript"] and tr.exists()) else ""
        if e["spotify"]:
            embed = (f'<iframe class="player" src="https://open.spotify.com/embed/episode/{e["spotify"]}" width="100%" height="152" '
                     f'frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" title="Play on Spotify"></iframe>')
        elif e.get("mp3"):
            embed = f'<audio class="player" controls preload="none" src="{e["mp3"]}"></audio>'
        else:
            embed = ""
        meta = " ".join(x for x in [nice_date(e["aired"]) if e.get("aired") else "",
                                    f'<a href="{e["soundcloud"]}">SoundCloud</a>' if e.get("soundcloud") else ""] if x)
        nav = '<p class="epnav">'
        nav += f'<a href="{ep_file(prev_e)}">Previous: {ep_title(prev_e)}</a>' if prev_e else ""
        nav += (" " if prev_e and next_e else "") + (f'<a href="{ep_file(next_e)}">Next: {ep_title(next_e)}</a>' if next_e else "")
        nav += "</p>"
        aired = f', {nice_date(e["aired"])}' if e.get("aired") else ""
        home = ("../podcast.html#ica4", "Intercontinental Academia 4") if e.get("series") == "ica4" else ("../podcast.html", "Free Range")
        label = ep_label(e) if e.get("series") != "ica4" else f'Interview {e["num"]}'
        body = (f'<p class="kicker"><a href="{home[0]}">{home[1]}</a>, {label}{aired}</p>\n'
                f'<h1 class="quiet">{ep_title(e)}</h1>\n<div class="page">\n{embed}\n'
                + "\n".join(f"<p>{p}</p>" for p in e["summary"])
                + (f'\n<p><a href="#transcript">Read the transcript</a></p>' if transcript else "")
                + f"\n{nav}\n</div>\n{transcript}")
        pages[f"podcast/{ep_file(e)}"] = dict(
            title=f'{ep_title(e)} — Free Range, {ep_label(e)}',
            description=(e["summary"][0][:200] if e["summary"] else ep_label(e)).replace('"', "'"),
            body=body, base="../", current="podcast.html")
    return pages


PAGES.update(episode_pages())

OWCAL_YEARS = sorted((p.stem for p in (ROOT / "content" / "owcal").glob("*.html")), reverse=True)

PAGES["owcal.html"] = dict(
    title="Online Workshop on the Computational Analysis of Law — Michael A. Livermore",
    description="OWCAL, the Online Workshop on the Computational Analysis of Law.",
    body="""
<h1 class="quiet">Online Workshop on the Computational Analysis of Law</h1>

<div class="page">
<p>OWCAL gives scholars who use computational tools to study the law a regular place to present work, receive feedback, and encounter new techniques and questions. The digitization of legal texts and advances in statistics, computer science, and data analytics have opened new methodological approaches to the study of law, building on empirical legal studies by treating the text of legal documents as data. The workshop's purpose is to highlight the best scholarship in this field and to build an intellectual community around it.</p>

<p>To join the participant list, email <a href="mailto:owcal@law.virginia.edu?subject=OWCAL%20RSVP">owcal@law.virginia.edu</a> with the subject line “OWCAL RSVP”. Please circulate to colleagues and graduate students who may be interested.</p>
</div>

<h3>Schedules</h3>
<ul class="years">
""" + "\n".join(f'  <li><a href="#y{y}">{y.replace("-", "–")}</a></li>' for y in OWCAL_YEARS) + """
</ul>

""" + "\n".join(f'<section class="season" id="y{y}"><h2>{y.replace("-", "–")}</h2>\n' + (ROOT / "content" / "owcal" / f"{y}.html").read_text(encoding="utf-8") + '</section>' for y in OWCAL_YEARS) + """
""",
)

REDIRECT = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Bio — Michael A. Livermore</title>
<meta http-equiv="refresh" content="0; url=index.html#about"><link rel="canonical" href="index.html#about"></head>
<body><p>The bio has moved to <a href="index.html#about">the home page</a>.</p></body></html>
"""


def build():
    (ROOT / "podcast").mkdir(exist_ok=True)
    for fname, page in PAGES.items():
        body = page["body"].strip()
        base = page.get("base", "")
        for k, v in LINKS.items():
            body = body.replace("{" + k + "}", v)
        html = SHELL.format(
            title=page["title"], description=page["description"], base=base,
            nav=nav_html(page.get("current", fname), base), body=body, **LINKS,
        )
        (ROOT / fname).write_text(html, encoding="utf-8")
    print("wrote", len(PAGES), "pages")
    (ROOT / "bio.html").write_text(REDIRECT, encoding="utf-8")
    print("wrote bio.html (redirect)")


if __name__ == "__main__":
    build()
