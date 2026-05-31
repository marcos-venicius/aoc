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
years = sorted([x for x in os.listdir('.') if x.isnumeric() and os.path.isdir(x)], key=lambda x: int(x), reverse=True)

for year in years:
    readme.append(f'- [**{year}**](./{year})')

    days = sorted(os.listdir(os.path.join('./', year)), key=lambda x: int(x), reverse=True)

    for day in days:
        entries = sorted([x for x in os.listdir(os.path.join('./', year, day))])
        dirs = [x for x in entries if os.path.isdir(os.path.join('./', year, day, x))]
        files = [x for x in entries if os.path.isfile(os.path.join('./', year, day, x))]

        if len(dirs) > 0:
            readme.append(f'  - [**Day {day}**]({os.path.join("./", year, day)})')
            for d in dirs:
                readme.append(f'    - [**{d}**]({os.path.join("./", year, day, d)})')
        else:
            langs = ', '.join([x for x in set([x.split('.')[-1] for x in files]) if x not in exclude_files])

            readme.append(f'  - [**Day {day}** ({langs})]({os.path.join("./", year, day)})')
        
readme.append("")

readme_as_text = '\n'.join(readme)

with open('./README.md', 'w') as f:
    f.write(readme_as_text)
    f.close()

