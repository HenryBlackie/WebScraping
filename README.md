# WebScraping
A collection of web scraping and data extraction scripts.

# Usage
## 4chan
```
usage: 4chan.py [-h] [-o OUTPUT-DIR] [-m] URL

Tool for extracting data through the read-only 4chan JSON API.

positional arguments:
  URL                   Target URL.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT-DIR         Output directory. [Default: Current directory].
  -m, --monitor-thread  Continue monitoring thread after initial download and wait for new content. Stops once the
                        thread is closed.
```

# To Do List
## 4chan
- [X] Show thread information
- [X] Export thread
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
