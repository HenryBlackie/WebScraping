#import json
#import pandas
from pprint import pprint
import argparse
import html
import os
import re
import requests
import sys


def line_break():
    # Print line across width of terminal
    print('-' * os.get_terminal_size(0)[0])


def parse_arguments():
    # Configure argument parser
    parser = argparse.ArgumentParser(
        description=
        'Tool for extracting data through the read-only 4chan JSON API.')

    # Create parser action group
    # Commands within this group are mutually exclusive
    action_group = parser.add_mutually_exclusive_group(required=True)

    # Configure arguments
    action_group.add_argument(
        '-sB',
        '--show-board',
        action='store_true',
        help=
        'Print board information and settings to console. Requires board ID (-b).'
    )
    action_group.add_argument(
        '-sC',
        '--show-catalog',
        action='store_true',
        help=
        'Print board catalog to console. This includes all thread and attribute details across each page. Requires board ID (-b).'
    )
    action_group.add_argument(
        '-sT',
        '--show-thread',
        action='store_true',
        help=
        'Print thread information to console. Requires thread ID (-t) and board ID (-b).'
    )
    action_group.add_argument(
        '-sTC',
        '--show-thread-comments',
        action='store_true',
        help=
        'Print thread comments to console. Requires thread ID (-t) and board ID (-b).'
    )
    parser.add_argument(
        '-u',
        type=str,
        dest='url',
        help=
        'The script will attempt to automatically extract the board (-b) and thread (-t) values from the provided URL.'
    )
    parser.add_argument('-b',
                        type=str,
                        dest='board_id',
                        metavar='BOARD-ID',
                        help='Board ID.')
    parser.add_argument('-t',
                        type=str,
                        dest='thread_id',
                        metavar='THREAD-ID',
                        help='Thread ID')
    parser.add_argument(
        '-d',
        type=int,
        default=0,
        dest='delay',
        metavar='DELAY',
        help=
        'Seconds to wait between major operations such as displaying thread information. [Default: 0]'
    )

    # Parse, verify, and return user-provided arguments
    if len(sys.argv) < 2:
        # Print help message if no arguments provided and exit script
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()


def parse_url(url):
    # Extract board ID from URL string
    # Board ID can be a alphanumeric value
    # Regex: (?<=org\/)[A-z1-9]+
    board_id = re.search(r'(?<=org\/)[A-z1-9]+', url)
    if board_id is not None:
        board_id = board_id.group()

    # Extract board ID from URL string
    # Thread ID is an integer
    # Regex: (?<=thread\/)\d+
    thread_id = re.search(r'(?<=thread\/)\d+', url)
    if thread_id is not None:
        thread_id = thread_id.group()

    print(f'URL Board ID: {board_id}')
    print(f'URL Thread ID: {thread_id}')

    return board_id, thread_id


def show_board(board_id, api_endpoints):
    # Get board details from JSON API
    json_response = requests.get(api_endpoints['boards']).json()

    # Extract board specific details from response
    try:
        board_dict = [
            details for details in json_response['boards']
            if details['board'] == board_id
        ][0]
    except IndexError as e:
        print(f'Error: Unable to find board "{board_id}"')
        sys.exit(1)

    # Define board attributes and descriptions
    board_attributes = {
        'board': 'Board directory',
        'title': 'Board title',
        'ws_board': 'Work safe',
        'per_page': 'Threads on each index page',
        'pages': 'Total pages',
        'max_filesize': 'Max size for non .webm attachments (KB)',
        'max_webm_filesize': 'Max size for .webm attachments (KB)',
        'max_comment_chars': 'Max characters in post comments',
        'max_webm_duration': 'Max duration of .webm attachments (seconds)',
        'bump_limit': 'Max replies allowed before thread stops bumping',
        'image_limit':
        'Max image replies per thread before image replies are discarded',
        'cooldowns': 'Cooldowns',
        'meta_description': 'SEO content meta description',
        'spoilers': 'Are spoilers enabled',
        'custom_spoilers': 'Number of custom spoilers',
        'is_archived': 'Are archives enabled',
        'board_flags': 'Flag codes mapped to flag names',
        'country_flags': 'Are poster country flags enabled',
        'user_ids': 'Are poster ID tags enabled',
        'oekaki': 'Can users submit via Oekaki app',
        'sjis_tags': 'Can users SJIS drawings',
        'code_tags': 'Board supports code syntax highlighting',
        'math_tags': 'Board supports TeX',
        'text_only': 'Image posting disabled',
        'forced_anon': 'Name field disabled',
        'webm_audio': 'Are .webm attachments allowed audio',
        'require_subject': 'Do OPs require a subject',
        'min_image_width': 'Minimum image width (pixels)',
        'min_image_height': 'Minimum image height (pixels)'
    }

    print(f'--- {board_dict["title"]} Details ---')
    # Iterate board details
    for k, v in board_dict.items():
        # Modify values depending on var type
        if type(v) == str:
            # Unescape HTML characters in strings
            v = html.unescape(v)
        elif type(v) == dict:
            # Parse dictionaries into readable format
            v_list = [f'\t{v_k}: {v_v}\n' for v_k, v_v in v.items()]
            v = '\n\t' + ''.join(v_list).strip()

        # Print board details to console
        # Use attribute description when possible
        try:
            print(f'{board_attributes[k]}: {v}')
        except KeyError as e:
            print(f'{k}: {v}')


