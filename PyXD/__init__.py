import os

from PyXD.xdownloader import PyXDownloader
from PyXD.utility import Utility
from PyXD.exception import *
from argparse import ArgumentParser
from typing import Any


def main() -> Any:
    """
    PyXDownloader is an advanced tool developed using the Python programming language to assist users in downloading posts from Twitter. With a simple and user-friendly interface, PyXDownloader allows users to quickly and efficiently retrieve content such as tweets, images, and videos from specific Twitter accounts.

    Key features of PyXDownloader include:

        - User-Centric Downloads: Focuses on user-friendly content retrieval from specific Twitter accounts.
        - Efficient Python Usage: Built with the Python programming language, ensuring fast and efficient performance.
        - Intuitive Graphic Interface: A user-friendly interface design makes it easy for users to configure and execute downloads seamlessly.
        - Content Filtering Options: Enables users to customize downloads based on date, content type, or specific keywords.
        - Download History Management: Stores a history of downloads, allowing users to easily access and manage previously downloaded files.
        - Regular Update Support: Ensures the tool stays up-to-date with the latest changes or updates on the Twitter platform.

        PyXDownloader is the ideal solution for those seeking a reliable and efficient tool to gather and manage content from Twitter accounts within the trusted Python programming environment. Explore the world of Twitter more easily and effectively with PyXDownloader.

    Created and developed by @muhfalihr.
    """
    def path():
        script_path = os.path.realpath(__file__)
        path = '/'.join(os.path.dirname(script_path).split("/")[:-1])
        return path

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
        "-p", "--path", type=str, dest="path", help="Path where to save photos or videos.", default=Utility.downloadstorage()
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

    if args.cookie:
        Utility.addcookie(args.cookie, path())
    else:
        cookie = Utility.getcookie(path())
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
