#!/usr/bin/env python3.6


import matplotlib.pyplot as plt
import subprocess as sp
import os
from contextlib import contextmanager
import datetime


ROOT_DIR = os.path.expanduser(
    os.path.join('~', 'dotfiles')
    )


def parse_commit(commit):
    lines = commit.split('\n')
    date_line = lines[2]
    return {
        'date': parse_date(date_line),
        }


def parse_date(date_line):
    line = ' '.join(date_line.split()[1:])
    date_format = '%a %b %d %H:%M:%S %Y %z'
    dt = datetime.datetime.strptime(line, date_format)
    return dt


@contextmanager
def change_dir(path):
    old_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_cwd)


def extract_meta(browser):
    data_path = f'{browser}.txt'  # noqa
    assert os.path.isfile(data_path)

    with open(data_path) as infile:
        for line in infile:
            line = line.strip()
            words = line.split()
            sha = words[1]

            yield extract_meta_from_sha(sha)


def extract_meta_from_sha(sha):
    with change_dir(ROOT_DIR):
        cmd = ['git', 'show', sha]
        stdout = sp.check_output(cmd).decode()
        return parse_commit(stdout)


chrome_dates = [row['date'] for row in extract_meta('chrome')]
firefox_dates = [row['date'] for row in extract_meta('firefox')]
safari_dates = [row['date'] for row in extract_meta('safari')]

all_dates = sorted(chrome_dates + firefox_dates + safari_dates)
winning_browser = []
for date in all_dates:
    for browser_entries in [chrome_dates, firefox_dates, safari_dates]:
        if date in browser_entries:
            if browser_entries is chrome_dates:
                winning_browser.append(0)
            elif browser_entries is firefox_dates:
                winning_browser.append(1)
            elif browser_entries is safari_dates:
                winning_browser.append(2)
            else:
                raise ValueError('Should not reach here')

fig, axis = plt.subplots(figsize=(11, 8))
axis.plot(all_dates, winning_browser, drawstyle='steps-mid')
axis.grid(True)
axis.set(
    title='Browser wars',
    yticks=[0, 1, 2],
    yticklabels=['Chrome', 'Firefox', 'Safari'],
    )
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig('browser-wars.png')
plt.show()