def show_catalog(board_id, api_endpoints):
    request_url = re.sub('BOARD', board_id, api_endpoints['catalog'])
    json_response = requests.get(request_url).json()

    # Define catalog attributes and descriptions
    catalog_attributes = {
        'no': 'Numeric post ID',
        'resto': 'ID of parent thread',
        'sticky': 'Is thread pinned',
        'closed': 'Is thread closed',
        'now': 'Creation time in EST/EDT timezone',
        'time': 'Creation time (UNIX)',
        'name': 'Name user posted with',
        'trip': 'User tripcode',
        'id': 'Poster ID',
        'capcode': 'Capcode identifier',
        'country': 'Poster country code (ISO 3166-2 alpha-2)',
        'country_name': 'Country name',
        'sub': 'Subject text',
        'com': 'Comment',
        'tim': 'Image upload time (UNIX + microtime)',
        'filename': 'Filename from device',
        'ext': 'Filetype',
        'fsize': 'Attachment size (bytes)',
        'md5': 'Filehash (MD5)',
        'w': 'Image width',
        'h': 'Image height',
        'tn_w': 'Thumbnail width',
        'tn_h': 'Thumbnail height',
        'filedeleted': 'Is file deleted',
        'spoiler': 'Is image spoilered',
        'custom_spoiler': 'Custom spoiler ID',
        'omitted_posts': 'Total replies minus previewed replies',
        'omitted_images': 'Total images minus previewed images',
        'replies': 'Total replies',
        'images': 'Total images',
        'bumplimit': 'Bumplimit reached',
        'imagelimit': 'Image limit reached',
        'last_modified': 'Thread last modified (UNIX)',
        'tag': '.swf upload category',
        'semantic_url': 'SEO URL slug',
        'since4pass': 'Year 4chan pass purchased',
        'unique_ips': 'Total unique posters',
        'm_img': 'Mobile optimised image exists',
        'last_replies': 'JSON representation of most recent replies to thread'
    }

    # Print catalog information
    print(f'--- {board_id} Catalog ---')
    for page in json_response:
        print(f'-- Page {page["page"]} --')
        for thread in page['threads']:
            for k, v in thread.items():
                # Modify values depending on var type
                if type(v) == str:
                    # Unescape HTML characters in strings
                    v = html.unescape(v)
                    # Indent comment text
                    if k == 'com':
                        v = '\n\t' + '\t'.join(v.splitlines(True))
                elif k == 'last_replies':
                    # Parse dictionaries into readable format
                    v = dict(v[0])
                    v_list = [f'\t{v_k}: {v_v}\n' for v_k, v_v in v.items()]
                    v = '\n\t' + ''.join(v_list).strip()

                # Print thread details to console
                # Use attribute description when possible
                try:
                    print(f'{catalog_attributes[k]}: {v}')
                except:
                    print(f'{k}: {v}')


