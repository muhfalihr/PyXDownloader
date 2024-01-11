#!/usr/bin/env python3

from PyXD.xdownloader import PyXDownloader
from argparse import ArgumentParser

if __name__ == "__main__":
    argument_parser = ArgumentParser(
        description="PyXDownloader is a tool used to download media from a specified username or link."
    )
    argument_parser.add_argument(
        "-f", "--function", type=str, dest="function", help="allmedia, images, linkdownloader", default="allmedia"
    )
    argument_parser.add_argument(
        "-link", "--link", type=str, dest="link", help="Image or video link."
    )
    argument_parser.add_argument(
        "-p", "--path", type=str, dest="path", help="Path where to save photos or videos."
    )
    argument_parser.add_argument(
        "-sn", "--screenname", type=str, dest="screenname", help="Example: @AM_EllaJKT48 but not included @."
    )
    argument_parser.add_argument(
        "-count", "--count", type=int, dest="count", help="The amount of data to be downloaded.", default=20
    )
    argument_parser.add_argument(
        "-cursor", "--cursor", type=str, dest="cursor", help="The key used to load the next page.", default=None
    )

    args = argument_parser.parse_args()

    cookie = ''  # Required
    PXD = PyXDownloader(cookie=cookie)

    match args.function:
        case "allmedia":
            PXD.allmedia(
                screen_name=args.screenname,
                path=args.path,
                count=args.count,
                cursor=args.cursor
            )

        case "images":
            PXD.images(
                screen_name=args.screenname,
                path=args.path,
                cursor=args.cursor
            )

        case "linkdownloader":
            PXD.linkdownloader(
                link=args.link,
                path=args.path
            )
