# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import praw
import bs4 as bs
import urllib.request
import os
from urllib.parse import quote, urlparse, urlunparse

reddit = praw.Reddit(client_id = 'TYPE REDDIT CREDENTIALS HERE',
                   client_secret = 'TYPE REDDIT CREDENTIALS HERE',
                   username = 'TYPE REDDIT CREDENTIALS HERE',
                   password = 'TYPE REDDIT CREDENTIALS HERE!!!',
                   user_agent = 'TYPE REDDIT CREDENTIALS HERE')

post_links = []

clear = lambda: os.system('cls')
clear()

another = 1
which_list = 's'

while another == "1" or another == 1 or another == "y" or another == "yes" or another == "Yes":
    post_links = []
    how_many = 0
    from_subreddit = ""

    from_subreddit = input("Which subreddit would you like to get posts from?\n")
    subreddit = reddit.subreddit('{}'.format(str(from_subreddit)))
    how_many = int(input("How many posts would you like to choose from?\n"))
    sort_by = input("Based on what would you like to sort? For now, (h)ot and (t)op are available.\n")

    another == 0
    clear()

    if sort_by == "h" or "hot":
        hot_python = subreddit.hot(limit=how_many)
        for submission in hot_python:
            if not submission.stickied:
                url_parts = list(urlparse(submission.url))
                url_parts[2] = quote(url_parts[2])
                post_links.append(urlunparse(url_parts))

    if sort_by == "t" or "top":
        top_python = subreddit.top(limit=how_many)
        for submission in top_python:
            if not submission.stickied:
                url_parts = list(urlparse(submission.url))
                url_parts[2] = quote(url_parts[2])
                post_links.append(urlunparse(url_parts))

    for title_number in range(0, len(post_links)//2):
        try:
            source = urllib.request.urlopen('{}'.format(post_links[title_number])).read()
            soup = bs.BeautifulSoup(source, 'lxml')
            if "<title>" in str(soup.title):
                print("{}.: ".format(title_number), str(soup.title)[7:-8].lstrip().rstrip())
            elif "<title " in str(soup.title):
                print("{}.: ".format(title_number), str(soup.title).partition(">")[2].partition("<")[0].lstrip().rstrip())
            else:
                print("{}.: ".format(title_number), str(soup.title).lstrip().rstrip())
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            title_number += 1

    which_list = 's'

    while which_list == 's':
        article_number = input("Type the number of the article you wish to read.\n")
        source = urllib.request.urlopen('{}'.format(post_links[int(article_number)])).read()
        soup = bs.BeautifulSoup(source, 'lxml')

        clear()
        for paragraph in soup.find_all('p'):
            print(str(paragraph.text).lstrip())

        another = input("\nWould you like to read another article?")
        if another == "1" or another == 1 or another == "y" or another == "yes" or another == "Yes":
            which_list = input("(S)ame list or a (n)ew one?")
        else:
            quit()
