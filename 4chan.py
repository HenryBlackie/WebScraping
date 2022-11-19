import argparse
import html
import json
import os
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

    # Configure arguments
    parser.add_argument('-v',
                        '-verbose',
                        dest='verbose',
                        action='store_true',
                        help='Verbose logging to console. [Default: False]')
    parser.add_argument('-sB',
                        '--show-board',
                        type=str,
                        dest='show_board',
                        help='Display board information')

    # Parse, verify, and return user-provided arguments
    if len(sys.argv) < 2:
        # Print help message if no arguments provided and exit script
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()


def show_board(args, api_endpoints):
    # Get board details from JSON API
    json_response = requests.get(api_endpoints['boards']).json()

    # Extract board specific details from response
    try:
        board_dict = [
            details for details in json_response['boards']
            if details['board'] == args.show_board
        ][0]
    except IndexError as e:
        print(f'Error: Unable to find board "{args.show_board}"')
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


def main():
    args = parse_arguments()
    if args.verbose:
        print('Using arguments:')
        for argument, value in vars(args).items():
            if value is not None:
                print(f'{argument.title()}: {value}')
        line_break()

    # Specify API endpoints
    api_endpoints = {
        'archive': 'https://a.4cdn.org/BOARD/archive.json',
        'boards': 'https://a.4cdn.org/boards.json',
        'catalog': 'https://a.4cdn.org/BOARD/archive.json'
    }

    # Process actions
    if args.show_board is not None:
        show_board(args, api_endpoints)


if __name__ == '__main__':
    main()
