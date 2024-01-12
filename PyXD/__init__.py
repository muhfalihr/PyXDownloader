import os

from PyXD.xdownloader import PyXDownloader
from PyXD.utility import Utility
from PyXD.exception import *
from argparse import ArgumentParser


def main():
    argument_parser = ArgumentParser(
        description="PyXDownloader is a tool used to download media from a specified username or link."
    )
    argument_parser.add_argument(
        "-func", "--function", type=str, dest="function", help="\"am | allmedia\", \"i | images\", \"ld | linkdownloader\""
    )
    argument_parser.add_argument(
        "-link", "--link", type=str, dest="link", help="Image or video link."
    )
    argument_parser.add_argument(
        "-p", "--path", type=str, dest="path", help="Path where to save photos or videos."
    )
    argument_parser.add_argument(
        "-sn", "--screenname", type=str, dest="screenname", help="Example: @screen_name but not included @."
    )
    argument_parser.add_argument(
        "-count", "--count", type=int, dest="count", help="The amount of data to be downloaded.", default=20
    )
    argument_parser.add_argument(
        "-cursor", "--cursor", type=str, dest="cursor", help="The key used to load the next page.", default=None
    )
    argument_parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0'
    )
    argument_parser.add_argument(
        "-cookie", "--cookie", type=str, dest="cookie", help="Enter your Twitter browser cookies."
    )

    args = argument_parser.parse_args()

    script_path = os.path.realpath(__file__)
    path = '/'.join(os.path.dirname(script_path).split("/")[:-1])

    if args.cookie:
        Utility.addcookie(args.cookie, path)

    else:
        cookie = Utility.getcookie(path)
        PXD = PyXDownloader(cookie=cookie)

        match args.function:
            case "allmedia" | "am":
                PXD.allmedia(
                    screen_name=args.screenname,
                    path=args.path,
                    count=args.count,
                    cursor=args.cursor
                )

            case "images" | "i":
                PXD.images(
                    screen_name=args.screenname,
                    path=args.path,
                    cursor=args.cursor
                )

            case "linkdownloader" | "ld":
                PXD.linkdownloader(
                    link=args.link,
                    path=args.path
                )

            case _:
                raise FunctionNotFoundError(
                    f"Error! The function with the name '{args.function}' is not available."
                )
