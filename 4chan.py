#import json
#import pprint
import argparse
import html
import os
import pandas
import re
import requests
import sys
import time


def line_break():
    # Print line across width of terminal
    print('-' * os.get_terminal_size(0)[0])


def parse_arguments():
    # Configure argument parser
    parser = argparse.ArgumentParser(
        description=
        'Tool for extracting data through the read-only 4chan JSON API.')

    # Configure additional arguments
    parser.add_argument('url', type=str, metavar='URL', help='Target URL.')
    parser.add_argument('-o',
                        type=str,
                        default='',
                        dest='output_dir',
                        metavar='OUTPUT-DIR',
                        help='Output directory. [Default: Current directory].')
    parser.add_argument(
        '-m',
        '--monitor-thread',
        action='store_true',
        help=
        'Continue monitoring thread after initial download and wait for new content. Stops once the thread is closed.'
    )

    # Parse, verify, and return user-provided arguments
    if len(sys.argv) < 2:
        # Print help message if no arguments provided and exit script
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()


def parse_url(url):
    # Extract required data from URL
    # Board ID: (?<=org\/)[A-z1-9]+
    # Thread ID: (?<=thread\/)\d+
    url_data = re.findall(r'(?<=org\/)[A-z1-9]+|(?<=thread\/)\d+', url)

    # Split extracted data into variables
    board_id = None
    thread_id = None
    if len(url_data) >= 1:
        board_id = url_data[0]
    if len(url_data) == 2:
        thread_id = url_data[1]

    return board_id, thread_id


def thread_closed(json_response):
    if json_response['posts'][0].get('closed') is not None:
        return True
    else:
        return False


def show_thread_details(args, api_endpoint):
    request_url = re.sub('THREAD', args['thread_id'], api_endpoint)
    request_url = re.sub('BOARD', args['board_id'], request_url)
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
    for k, v in json_response['posts'][0].items():
        if type(v) == str:
            v = html.unescape(v)

        if k == 'com':
            v = re.sub(r'<[^>]*>', '', v)

        print(f'{thread_attributes[k]}: {v}')


def download_thread(args, api_endpoint):
    # Format output directory string
    output_dir = os.path.join(args['output_dir'],
                              f'{args["board_id"]}_{args["thread_id"]}')

    # Format request URL
    request_url = re.sub('THREAD', args['thread_id'], api_endpoint)
    request_url = re.sub('BOARD', args['board_id'], request_url)

    # Fetch data from JSON API
    json_response = requests.get(request_url).json()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Convert JSON data to pandas DataFrame and export as CSV file
    df = pandas.json_normalize(json_response, record_path=['posts'])

    # Only save comments if current board length is longer than existing CSV file
    if os.path.exists(os.path.join(output_dir, 'comments.csv')):
        with open(os.path.join(output_dir, 'comments.csv'), 'r') as f:
            old_length = sum(1 for row in f) - 1
        current_length = len(df)
        if current_length > old_length:
            df.to_csv(f'{output_dir}/comments.csv')
            if current_length - old_length == 1:
                print(f'[+] Saved {current_length - old_length} new comment')
            else:
                print(f'[+] Saved {current_length - old_length} new comments')
    else:
        df.to_csv(f'{output_dir}/comments.csv')
        if len(df) == 1:
            print(f'[+] Saved {len(df)} comment')
        else:
            print(f'[+] Saved {len(df)} comments')

    # Save post attachments
    for post in json_response['posts']:
        if post.get('md5') is not None:
            # Format attachments variables
            attachments_dir = os.path.join(output_dir, 'attachments')
            attachment_url = f'https://i.4cdn.org/{args["board_id"]}/{post["tim"]}{post["ext"]}'
            attachment_name = f'{post["tim"]}{post["ext"]}'

            # Check if file exists
            if os.path.exists(os.path.join(attachments_dir, attachment_name)):
                continue

            # Create output directory
            os.makedirs(attachments_dir, exist_ok=True)

            # Download and save image
            with open(os.path.join(attachments_dir, attachment_name),
                      'wb') as f:
                f.write(requests.get(attachment_url).content)

            print(f'[+] Saved {attachment_name}')


def monitor_thread(args, api_endpoint):
    if args['monitor_thread'] is True:
        # Format request URL
        request_url = re.sub('THREAD', args['thread_id'], api_endpoint)
        request_url = re.sub('BOARD', args['board_id'], request_url)

        while True:
            # Fetch data from JSON API
            json_response = requests.get(request_url).json()

            if thread_closed(json_response):
                print(
                    f'Thread {args["thread_id"]} is marked as closed, ending script.'
                )
                break

            download_thread(args, api_endpoint)
            time.sleep(15)
    else:
        download_thread(args, api_endpoint)


def main():
    # Parse arguments into dictionary
    args = vars(parse_arguments())
    # Extract board and thread ID from URL and add to args dictionary
    args['board_id'], args['thread_id'] = parse_url(args['url'])

    # Display script arguments
    for k, v in args.items():
        print(f'{k + ":":25}{v}')
    line_break()

    # API Endpoints
    ## Archive: https://a.4cdn.org/BOARD/archive.json
    ## Boards: https://a.4cdn.org/boards.json
    ## Catalog: https://a.4cdn.org/BOARD/catalog.json
    ## Thread: https://a.4cdn.org/BOARD/thread/THREAD.json

    # Call function for appropriate action
    show_thread_details(args, 'https://a.4cdn.org/BOARD/thread/THREAD.json')
    line_break()
    monitor_thread(args, 'https://a.4cdn.org/BOARD/thread/THREAD.json')


if __name__ == '__main__':
    main()
