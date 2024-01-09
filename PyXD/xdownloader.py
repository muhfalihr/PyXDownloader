import re
import json
import requests

from requests.sessions import Session
from urllib.parse import urljoin, unquote, quote
from datetime import datetime
from utility import Utility
from faker import Faker
from typing import Any


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

        self.__generatekey = lambda datas, keys:  [
            key for key in datas if key in keys]

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
            case "search":
                rawquery = kwargs["rawquery"]
                count = kwargs["count"]
                cursor = kwargs["cursor"]
                product = kwargs["product"]

                variables = {
                    "rawQuery": f"{rawquery}",
                    "count": count,
                    "cursor": f"{cursor}",
                    "querySource": "typed_query",
                    "product": f"{product}"
                } if cursor else {
                    "rawQuery": f"{rawquery}",
                    "count": count,
                    "querySource": "typed_query",
                    "product": f"{product}"
                }

            case "__profile":
                screen_name = kwargs["screen_name"]

                variables = {
                    "screen_name": screen_name.lower(),
                    "withSafetyModeUserFields": True
                }

                fieldToggles = {"withAuxiliaryUserLabels": False}

            case "posts":
                userId = kwargs["userId"]
                count = kwargs["count"]
                cursor = kwargs["cursor"]

                variables = {
                    "userId": f"{userId}",
                    "count": count,
                    "cursor": f"{cursor}",
                    "includePromotedContent": True,
                    "withQuickPromoteEligibilityTweetFields": True,
                    "withVoice": True,
                    "withV2Timeline": True
                } if cursor else {
                    "userId": f"{userId}",
                    "count": count,
                    "includePromotedContent": True,
                    "withQuickPromoteEligibilityTweetFields": True,
                    "withVoice": True,
                    "withV2Timeline": True
                }

            case "media" | "likes":
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

            case "replies":
                userId = kwargs["userId"]
                count = kwargs["count"]
                cursor = kwargs["cursor"]

                variables = {
                    "userId": f"{userId}",
                    "count": count,
                    "cursor": f"{cursor}",
                    "includePromotedContent": True,
                    "withCommunity": True,
                    "withVoice": True,
                    "withV2Timeline": True
                } if cursor else {
                    "userId": f"{userId}",
                    "count": count,
                    "includePromotedContent": True,
                    "withCommunity": True,
                    "withVoice": True,
                    "withV2Timeline": True
                }

            case "recomendation":
                limit = kwargs["limit"]
                userId = kwargs["userId"]

            case "tweetdetail":
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

            case "following" | "followers" | "blue_verified_followers" | "followers_you_know":
                userId = kwargs["userId"]
                count = kwargs["count"]

                variables = {
                    "userId": f"{userId}",
                    "count": count,
                    "includePromotedContent": False
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
                "search", "posts", "media",
                "replies", "likes", "tweetdetail",
                "following", "followers", "blue_verified_followers",
                "followers_you_know"
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
        } if func_name != "recomendation" else {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "include_ext_is_blue_verified": 1,
            "include_ext_verified_type": 1,
            "include_ext_profile_image_shape": 1,
            "skip_status": 1,
            "pc": True,
            "display_location": "profile_accounts_sidebar",
            "limit": limit,
            "user_id": f"{userId}",
            "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl"
        }
        if func_name in ["__profile", "tweetdetail"]:
            params.update(
                {
                    "fieldToggles": fieldToggles
                }
            )

        return params

    def __replacechar(self, text: str, replacement: str):
        if not isinstance(text, str):
            raise TypeError("Invalid parameter for '__replacechar'. Expected str, got {}".format(
                type(text).__name__)
            )
        if not isinstance(replacement, str):
            raise TypeError("Invalid parameter for '__replacechar'. Expected str, got {}".format(
                type(replacement).__name__)
            )

        pattern = re.compile(r'_(.*?)\.jpg')
        matches = pattern.search(
            string=text.split("/")[-1]
        )
        if matches:
            replace = matches.group(1)
            result = text.replace(replace, replacement)
            return result
        return text

    def __processmedia(self, entry: dict = None) -> dict:
        """
        Process media entry data and return a cleaned dictionary.
        """
        if not isinstance(entry, dict):
            raise TypeError("Invalid parameter for '__processmedia'. Expected dict, got {}".format(
                type(entry).__name__)
            )

        if "content" in entry:
            deeper = entry["content"]["itemContent"]["tweet_results"]["result"]
        else:
            if "rest_id" in entry:
                deeper = entry
            else:
                deeper = entry["tweet"]

        if "legacy" in deeper:
            legacy = deeper["legacy"]
            medias = [
                media["media_url_https"] if "video_info" not in media else max(
                    media["video_info"]["variants"], key=lambda x: x.get(
                        "bitrate", 0
                    )
                ).get("url", "")
                for media in legacy["entities"]["media"]
            ]
            return medias

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

    def media(self, screen_name: str, count: int = 20, cursor: str = None, proxy=None, **kwargs) -> dict:
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
            for index, value in enumerate(instructions):
                if isinstance(value, dict) and value["type"] == "TimelineAddEntries":
                    deep = instructions[index]

                    cursor_value = ""
                    for entry in deep["entries"]:
                        for key in entry:
                            if key == "content":
                                for key_content in entry[key]:
                                    if key_content == "itemContent":
                                        if "tweet_results" in entry[key][key_content]:
                                            tweet_results = entry[key][key_content]["tweet_results"]["result"]
                                            twr = self.__processmedia(
                                                entry=tweet_results)
                                            medias.extend(twr)
                                    if key_content == "items":
                                        for item in entry[key][key_content]:
                                            if "tweet_results" in item["item"]["itemContent"]:
                                                tweet_results = item["item"]["itemContent"]["tweet_results"]["result"]
                                                twr = self.__processmedia(
                                                    entry=tweet_results)
                                                medias.extend(twr)
                                if entry[key].get("cursorType", "") == "Bottom":
                                    cursor_value += entry[key].get(
                                        "value", ""
                                    )

                if isinstance(value, dict) and value["type"] == "TimelineAddToModule":
                    deep = instructions[index]

                    for entry in deep["moduleItems"]:
                        if "item" in entry:
                            deeper = entry["item"]["itemContent"]["tweet_results"]["result"]
                            tweet_results = self.__processmedia(
                                entry=deeper
                            )
                            medias.extend(tweet_results)

            for link in medias:
                try:
                    data_content, filename = self.__download(url=link)
                    with open(f"data/{filename}", "wb") as file:
                        file.write(data_content)
                except requests.RequestException:
                    pass
            print(cursor_value)
        else:
            raise Exception(
                f"Error! status code {resp.status_code} : {resp.reason}")


if __name__ == "__main__":
    cookie = ''
    sb = PyXDownloader(cookie=cookie)