def show_thread(board_id, thread_id, api_endpoints):
    request_url = re.sub('THREAD', thread_id, api_endpoints['thread'])
    request_url = re.sub('BOARD', board_id, request_url)
    json_response = requests.get(request_url).json()

    # Define thread attributes and descriptions
    thread_attributes = {
        'no': 'Numeric post ID',
        'resto': 'ID of parent thread',
        'sticky': 'Is thread pinned',
        'closed': 'Is thread closed',
        'now': 'Creation time in EST/EDT timezone',
        'time': 'Creation time (UNIX)',
        'name': 'Name user posted with',
        'trip': 'User tripcode',
        'id': 'Poster ID',
        'capcode': 'Capcode identifier',
        'country': 'Poster country code (ISO 3166-2 alpha-2)',
        'country_name': 'Country name',
        'board_flag': 'Board flag code',
        'flag name': 'Board flag name',
        'sub': 'Subject text',
        'com': 'Comment',
        'tim': 'Image upload time (UNIX + microtime)',
        'filename': 'Filename from device',
        'ext': 'Filetype',
        'fsize': 'Attachment size (bytes)',
        'md5': 'Filehash (MD5)',
        'w': 'Image width',
        'h': 'Image height',
        'tn_w': 'Thumbnail width',
        'tn_h': 'Thumbnail height',
        'filedeleted': 'Is file deleted',
        'spoiler': 'Is image spoilered',
        'custom_spoiler': 'Custom spoiler ID',
        'replies': 'Total replies',
        'images': 'Total images',
        'bumplimit': 'Bumplimit reached',
        'imagelimit': 'Image limit reached',
        'last_modified': 'Thread last modified (UNIX)',
        'tag': '.swf upload category',
        'semantic_url': 'SEO URL slug',
        'since4pass': 'Year 4chan pass purchased',
        'unique_ips': 'Total unique posters',
        'm_img': 'Mobile optimised image exists',
        'archived': 'Is thread archived',
        'archived_on': 'UNIX timestamp post was archived'
    }

    # Update JSON data to a more human readable format
    print(f'--- Thread {thread_id} ---')
    for idx, post in enumerate(json_response['posts']):
        print(f'-- Post {idx + 1} --')
        for k, v in post.items():
            if type(v) == str:
                v = html.unescape(v)

            if k == 'com':
                v = f'\n\t{v}'

            print(f'{thread_attributes[k]}: {v}')


def show_thread_comments(board_id, thread_id, api_endpoints):
    request_url = re.sub('THREAD', thread_id, api_endpoints['thread'])
    request_url = re.sub('BOARD', board_id, request_url)
    json_response = requests.get(request_url).json()

    # Define thread attributes and descriptions
    thread_attributes = {
        'no': 'Numeric post ID',
        'name': 'Name user posted with',
        'com': 'Comment'
    }

    thread_data = []
    for post in json_response['posts']:
        post_dict = {}
        for k, v in post.items():
            if k in thread_attributes.keys():
                if k == 'com':
                    # Unescape HTML characters
                    v = html.unescape(''.join(v))
                    # Remove HTML tags from comments
                    v = re.sub(r'<[^>]*>', '', v)
                post_dict[k] = v
        thread_data.append(post_dict)

    for post in thread_data:
        print(f'-- {post["no"]} {post["name"]} --')
        print(post['com'])


def main():
    # Parse arguments into dictionary
    args = vars(parse_arguments())
    if args['url'] is not None:
        args['board_id'], args['thread_id'] = parse_url(args['url'])

    # Specify API endpoints
    api_endpoints = {
        'archive': 'https://a.4cdn.org/BOARD/archive.json',
        'boards': 'https://a.4cdn.org/boards.json',
        'catalog': 'https://a.4cdn.org/BOARD/catalog.json',
        'thread': 'https://a.4cdn.org/BOARD/thread/THREAD.json'
    }

    # Call function for appropriate action
    if args['show_board']:
        if args['board_id'] is not None:
            show_board(args['board_id'], api_endpoints)
        else:
            print('Show board command requires board ID (-b)')
    elif args['show_catalog']:
        if args['board_id'] is not None:
            show_catalog(args['board_id'], api_endpoints)
        else:
            print('Show catalog command requires board ID (-b)')
    elif args['show_thread']:
        if args['thread_id'] is not None and args['board_id'] is not None:
            show_thread(args['board_id'], args['thread_id'], api_endpoints)
        else:
            print('Show thread command requires board and thread IDs.')
    elif args['show_thread_comments']:
        if args['thread_id'] is not None and args['board_id'] is not None:
            show_thread_comments(args['board_id'], args['thread_id'],
                                 api_endpoints)
        else:
            print(
                'Show thread comments command requires board and thread IDs.')


if __name__ == '__main__':
    main()
