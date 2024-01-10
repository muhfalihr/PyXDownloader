import re
import json
import requests

from requests.sessions import Session
from urllib.parse import urljoin, unquote, quote
from datetime import datetime
from PyXD.utility import Utility
from faker import Faker
from typing import Any
from tqdm import tqdm


class PyXDownloader:
    def __init__(self, cookie: str = None) -> Any:
        self.__cookie = cookie
        self.__session = Session()
        self.__fake = Faker()

        self.__headers = dict()
        self.__headers["Accept"] = "application/json, text/plain, */*"
        self.__headers["Accept-Language"] = "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        self.__headers["Sec-Fetch-Dest"] = "empty"
        self.__headers["Sec-Fetch-Mode"] = "cors"
        self.__headers["Sec-Fetch-Site"] = "same-site"
        self.__headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        if cookie is not None:
            self.__headers["Cookie"] = cookie

    def __guest_token(self):
        user_agent = self.__fake.user_agent()
        url = "https://api.twitter.com/1.1/guest/activate.json"
        self.__headers["User-Agent"] = user_agent
        resp = self.__session.post(
            url=url,
            headers=self.__headers,
            timeout=60
        )
        status_code = resp.status_code
        if status_code == 200:
            content = resp.json()["guest_token"]
            self.__headers.update({
                "X-Guest-Token": content
            })
            return self.__headers["X-Guest-Token"]
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")

    def __Csrftoken(self):
        pattern = re.compile(r'ct0=([a-zA-Z0-9_-]+)')
        matches = pattern.search(self.__cookie)
        if matches:
            csrftoken = matches.group(1)
            return csrftoken
        return None

    def __buildparams(self, **kwargs):
        func_name = kwargs["func_name"]
        match func_name:
            case "__profile":
                screen_name = kwargs["screen_name"]

                variables = {
                    "screen_name": screen_name.lower(),
                    "withSafetyModeUserFields": True
                }

                fieldToggles = {"withAuxiliaryUserLabels": False}

            case "__tweetdetail":
                focalTweetId = kwargs["focalTweetId"]
                controller_data = kwargs["controller_data"]
                cursor = kwargs["cursor"]

                variables = {
                    "focalTweetId": f"{focalTweetId}",
                    "cursor": f"{cursor}",
                    "referrer": "tweet",
                    "controller_data": f"{controller_data}",
                    "with_rux_injections": False,
                    "includePromotedContent": True,
                    "withCommunity": True,
                    "withQuickPromoteEligibilityTweetFields": True,
                    "withBirdwatchNotes": True,
                    "withVoice": True,
                    "withV2Timeline": True
                } if cursor else {
                    "focalTweetId": f"{focalTweetId}",
                    "with_rux_injections": False,
                    "includePromotedContent": True,
                    "withCommunity": True,
                    "withQuickPromoteEligibilityTweetFields": True,
                    "withBirdwatchNotes": True,
                    "withVoice": True,
                    "withV2Timeline": True
                }

                fieldToggles = {"withArticleRichContentState": False}

            case "allmedia" | "images":
                userId = kwargs["userId"]
                count = kwargs["count"]
                cursor = kwargs["cursor"]

                variables = {
                    "userId": f"{userId}",
                    "count": count,
                    "cursor": f"{cursor}",
                    "includePromotedContent": False,
                    "withClientEventToken": False,
                    "withBirdwatchNotes": False,
                    "withVoice": True,
                    "withV2Timeline": True
                } if cursor else {
                    "userId": f"{userId}",
                    "count": count,
                    "includePromotedContent": False,
                    "withClientEventToken": False,
                    "withBirdwatchNotes": False,
                    "withVoice": True,
                    "withV2Timeline": True
                }

        params = {
            "variables": variables,
            "features": {
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "rweb_video_timestamps_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_media_download_video_enabled": False,
                "responsive_web_enhance_cards_enabled": False
            } if func_name in [
                "allmedia", "images", "__tweetdetail"
            ] else {
                "hidden_profile_likes_enabled": True,
                "hidden_profile_subscriptions_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "subscriptions_verification_info_is_identity_verified_enabled": True,
                "subscriptions_verification_info_verified_since_enabled": True,
                "highlights_tweets_tab_ui_enabled": True,
                "responsive_web_twitter_article_notes_tab_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            }
        }
        if func_name in ["__profile", "__tweetdetail"]:
            params.update(
                {
                    "fieldToggles": fieldToggles
                }
            )

        return params

    def __profile(self, screen_name: str = None, proxy=None, **kwargs) -> dict:
        if not isinstance(screen_name, str):
            raise TypeError("Invalid parameter for 'profile'. Expected str, got {}".format(
                type(screen_name).__name__)
            )
        user_agent = self.__fake.user_agent()
        function_name = Utility.current_funcname()
        params = self.__buildparams(
            func_name=function_name,
            screen_name=screen_name
        )
        for key in params:
            params.update({key: Utility.convertws(params[key])})

        variables = quote(params["variables"])
        features = quote(params["features"])
        fieldToggles = quote(params["fieldToggles"])
        url = "https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName?variables={variables}&features={features}&fieldToggles={fieldToggles}".format(
            variables=variables,
            features=features,
            fieldToggles=fieldToggles
        )
        self.__headers["User-Agent"] = user_agent
        if self.__cookie is None:
            self.__headers["X-Guest-Token"] = self.__guest_token()
        else:
            self.__headers["X-Csrf-Token"] = self.__Csrftoken()
        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            proxies=proxy,
            headers=self.__headers,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            result = data["data"]["user"]["result"]
            rest_id = result["rest_id"]
            return rest_id
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")

    def __download(self, url: str):
        user_agent = self.__fake.user_agent()
        self.__headers["User-Agent"] = user_agent
        resp = self.__session.request(
            method="GET",
            url=url,
            headers=self.__headers,
            timeout=60
        )
        status_code = resp.status_code
        data = resp.content
        if status_code == 200:
            try:
                if ".mp4" in url:
                    pattern = re.compile(r'/([^/?]+)\?')
                    matches = pattern.search(url)
                    if matches:
                        filename = matches.group(1)
                else:
                    filename = url.split("/")[-1]
            except IndexError:
                filename = resp.headers.get("x-transaction-id")
            return data, filename
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")

    def __processmedia(self, tweet_results: dict, func_name: str):
        medias = []
        for media in tweet_results.get("entities", {}).get("media", []):
            media_type = media.get("type", "")

            match func_name:
                case "allmedia":
                    if media_type == "photo":
                        image = media.get("media_url_https", "")
                        medias.append(image)
                    if media_type == "video":
                        videos = max(media.get("video_info", {}).get(
                            "variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                        medias.append(videos)

                case "images":
                    if media_type == "photo":
                        image = media.get("media_url_https", "")
                        medias.append(image)

                case "__tweetdetail":
                    if media_type == "photo":
                        image = media.get("media_url_https", "")
                        medias.append(image)
                    elif media_type == "video":
                        videos = max(media.get("video_info", {}).get(
                            "variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                        medias.append(videos)

        return medias

    def allmedia(self, screen_name: str, path: str, count: int = 20, cursor: str = None, proxy=None, **kwargs) -> dict:
        Utility.mkdir(path=path)

        print(
            f"Downloading all media from Twitter users with the name @{screen_name}."
        )
        print(f"Saved in path: \"{path}\"")

        user_agent = self.__fake.user_agent()

        function_name = Utility.current_funcname()
        userId = self.__profile(screen_name=screen_name)
        params = self.__buildparams(
            func_name=function_name,
            userId=userId,
            count=count,
            cursor=cursor
        )

        for key in params:
            params.update({key: Utility.convertws(params[key])})

        variables = quote(params["variables"])
        features = quote(params["features"])
        url = "https://twitter.com/i/api/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia?variables={variables}&features={features}".format(
            variables=variables,
            features=features
        )
        self.__headers["User-Agent"] = user_agent
        if self.__cookie is None:
            self.__headers["X-Guest-Token"] = self.__guest_token()
        else:
            self.__headers["X-Csrf-Token"] = self.__Csrftoken()
        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            proxies=proxy,
            headers=self.__headers,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]

            medias = []
            for instruction in instructions:
                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":

                    cursor_value = ""
                    for entry in instruction.get("entries", []):
                        content = entry.get("content", {})
                        item_content = content.get("itemContent", {})

                        tweet_results = item_content.get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

                        items_content = content.get("items", {})

                        for item_content in items_content:
                            tweet_results = item_content.get(
                                "item", {}
                            ).get(
                                "itemContent", {}
                            ).get(
                                "tweet_results", {}
                            ).get(
                                "result", {}
                            ).get(
                                "legacy", {}
                            )

                            medias.extend(
                                self.__processmedia(
                                    tweet_results=tweet_results,
                                    func_name=function_name
                                )
                            )

                        cursor_value += content.get("value", "") if content.get(
                            "cursorType") == "Bottom" else ""

                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddToModule":

                    for entry in instruction.get("moduleItems", []):
                        tweet_results = entry.get(
                            "item", {}
                        ).get(
                            "itemContent", {}
                        ).get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

            for link in tqdm(medias, desc="Downloading"):
                try:
                    data_content, filename = self.__download(url=link)
                    with open(f"{path}/{filename}", "wb") as file:
                        file.write(data_content)
                except requests.RequestException:
                    pass
            print("DONE!!!🥳🥳🥳")
            print(f"Cursor value for next page \"{cursor_value}\"")
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")

    def images(self, screen_name: str, path: str, cursor: str = None, proxy=None, **kwargs) -> dict:
        Utility.mkdir(path=path)

        print(
            f"Downloading all image from Twitter users with the name @{screen_name}."
        )
        print(f"Saved in path: \"{path}\"")

        user_agent = self.__fake.user_agent()

        function_name = Utility.current_funcname()
        userId = self.__profile(screen_name=screen_name)
        params = self.__buildparams(
            func_name=function_name,
            userId=userId,
            count=20,
            cursor=cursor
        )

        for key in params:
            params.update({key: Utility.convertws(params[key])})

        variables = quote(params["variables"])
        features = quote(params["features"])
        url = "https://twitter.com/i/api/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia?variables={variables}&features={features}".format(
            variables=variables,
            features=features
        )
        self.__headers["User-Agent"] = user_agent
        if self.__cookie is None:
            self.__headers["X-Guest-Token"] = self.__guest_token()
        else:
            self.__headers["X-Csrf-Token"] = self.__Csrftoken()
        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            proxies=proxy,
            headers=self.__headers,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]

            medias = []
            for instruction in instructions:
                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":
                    cursor_value = ""

                    for entry in instruction.get("entries", []):
                        content = entry.get("content", {})
                        item_content = content.get("itemContent", {})

                        tweet_results = item_content.get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

                        items_content = content.get("items", {})

                        for item_content in items_content:
                            tweet_results = item_content.get(
                                "item", {}
                            ).get(
                                "itemContent", {}
                            ).get(
                                "tweet_results", {}
                            ).get(
                                "result", {}
                            ).get(
                                "legacy", {}
                            )

                            medias.extend(
                                self.__processmedia(
                                    tweet_results=tweet_results,
                                    func_name=function_name
                                )
                            )

                        cursor_value += content.get("value", "") if content.get(
                            "cursorType") == "Bottom" else ""

                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddToModule":

                    for entry in instruction.get("moduleItems", []):
                        tweet_results = entry.get(
                            "item", {}
                        ).get(
                            "itemContent", {}
                        ).get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )
                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

            for link in tqdm(medias, desc="Downlaoding"):
                try:
                    data_content, filename = self.__download(url=link)
                    with open(f"{path}/{filename}", "wb") as file:
                        file.write(data_content)
                except requests.RequestException:
                    pass
            print("DONE!!!🥳🥳🥳")
            print(f"Cursor value for next page \"{cursor_value}\"")
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")

    def __tweetdetail(
            self,
            focalTweetId: str | int,
            controller_data: str = "DAACDAABDAABCgABAAAAAAAAAAAKAAkXK+YwNdoAAAAAAAA=",
            cursor: str = None,
            proxy=None,
            **kwargs
    ):
        user_agent = self.__fake.user_agent()
        function_name = Utility.current_funcname()
        params = self.__buildparams(
            func_name=function_name,
            focalTweetId=focalTweetId,
            controller_data=controller_data,
            cursor=cursor
        )
        for key in params:
            params.update({key: Utility.convertws(params[key])})

        variables = quote(params["variables"])
        features = quote(params["features"])
        fieldToggles = quote(params["fieldToggles"])
        url = "https://twitter.com/i/api/graphql/-H4B_lJDEA-O_7_qWaRiyg/TweetDetail?variables={variables}&features={features}&fieldToggles={fieldToggles}".format(
            variables=variables,
            features=features,
            fieldToggles=fieldToggles
        )
        self.__headers["User-Agent"] = user_agent
        if self.__cookie is None:
            self.__headers["X-Guest-Token"] = self.__guest_token()
        else:
            self.__headers["X-Csrf-Token"] = self.__Csrftoken()
        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            proxies=proxy,
            headers=self.__headers,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            instructions = data["data"]["threaded_conversation_with_injections_v2"]["instructions"]
            medias = []

            for instruction in instructions:
                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":
                    for entry in instruction.get("entries", []):
                        content = entry.get("content", {})
                        item_content = content.get("itemContent", {})

                        tweet_results = item_content.get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

            return medias
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")

    def linkdownloader(self, link: str, path: str) -> Any:
        Utility.mkdir(path=path)

        print(
            f"Download media from the given link."
        )
        print(f"Saved in path: \"{path}\"")

        pattern = re.compile(r'/([^/?]+)\?')
        matches = pattern.search(string=link)
        if matches:
            focalTweetId = matches.group(1)

        medias = self.__tweetdetail(focalTweetId=focalTweetId)

        for media in tqdm(medias, desc="Downloading"):
            try:
                data_content, filename = self.__download(url=media)
                with open(f"{path}/{filename}", "wb") as file:
                    file.write(data_content)
            except requests.RequestException:
                pass
        print("DONE!!!🥳🥳🥳")


if __name__ == "__main__":
    cookie = ''
    sb = PyXDownloader(cookie=cookie)
