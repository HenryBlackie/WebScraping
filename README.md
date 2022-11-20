# WebScraping
A collection of web scraping and data extraction scripts.

# Usage
## 4chan
```
usage: 4chan.py [-h] (-sB | -sC | -sT) [-b BOARD-ID] [-t THREAD-ID]

Tool for extracting data through the read-only 4chan JSON API.

optional arguments:
  -h, --help           show this help message and exit
  -sB, --show-board    Print board information and settings to console. Requires board ID (-b).
  -sC, --show-catalog  Print board catalog to console. This includes all thread and attribute details across each
                       page. Requires board ID (-b).
  -sT, --show-thread   Print thread information to console. Requires thread ID (-t).
  -b BOARD-ID          Board ID.
  -t THREAD-ID         Thread ID
```

# To Do List
## 4chan
- [X] Show board information
- [X] Show catalog information
- [ ] Show thread information
- [ ] Export thread
- [ ] Support different export options for threads and attachments
- [ ] Support archived threads
- [ ] Support regex matching and selective scraping of boards/threads

## Reddit
- [ ] Show subreddit information
- [ ] Show post information
- [ ] Show user information
- [ ] Export post
- [ ] Export user data
- [ ] Export subreddit data
- [ ] Support regex matching and selective scraping of subreddit posts

## TikTok
- [ ] Show user information
- [ ] Show post information
- [ ] Show hashtag information
- [ ] Export post
- [ ] Export user
- [ ] Support regex matching and selective scraping of users and hashtags
