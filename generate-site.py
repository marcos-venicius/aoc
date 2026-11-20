#!/usr/bin/env python3
"""
Generate the BLACKSITE static site for this Advent of Code repository.

    ./generate-site.py            # writes ./_site
    ./generate-site.py -o out     # writes ./out
    python3 -m http.server -d _site     # preview at http://localhost:8000
    (or just open index.html at your browser)

Only files tracked by git are published, so puzzle inputs (gitignored *.txt)
never leave your machine. No third-party dependencies.
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- config ---

LANGS = {
    # key: (label, colour, short tag)
    'python': ('Python', '#4fc1ff', 'PY'),
    'go':     ('Go',     '#00e5ff', 'GO'),
    'mca':    ('MCA',    '#ff3b5c', 'MCA'),
    'c':      ('C',      '#a0a0ff', 'C'),
    'c3':     ('C3',     '#c792ea', 'C3'),
    'odin':   ('Odin',   '#ffb000', 'ODN'),
    'zig':    ('Zig',    '#f7a41d', 'ZIG'),
    'elixir': ('Elixir', '#b48ead', 'EX'),
}

DIR_TO_LANG = {'py': 'python', 'python': 'python', 'go': 'go', 'mca': 'mca', 'c': 'c',
               'c3': 'c3', 'odin': 'odin', 'zig': 'zig', 'elixir': 'elixir', 'ex': 'elixir'}

EXT_TO_LANG = {'.py': 'python', '.go': 'go', '.mca': 'mca', '.c': 'c', '.h': 'c', '.c3': 'c3',
               '.odin': 'odin', '.zig': 'zig', '.ex': 'elixir', '.exs': 'elixir'}

SKIP_FILES = {'go.sum', '.gitignore'}
SKIP_EXTS = {'.txt', '.sum', '.o', '.so', '.a', '.dump', '.swp'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
NOTE_EXTS = {'.md'}


def days_in_year(year):
    # Since 2025 Advent of Code runs for 12 days.
    return 12 if year >= 2025 else 25


# ------------------------------------------------------------- git data ---

def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout


def repo_slug():
    if os.getenv('GITHUB_REPOSITORY'):
        return os.environ['GITHUB_REPOSITORY']
    try:
        url = git('remote', 'get-url', 'origin').strip()
    except subprocess.CalledProcessError:
        return None
    m = re.search(r'github\.com[:/](.+?)(?:\.git)?$', url)
    return m.group(1) if m else None


def commit_dates():
    """Map 'YYYY/DD' -> (first commit date, last commit ISO timestamp) touching that day."""
    out = git('log', '--reverse', '--format=@%aI', '--name-only')
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith('@'):
            current = line[1:]
        elif line:
            m = re.match(r'(\d{4})/(\d{2})/', line)
            if m:
                key = f'{m.group(1)}/{m.group(2)}'
                first = dates.get(key, (current[:10], None))[0]
                dates[key] = (first, current)
    return dates


# ---------------------------------------------------------------- model ---

@dataclass
class SrcFile:
    path: str          # repo-relative
    name: str          # relative to the solution dir
    lang: str | None   # highlighter key
    text: str

    @property
    def lines(self):
        return self.text.count('\n') + (0 if self.text.endswith('\n') or not self.text else 1)


@dataclass
class Solution:
    lang: str
    files: list = field(default_factory=list)

    @property
    def loc(self):
        return sum(f.lines for f in self.files)


@dataclass
class Day:
    year: int
    day: int
    solutions: dict = field(default_factory=dict)  # lang -> Solution
    notes: list = field(default_factory=list)      # (repo path, text)
    images: list = field(default_factory=list)     # repo paths
    date: str | None = None      # first commit (YYYY-MM-DD)
    updated: str | None = None   # last commit (ISO timestamp)

    @property
    def key(self):
        return f'{self.year}/{self.day:02d}'

    @property
    def loc(self):
        return sum(s.loc for s in self.solutions.values())


def file_lang(name):
    base = os.path.basename(name)
    if base == 'Makefile':
        return 'make'
    if base == 'go.mod':
        return 'gomod'
    return EXT_TO_LANG.get(os.path.splitext(base)[1].lower())


def file_order(f):
    base = os.path.basename(f.name)
    stem = os.path.splitext(base)[0]
    rank = 0 if stem == 'main' else 3 if stem.endswith('_test') or stem.startswith('test') else \
        4 if f.lang in ('make', 'gomod') else 1
    return (rank, f.name.count('/'), f.name)


def read_text(path):
    try:
        with open(os.path.join(ROOT, path), encoding='utf-8') as fp:
            return fp.read()
    except (UnicodeDecodeError, FileNotFoundError):
        return None


def collect():
    tracked = git('ls-files').splitlines()
    dates = commit_dates()
    days = {}

    for path in tracked:
        m = re.match(r'(\d{4})/(\d{2})/(.+)$', path)
        if not m:
            continue
        year, dd, rest = int(m.group(1)), int(m.group(2)), m.group(3)
        base = os.path.basename(rest)
        ext = os.path.splitext(base)[1].lower()
        day = days.setdefault((year, dd), Day(year, dd))
        day.date, day.updated = dates.get(day.key, (None, None))

        if ext in IMAGE_EXTS:
            day.images.append(path)
            continue
        if base in SKIP_FILES or ext in SKIP_EXTS:
            continue
        text = read_text(path)
        if text is None:
            continue
        if ext in NOTE_EXTS:
            day.notes.append((path, text))
            continue

        parts = rest.split('/')
        if len(parts) > 1 and parts[0].lower() in DIR_TO_LANG:
            lang, name = DIR_TO_LANG[parts[0].lower()], '/'.join(parts[1:])
        else:
            lang, name = file_lang(rest), rest
        if lang in ('make', 'gomod', None):
            lang = None  # attach to a solution later
        sol_key = lang or '_misc'
        sol = day.solutions.setdefault(sol_key, Solution(sol_key))
        sol.files.append(SrcFile(path, name, file_lang(rest), text))

    # Flat days: Makefile / go.mod without a language folder join a real solution.
    for day in days.values():
        misc = day.solutions.pop('_misc', None)
        if misc:
            target = next(iter(day.solutions.values()), None)
            if target is None:
                continue
            target.files.extend(misc.files)
        for sol in day.solutions.values():
            sol.files.sort(key=file_order)

    return {k: d for k, d in days.items() if d.solutions}


# ------------------------------------------------------------ highlight ---

C_LIKE = dict(line='//', block=('/*', '*/'))

HL = {
    'python': dict(line='#', triple=True, kw='''and as assert async await break class continue def del
        elif else except finally for from global if import in is lambda nonlocal not or pass raise
        return try while with yield match case''', const='True False None self',
        types='int str float list dict set tuple bool bytes object range len print open enumerate zip map filter sorted sum min max abs any all iter next'),
    'go': dict(C_LIKE, raw='`', kw='''break case chan const continue default defer else fallthrough for
        func go goto if import interface map package range return select struct switch type var''',
        const='true false nil iota', types='''bool byte complex64 complex128 error float32 float64 int int8
        int16 int32 int64 rune string uint uint8 uint16 uint32 uint64 uintptr any append cap close copy
        delete len make new panic print println recover'''),
    'c': dict(C_LIKE, pre=True, kw='''auto break case const continue default do else enum extern for goto
        if inline register restrict return sizeof static struct switch typedef union volatile while''',
        const='NULL true false', types='''void char short int long float double signed unsigned bool size_t
        FILE uint8_t uint16_t uint32_t uint64_t int8_t int16_t int32_t int64_t'''),
    'c3': dict(C_LIKE, kw='''module import fn def const fault struct enum union macro return if else for
        foreach while do switch case default break continue defer try catch nextcase var distinct
        interface extern static inline''', const='true false null', types='''void bool char ichar short
        ushort int uint long ulong float double String usz isz any'''),
    'odin': dict(C_LIKE, kw='''package import proc struct enum union if else for in when switch case return
        defer break continue fallthrough using distinct map dynamic cast transmute auto_cast or_return
        not_in foreign bit_set where context''', const='true false nil',
        types='''int uint i8 i16 i32 i64 u8 u16 u32 u64 f32 f64 bool string rune rawptr byte any len cap
        make delete append new free'''),
    'zig': dict(C_LIKE, kw='''const var fn pub return if else while for switch break continue defer
        errdefer try catch orelse and or comptime struct enum union error test inline unreachable
        usingnamespace export extern''', const='true false null undefined',
        types='''void bool u8 u16 u32 u64 usize i8 i16 i32 i64 isize f32 f64 anyerror type anytype'''),
    'elixir': dict(line='#', kw='''def defp defmodule do end fn if else unless case cond when with for in
        and or not import alias require use receive try rescue after raise''',
        const='true false nil', types='Enum String List Map IO File Integer Kernel'),
    'mca': dict(line='#', kw='const for if else continue break return defer and or not while import',
        const='true false', types='''len append contains map filter sort any all keys set freeze bucket
        print println as_int as_string sum min max abs split'''),
    'make': dict(line='#', kw='ifeq ifneq else endif include define endef', const='', types='', var=True),
    'gomod': dict(line='//', kw='module go require replace exclude toolchain', const='', types=''),
}

for cfg in HL.values():
    for k in ('kw', 'const', 'types'):
        cfg[k] = set(cfg.get(k, '').split())

TOKEN = re.compile(r'''
    (?P<num>\b(?:0[xX][0-9a-fA-F_]+|0[bB][01_]+|\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?)\b)
  | (?P<id>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<ws>\s+)
  | (?P<op>[^\sA-Za-z0-9_])
  | (?P<other>.)
''', re.X | re.S)


def esc(s):
    return html.escape(s, quote=False)


def highlight(text, lang):
    """Small, forgiving tokenizer. Returns HTML (may contain spans across lines)."""
    cfg = HL.get(lang)
    if not cfg:
        return esc(text)
    out, i, n = [], 0, len(text)
    line, block = cfg.get('line'), cfg.get('block')
    at_line_start = True

    def span(cls, s):
        out.append(f'<span class="t-{cls}">{esc(s)}</span>')

    while i < n:
        c = text[i]
        if block and text.startswith(block[0], i):
            j = text.find(block[1], i + 2)
            j = n if j < 0 else j + len(block[1])
            span('com', text[i:j]); i = j; continue
        if line and text.startswith(line, i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            span('com', text[i:j]); i = j; continue
        if cfg.get('pre') and at_line_start and c == '#':
            j = text.find('\n', i)
            j = n if j < 0 else j
            span('pre', text[i:j]); i = j; continue
        if cfg.get('triple') and text.startswith(('"""', "'''"), i):
            q = text[i:i + 3]
            j = text.find(q, i + 3)
            j = n if j < 0 else j + 3
            span('str', text[i:j]); i = j; continue
        if c in '"\'' or (cfg.get('raw') and c == cfg['raw']):
            j = i + 1
            while j < n and text[j] != c and (c == '`' or text[j] != '\n'):
                j += 2 if text[j] == '\\' and c != '`' else 1
            j = min(j + 1, n)
            span('str', text[i:j]); i = j; continue
        if cfg.get('var') and text.startswith('$(', i):
            j = text.find(')', i)
            j = n if j < 0 else j + 1
            span('const', text[i:j]); i = j; continue

        m = TOKEN.match(text, i)
        tok = m.group(0)
        kind = m.lastgroup
        if kind == 'id':
            if tok in cfg['kw']:
                span('kw', tok)
            elif tok in cfg['const']:
                span('const', tok)
            elif tok in cfg['types']:
                span('type', tok)
            elif text[m.end():m.end() + 1] == '(':
                span('fn', tok)
            elif tok[0].isupper() and lang in ('go', 'c3', 'odin', 'zig', 'elixir'):
                span('type', tok)
            else:
                out.append(esc(tok))
        elif kind == 'num':
            span('num', tok)
        elif kind == 'op':
            span('op', tok) if tok in '=+-*/%<>!&|^~?:\\' else out.append(esc(tok))
        else:
            out.append(tok)
        if kind != 'ws':
            at_line_start = False
        elif '\n' in tok:
            at_line_start = True
        i = m.end()
    return ''.join(out)


