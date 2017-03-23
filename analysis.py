#!/usr/bin/env python3.6


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import subprocess as sp
import os
from contextlib import contextmanager
import datetime

plt.rc('figure', figsize=(11, 8))


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
            sha = words[0]

            if browser.lower() == 'log':
                lower_line = line.lower()
                if 'chrome' in lower_line:
                    browser_name = 'chrome'
                elif 'firefox' in lower_line:
                    browser_name = 'firefox'
                elif 'safari' in lower_line:
                    browser_name = 'safari'
            else:
                browser_name = browser

            yield extract_meta_from_sha(sha, browser_name)


def extract_meta_from_sha(sha, browser_name=None):
    with change_dir(ROOT_DIR):
        cmd = ['git', 'show', sha]
        stdout = sp.check_output(cmd).decode()
        info = parse_commit(stdout)
        if browser_name:
            info['browser'] = browser_name
        return info


def show_timeseries():
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

    fig, axis = plt.subplots()
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


def show_breakdown():
    all_dates = sorted(list(extract_meta('log')), key=lambda row: row['date'])
    chrome_seconds, firefox_seconds, safari_seconds = 0, 0, 0
    last = all_dates[0]['date']

    for entry in all_dates:
        dt = (entry['date'] - last).seconds
        if entry['browser'] == 'chrome':
            chrome_seconds += dt
        elif entry['browser'] == 'firefox':
            firefox_seconds += dt
        elif entry['browser'] == 'safari':
            safari_seconds += dt
        else:
            raise ValueError('Unexpected browser: {}'.format(entry['browser']))

    fig, axis = plt.subplots()
    axis.bar([0, 1, 2], [chrome_seconds / 86400., firefox_seconds / 86400., safari_seconds / 86400.])
    axis.set(
        xticks=[0, 1, 2],
        xticklabels=['Chrome', 'Firefox', 'Safari'],
        xlabel='Browser',
        ylabel='Duration [days]',
        )
    fig.tight_layout()
    fig.savefig('browser-bars.png')




# show_timeseries()
show_breakdown()
