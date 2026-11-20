#!/usr/bin/env python3

import re
import os
import sys
import requests
import shutil

IS_GET_INPUT_COMMAND = 'getinput' in sys.argv
IS_HELP_COMMAND = '--help' in sys.argv or '-h' in sys.argv
IS_PY_COMMAND = 'py' in sys.argv

AOC_AUTH_KEY = 'AOC_AUTH'
AOC_GITHUB_REPO_KEY = 'AOC_GITHUB_REPO'
AOC_INPUT_FILE = 'input.txt'

def get_aoc_root_dir():
    path = os.getcwd()

    while path != '/':
        dirs = os.listdir(path)

        if '.git' in dirs:
            return os.path.abspath(path)

        path = os.path.join(path, '../')

    raise Exception("didn't find root folder")

def get_template_dir_for(lang):
    dir = get_aoc_root_dir()

    template_dir = os.path.join(dir, '.templates', lang)

    if not os.path.exists(template_dir) or not os.path.isdir(template_dir):
        raise Exception(f"{template_dir} doesn't exists or isn't a valid directory")

    return template_dir

if IS_HELP_COMMAND:
    print('usage:', sys.argv[0], 'getinput|py')
    print('commands:')
    print('  getinput    get the current pwd aoc day input')
    print('  py          generate a python boilerplate')
    print('flags:')
    print(f'  --force      to force getting the input again when you already has a {AOC_INPUT_FILE}')
    print(f'  --help|-h    to see this help message')
    print(' run without "getinput" argument to open the day at your browser')
    exit(0)

if IS_GET_INPUT_COMMAND and (AOC_AUTH := os.getenv(AOC_AUTH_KEY, 'NOT_FOUND')) == 'NOT_FOUND':
    print("error:")
    print(f" you don't have {AOC_AUTH_KEY} configured. Exiting...")
    print(" to configure you account, open the https://adventofcode.com logged in your account and:")
    print("  - search for a cookie 'session=[a-z0-9]+'")
    print("  - get the value of the 'session' cookie")
    print(f"  - put it in the env vars of your system with the name {AOC_AUTH_KEY}")
    print(" done.")
    exit(1)

if IS_GET_INPUT_COMMAND and (AOC_GITHUB_REPO := os.getenv(AOC_GITHUB_REPO_KEY, 'NOT_FOUND')) == 'NOT_FOUND':
    print("error:")
    print(f" please, create an env var called '{AOC_GITHUB_REPO_KEY}' and put your git aoc repository")
    print(" it's sent trought the requests as the user agent")
    exit(1)

if IS_GET_INPUT_COMMAND and AOC_INPUT_FILE in os.listdir(os.getcwd()):
    if '--force' not in sys.argv:
        print('error:')
        print(' you seems to already have the input loaded locally')
        print(' do you really want to download it?')
        print(' use --force to download it anyway')
        exit(1)

pattern = r'.*(?:[/\\]\w+)+[/\\](\d{4})[/\\](\d{2})'

if not re.match(pattern, os.getcwd()):
    print('error:')
    print(' the script works better when you are inside an aoc challenge folder')
    exit(1)

year, day = re.findall(pattern, os.getcwd())[0]
year, day = int(year), int(day)


if IS_GET_INPUT_COMMAND:
    result = requests.get(
        f'https://adventofcode.com/{year}/day/{day}/input',
        headers={
            'User-Agent': AOC_GITHUB_REPO
        },
        cookies={
            'session': AOC_AUTH
        },
        timeout=10
    )

    if result.status_code != 200:
        print('Could not successfully load the input file due to status code', result.status_code)
        print('error:', result.text.strip())

        exit(1)

    input_file_path = os.path.join(os.getcwd(), AOC_INPUT_FILE)

    fd = os.open(input_file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)

    with os.fdopen(fd, "w", encoding='utf-8') as file:
        file.write(result.text)

    print('input saved successfully')
elif IS_PY_COMMAND:
    template_dir = get_template_dir_for('python')

    entries = os.listdir(template_dir)
    base_path = os.getcwd()

    for entry in entries:
        origin = os.path.join(template_dir, entry)
        destination = os.path.join(base_path, entry)

        if os.path.exists(destination):
            print(f'skipping {entry}...')
            continue

        print(f'copying {entry}...')
        shutil.copy(origin, destination)
else:
    import webbrowser

    url = f'https://adventofcode.com/{year}/day/{day}'

    webbrowser.open(url)
    