def split_lines(hl):
    """Split highlighted HTML into lines, closing/reopening spans at line breaks."""
    lines, cur, stack = [], [], []
    for part in re.split(r'(<span class="[^"]+">|</span>|\n)', hl):
        if part == '\n':
            lines.append(''.join(cur) + '</span>' * len(stack))
            cur = list(stack)
        elif part.startswith('<span'):
            stack.append(part); cur.append(part)
        elif part == '</span>':
            stack.pop(); cur.append(part)
        elif part:
            cur.append(part)
    lines.append(''.join(cur) + '</span>' * len(stack))
    return lines


# -------------------------------------------------------------- markdown ---

def md_inline(s, resolve):
    codes = []

    def keep(m):
        codes.append(f'<code>{esc(m.group(1))}</code>')
        return f'\x00{len(codes) - 1}\x00'
    s = re.sub(r'`([^`]+)`', keep, s)
    s = esc(s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;[^&]*&quot;|\s+"[^"]*")?\)',
               lambda m: f'<img src="{resolve(m.group(2))}" alt="{m.group(1)}" loading="lazy">', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',
               lambda m: f'<a href="{resolve(m.group(2))}">{m.group(1)}</a>', s)
    s = re.sub(r'(?<!["=>])\b(https?://[^\s<]+)', r'<a href="\1">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    return re.sub(r'\x00(\d+)\x00', lambda m: codes[int(m.group(1))], s)


def markdown(text, resolve):
    out, para, lst = [], [], None
    lines = text.splitlines()
    i = 0

    def flush():
        nonlocal para, lst
        if para:
            out.append(f'<p>{md_inline(" ".join(para), resolve)}</p>')
            para = []
        if lst:
            out.append('<ul>' + ''.join(f'<li>{md_inline(x, resolve)}</li>' for x in lst) + '</ul>')
            lst = None

    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            flush()
            lang = ln[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            code = '\n'.join(lines[i + 1:j])
            out.append(f'<pre class="md-code"><code>{highlight(code, DIR_TO_LANG.get(lang, lang))}</code></pre>')
            i = j + 1
            continue
        if m := re.match(r'(#{1,6})\s+(.*)', ln):
            flush()
            lvl = min(len(m.group(1)) + 1, 6)
            out.append(f'<h{lvl}>{md_inline(m.group(2), resolve)}</h{lvl}>')
        elif m := re.match(r'\s*[-*]\s+(.*)', ln):
            if para:
                flush()
            lst = (lst or []) + [m.group(1)]
        elif not ln.strip():
            flush()
        else:
            if lst:
                flush()
            para.append(ln.strip())
        i += 1
    flush()
    return '\n'.join(out)


# ---------------------------------------------------------------- pages ---

def lang_label(k):
    return LANGS.get(k, (k.title(), '#33ff66', k[:3].upper()))[0]


def lang_color(k):
    return LANGS.get(k, (k, '#33ff66', k))[1]


def lang_tag(k):
    return LANGS.get(k, (k, '#33ff66', k[:3].upper()))[2]


def bar(frac, width=24):
    full = round(frac * width)
    return '█' * full + '░' * (width - full)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&'
         'family=VT323&display=swap" rel="stylesheet">')


def page(title, body, base, desc='Advent of Code solutions archive', extra_js='', inline_css=None):
    css = f'<style>{inline_css}</style>' if inline_css else f'<link rel="stylesheet" href="{base}assets/site.css">'
    script = '' if inline_css else f'<script src="{base}assets/site.js" defer></script>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%23000'/%3E%3Cpath d='M3 4l4 4-4 4' stroke='%2333ff66' stroke-width='2' fill='none'/%3E%3Crect x='8' y='11' width='5' height='2' fill='%2333ff66'/%3E%3C/svg%3E">
{FONTS}
{css}
</head>
<body>
<div class="crt" aria-hidden="true"></div>
<a class="skip" href="#main">skip to content</a>
<header class="top">
  <a class="brand" href="{base}index.html"><span class="blink">▮</span> BLACKSITE<span class="dim">://aoc</span></a>
  <span class="clearance">CLEARANCE: <b>PUBLIC</b></span>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <span>// end of transmission</span>
  <span class="dim">generated {date.today().isoformat()} · not affiliated with Advent of Code</span>
</footer>
{script}
{extra_js}
</body>
</html>
'''


ASCII = r'''
 █████╗  ██████╗  ██████╗
██╔══██╗██╔═══██╗██╔════╝
███████║██║   ██║██║
██╔══██║██║   ██║██║
██║  ██║╚██████╔╝╚██████╗
╚═╝  ╚═╝ ╚═════╝  ╚═════╝'''.strip('\n')


def render_index(days, slug):
    years = sorted({y for y, _ in days}, reverse=True)
    lang_days = Counter(l for d in days.values() for l in d.solutions)
    lang_loc = Counter()
    for d in days.values():
        for l, s in d.solutions.items():
            lang_loc[l] += s.loc
    total_sol = sum(lang_days.values())
    total_loc = sum(lang_loc.values())
    total_possible = sum(days_in_year(y) for y in years)
    latest = max(days.values(), key=lambda d: (d.updated or '', d.year, d.day))

    boot = [
        ('OK', 'mounting /dev/archive ... done'),
        ('OK', f'{len(days)} dossiers recovered across {len(years)} operations'),
        ('OK', f'{total_sol} solutions · {len(lang_days)} languages · {total_loc:,} lines'),
        ('WARN', 'subject is not competing. files arrive at their own pace.'),
        ('WARN', 'code optimised for fun, not for speed.'),
        ('INFO', f'last intercept: <a href="{latest.year}/{latest.day:02d}/index.html">'
                 f'{latest.key}</a> ({(latest.updated or "?")[:10]})'),
    ]
    boot_html = '\n'.join(
        f'<li style="--i:{i}"><span class="lvl lvl-{lvl.lower()}">[{lvl:^4}]</span> {msg}</li>'
        for i, (lvl, msg) in enumerate(boot))

    langs_html = []
    top = max(lang_days.values())
    for l, n in lang_days.most_common():
        langs_html.append(
            f'<li><span class="lname" style="--c:{lang_color(l)}">{lang_label(l)}</span>'
            f'<span class="lbar" style="--c:{lang_color(l)}">{bar(n / top, 20)}</span>'
            f'<span class="lnum">{n:>3}</span><span class="dim lloc">{lang_loc[l]:,} loc</span></li>')

    years_html = []
    for y in years:
        total = days_in_year(y)
        solved = [d for (yy, _), d in days.items() if yy == y]
        cells = []
        for dd in range(1, total + 1):
            d = days.get((y, dd))
            if d:
                dots = ''.join(f'<i style="--c:{lang_color(l)}" title="{lang_label(l)}"></i>'
                               for l in sorted(d.solutions))
                langs = ', '.join(lang_label(l) for l in sorted(d.solutions))
                cells.append(f'<a class="cell on" href="{y}/{dd:02d}/index.html" '
                             f'aria-label="{y} day {dd}: {langs}"><b>{dd:02d}</b>'
                             f'<span class="dots">{dots}</span></a>')
            else:
                cells.append(f'<span class="cell off" aria-label="{y} day {dd}: not solved">'
                             f'<b>{dd:02d}</b><span class="redact">█████</span></span>')
        pct = len(solved) / total
        years_html.append(f'''
<section class="year" id="y{y}">
  <h2><a href="#y{y}">OP-{y}</a>
    <span class="prog"><span class="pbar">{bar(pct, 25)}</span> {len(solved):>2}/{total}</span>
    <a class="ext" href="https://adventofcode.com/{y}" rel="noopener">aoc ↗</a></h2>
  <div class="grid g{total}">{''.join(cells)}</div>
</section>''')

    src = f'<a href="https://github.com/{slug}" rel="noopener">github.com/{slug}</a>' if slug else ''
    body = f'''
<section class="hero">
  <pre class="ascii" aria-label="AOC">{ASCII}</pre>
  <div class="hero-side">
    <p class="stamp">CLASSIFIED // DECLASSIFIED</p>
    <p class="tagline">Advent of Code field archive.<br>Every puzzle, every language, raw source.</p>
    <p class="dim">source: {src}</p>
  </div>
</section>

<section class="term" aria-label="system log">
  <p class="prompt"><span class="u">root@blacksite</span>:<span class="p">~/aoc</span>$ ./boot --verbose</p>
  <ol class="boot">{boot_html}</ol>
</section>

<section class="stats">
  <div class="stat"><span class="k">operations</span><span class="v">{len(years)}</span></div>
  <div class="stat"><span class="k">days cracked</span><span class="v">{len(days)}<small>/{total_possible}</small></span></div>
  <div class="stat"><span class="k">solutions</span><span class="v">{total_sol}</span></div>
  <div class="stat"><span class="k">lines of code</span><span class="v">{total_loc:,}</span></div>
</section>

<section class="langs" aria-label="languages">
  <p class="prompt"><span class="u">root@blacksite</span>:<span class="p">~/aoc</span>$ stat --by-language</p>
  <ul>{''.join(langs_html)}</ul>
</section>

<nav class="filter" aria-label="filter by language">
  <span class="dim">filter:</span>
  <button class="chip active" data-lang="">all</button>
  {''.join(f'<button class="chip" data-lang="{lang_label(l)}" style="--c:{lang_color(l)}">{lang_label(l)}</button>' for l, _ in lang_days.most_common())}
</nav>

{''.join(years_html)}
'''
    return page('BLACKSITE // Advent of Code', body, '')


def render_day(d, prev, nxt, slug):
    base = '../../'
    gh = f'https://github.com/{slug}/blob/main/' if slug else None
    langs = sorted(d.solutions, key=lambda l: (-d.solutions[l].loc, l))
    tabs, panels = [], []
    for i, l in enumerate(langs):
        sol = d.solutions[l]
        sel = 'true' if i == 0 else 'false'
        tabs.append(f'<button role="tab" id="tab-{l}" aria-controls="panel-{l}" aria-selected="{sel}" '
                    f'style="--c:{lang_color(l)}">{lang_label(l)} <span class="dim">{sol.loc}L</span></button>')
        files_html = []
        index = []
        for fi, f in enumerate(sol.files):
            fid = f'{l}-{fi}'
            index.append(f'<a href="#{fid}">{esc(f.name)}</a>')
            rows = split_lines(highlight(f.text.rstrip('\n'), f.lang))
            code = ''.join(f'<span class="ln" id="{fid}-L{n}"><a href="#{fid}-L{n}" '
                           f'class="lnum" aria-hidden="true">{n}</a><span class="lc">{r or " "}</span></span>'
                           for n, r in enumerate(rows, 1))
            raw = f' <a href="{gh}{f.path}" rel="noopener">view on github ↗</a>' if gh else ''
            files_html.append(f'''
<figure class="file" id="{fid}">
  <figcaption><span class="fname">── {esc(f.name)} ──</span><span class="dim">{f.lines} lines</span>
    <span class="acts"><button class="copy" data-target="{fid}-src">[copy]</button>{raw}</span></figcaption>
  <pre class="code"><code>{code}</code></pre>
  <textarea hidden id="{fid}-src">{html.escape(f.text)}</textarea>
</figure>''')
        hidden = '' if i == 0 else ' hidden'
        panels.append(f'''
<section role="tabpanel" id="panel-{l}" aria-labelledby="tab-{l}" class="panel"{hidden}>
  <p class="prompt"><span class="u">root@blacksite</span>:<span class="p">~/aoc/{d.key}</span>$ ls {l}/</p>
  <p class="findex">{' '.join(index)}</p>
  {''.join(files_html)}
</section>''')

    notes_html = ''
    if d.notes:
        parts = []
        day_dir = f'{d.year}/{d.day:02d}'
        for path, text in d.notes:
            note_dir = os.path.dirname(path)

            def resolve(url, note_dir=note_dir):
                if re.match(r'^[a-z]+:|^#|^/', url):
                    return html.escape(url)
                target = os.path.normpath(os.path.join(note_dir, url))
                return html.escape(os.path.relpath(target, day_dir))
            parts.append(f'<article class="note">{markdown(text, resolve)}</article>')
        notes_html = f'''
<details class="notes">
  <summary class="prompt"><span class="u">root@blacksite</span>:<span class="p">~/aoc/{d.key}</span>$ cat README.md
    <span class="dim">[field notes attached — click to expand]</span></summary>
  {''.join(parts)}
</details>'''

    def navlink(x, rel, label):
        if not x:
            return f'<span class="dim">{label}</span>'
        return f'<a rel="{rel}" href="{base}{x.year}/{x.day:02d}/index.html">{label.replace("%", x.key)}</a>'

    aoc = f'https://adventofcode.com/{d.year}/day/{d.day}'
    gh_dir = f' · <a href="https://github.com/{slug}/tree/main/{d.key}" rel="noopener">source ↗</a>' if slug else ''
    body = f'''
<nav class="crumbs"><a href="{base}index.html">~/aoc</a> / <a href="{base}index.html#y{d.year}">{d.year}</a> / <b>{d.day:02d}</b></nav>

<section class="dossier">
  <div>
    <p class="dim">DOSSIER</p>
    <h1>{d.year}<span class="sep">-</span>{d.day:02d}</h1>
    <p class="meta">
      <span>langs: {' '.join(f'<b style="color:{lang_color(l)}">{lang_tag(l)}</b>' for l in langs)}</span>
      <span>loc: <b>{d.loc}</b></span>
      <span>declassified: <b>{d.date or 'unknown'}</b></span>
    </p>
    <p class="links"><a href="{aoc}" rel="noopener">puzzle brief ↗</a>{gh_dir}</p>
  </div>
  <p class="stamp big">DECLASSIFIED</p>
</section>

<nav class="daynav" aria-label="day navigation">
  {navlink(prev, 'prev', '← %')}
  <span class="dim keys">[h/←] prev · [l/→] next · [u] up</span>
  {navlink(nxt, 'next', '% →')}
</nav>

{notes_html}

<div class="tabs" role="tablist" aria-label="languages">{''.join(tabs)}</div>
{''.join(panels)}
'''
    return page(f'{d.key} // BLACKSITE', body, base, desc=f'Advent of Code {d.year} day {d.day} solutions')


def render_404(slug):
    body = '''
<section class="term lost">
  <p class="prompt"><span class="u">root@blacksite</span>:<span class="p">~/aoc</span>$ cat ./requested-file</p>
  <p class="err">cat: ./requested-file: <b>ACCESS DENIED</b> — file does not exist or is above your clearance.</p>
  <p class="redact-line">████████ ██████ ███ ████████████ ██ ███████</p>
  <p><a href="index.html">← return to archive</a></p>
</section>'''
    # 404.html is served for any missing path, so relative URLs break. The CSS is
    # inlined, and the home links point at the Pages base (/<repo>/ for project
    # pages, / for <user>.github.io), falling back to / for local previews.
    repo = slug.split('/')[-1] if slug else ''
    base = os.getenv('SITE_BASE') or ('/' if not repo or repo.endswith('.github.io') else f'/{repo}/')
    with open(os.path.join(ROOT, '.site', 'site.css'), encoding='utf-8') as fp:
        css = fp.read()
    fix_links = (f'<script>(() => {{ const b = location.pathname.startsWith({json.dumps(base)}) '
                 f'? {json.dumps(base)} : "/"; document.querySelectorAll(\'a[href$="index.html"]\')'
                 f'.forEach(a => a.href = b + "index.html"); }})();</script>')
    return page('404 // BLACKSITE', body, base, extra_js=fix_links, inline_css=css)


# ---------------------------------------------------------------- build ---

def build(out):
    days = collect()
    if not days:
        sys.exit('no solutions found')
    slug = repo_slug()

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'assets'))

    src_assets = os.path.join(ROOT, '.site')
    for name in os.listdir(src_assets):
        shutil.copy(os.path.join(src_assets, name), os.path.join(out, 'assets', name))

    def write(rel, content):
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fp:
            fp.write(content)

    order = sorted(days.values(), key=lambda d: (d.year, d.day))
    for i, d in enumerate(order):
        prev = order[i - 1] if i > 0 else None
        nxt = order[i + 1] if i + 1 < len(order) else None
        write(f'{d.key}/index.html', render_day(d, prev, nxt, slug))
        for img in d.images:
            dst = os.path.join(out, img)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(ROOT, img), dst)

    write('index.html', render_index(days, slug))
    write('404.html', render_404(slug))
    write('.nojekyll', '')
    write('manifest.json', json.dumps(
        {d.key: sorted(d.solutions) for d in order}, indent=1))

    print(f'built {len(order)} days into {os.path.relpath(out, os.getcwd())}/')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('-o', '--out', default=os.path.join(ROOT, '_site'))
    build(os.path.abspath(ap.parse_args().out))
