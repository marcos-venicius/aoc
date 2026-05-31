#!/usr/bin/env python3

import os

readme = [
    "# Advent of code - table of contents",
    "",
    "> [!WARNING]",
    "> I'm not competing, so please don't expect this repository to have every solution right away.",
    "> I'm solving these at my own pace, but eventually, all the solutions will be here.",
    "",
    "> [!NOTE]",
    "> The code for these challenges isn't necessarily built for maximum performance.",
    "> Instead, my goal is to solve them in ways that I find fun and interesting!",
    ""
]

exclude_files = set(['sum', 'mod', 'txt', 'md', 'gitignore'])
exclude_dirs = set(['assets'])
years = sorted([x for x in os.listdir('.') if x.isnumeric() and os.path.isdir(x)], key=lambda x: int(x), reverse=True)
langs_map = {
  'c': 'C',
  'c3': 'C3',
  'py': 'Python',
  'python': 'Python',
  'odin': 'Odin',
  'go': 'Go',
  'elixir': 'Elixir',
  'zig': 'Zig'
}

def map_lang(lang):
  if lang not in langs_map:
    return lang
  return langs_map[lang]

def map_aoc_year(year):
  return f'https://adventofcode.com/{int(year)}'

def map_aoc_day(year, day):
  return f'https://adventofcode.com/{int(year)}/day/{int(day)}'

for year in years:
    readme.append(f'- Solution [{year}](./{year}) | [↗AOC]({map_aoc_year(year)})')

    days = sorted(os.listdir(os.path.join('./', year)), key=lambda x: int(x), reverse=True)

    for day in days:
        entries = sorted([x for x in os.listdir(os.path.join('./', year, day))])
        dirs = [x for x in entries if os.path.isdir(os.path.join('./', year, day, x)) if x not in exclude_dirs]
        files = [x for x in entries if os.path.isfile(os.path.join('./', year, day, x))]

        if len(dirs) > 0:
            readme.append(f'  - Solution [{day}]({os.path.join("./", year, day)}) | [↗AOC]({map_aoc_day(year, day)})')
            for d in dirs:
                readme.append(f'    - Solution [{map_lang(d)}]({os.path.join("./", year, day, d)})')
        else:
            langs = ', '.join([map_lang(x) for x in sorted(set([x.split('.')[-1] for x in files])) if x not in exclude_files])

            readme.append(f'  - Solution [{day} ({langs})]({os.path.join("./", year, day)})')
        
readme.append("")

readme_as_text = '\n'.join(readme)

with open('./README.md', 'w') as f:
    f.write(readme_as_text)
    f.close()

