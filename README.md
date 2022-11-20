# WebScraping
A collection of web scraping and data extraction scripts.

# Usage
## 4chan
```
usage: 4chan.py [-h] [-sB BOARD-ID | -sC BOARD-ID | -sT THREAD-ID]

Tool for extracting data through the read-only 4chan JSON API.

optional arguments:
  -h, --help            show this help message and exit
  -sB BOARD-ID, --show-board BOARD-ID
                        Print board information and settings to console.
  -sC BOARD-ID, --show-catalog BOARD-ID
                        Print board catalog to console. This includes all thread and attribute details across each
                        page.
  -sT THREAD-ID         Print thread information to console.
```

# To Do List
## 4chan
- [X] Show board information
- [ ] Show catalog information
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
