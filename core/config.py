"""Configuration and platform definitions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Platform:
    name: str
    url: str
    category: str
    adult: bool = False


SOCIAL_MEDIA_PLATFORMS = [
    Platform("X", "https://x.com/{username}", "social_media"),
    Platform("Instagram", "https://instagram.com/{username}", "social_media"),
    Platform("Facebook", "https://facebook.com/{username}", "social_media"),
    Platform("TikTok", "https://www.tiktok.com/@{username}", "social_media"),
    Platform("YouTube", "https://www.youtube.com/@{username}", "social_media"),
    Platform("Reddit", "https://www.reddit.com/user/{username}", "social_media"),
    Platform("Pinterest", "https://www.pinterest.com/{username}", "social_media"),
    Platform("Threads", "https://www.threads.net/@{username}", "social_media"),
    Platform("Snapchat", "https://www.snapchat.com/add/{username}", "social_media"),
    Platform("Tumblr", "https://www.tumblr.com/{username}", "social_media"),
    Platform("Medium", "https://medium.com/@{username}", "social_media"),
    Platform("Vimeo", "https://vimeo.com/{username}", "social_media"),
    Platform("Flickr", "https://www.flickr.com/people/{username}", "social_media"),
    Platform("SoundCloud", "https://soundcloud.com/{username}", "social_media"),
    Platform("Telegram", "https://t.me/{username}", "social_media"),
    Platform("VK", "https://vk.com/{username}", "social_media"),
    Platform("Bluesky", "https://bsky.app/profile/{username}.bsky.social", "social_media"),
    Platform("Mastodon", "https://mastodon.social/@{username}", "social_media"),
    Platform("Linktree", "https://linktr.ee/{username}", "social_media"),
    Platform("Cash App", "https://cash.app/${username}", "social_media"),
    Platform("Rumble", "https://rumble.com/user/{username}", "social_media"),
    Platform("Last.fm", "https://www.last.fm/user/{username}", "social_media"),
    Platform("DeviantArt", "https://www.deviantart.com/{username}", "social_media"),
    Platform("Letterboxd", "https://letterboxd.com/{username}", "social_media"),
]

GENERAL_PLATFORMS = [
    Platform("About.me", "https://about.me/{username}", "general_sites"),
    Platform("Behance", "https://www.behance.net/{username}", "general_sites"),
    Platform("Buy Me a Coffee", "https://www.buymeacoffee.com/{username}", "general_sites"),
    Platform("Dribbble", "https://dribbble.com/{username}", "general_sites"),
    Platform("Etsy", "https://www.etsy.com/shop/{username}", "general_sites"),
    Platform("Gumroad", "https://gumroad.com/{username}", "general_sites"),
    Platform("Imgur", "https://imgur.com/user/{username}", "general_sites"),
    Platform("Instructables", "https://www.instructables.com/member/{username}", "general_sites"),
    Platform("Issuu", "https://issuu.com/{username}", "general_sites"),
    Platform("Ko-fi", "https://ko-fi.com/{username}", "general_sites"),
    Platform("Keybase", "https://keybase.io/{username}", "general_sites"),
    Platform("Patreon", "https://www.patreon.com/{username}", "general_sites"),
    Platform("Pastebin", "https://pastebin.com/u/{username}", "general_sites"),
    Platform("Product Hunt", "https://www.producthunt.com/@{username}", "general_sites"),
    Platform("Replit", "https://replit.com/@{username}", "general_sites"),
    Platform("SlideShare", "https://www.slideshare.net/{username}", "general_sites"),
    Platform("Scribd", "https://www.scribd.com/{username}", "general_sites"),
    Platform("Tripadvisor", "https://www.tripadvisor.com/members/{username}", "general_sites"),
    Platform("Canva", "https://www.canva.com/{username}", "general_sites"),
    Platform("Gravatar", "https://gravatar.com/{username}", "general_sites"),
    Platform("Wattpad", "https://www.wattpad.com/user/{username}", "general_sites"),
    Platform("Bandcamp", "https://bandcamp.com/{username}", "general_sites"),
]

DEVELOPER_PLATFORMS = [
    Platform("GitHub", "https://github.com/{username}", "developer_platforms"),
    Platform("GitLab", "https://gitlab.com/{username}", "developer_platforms"),
    Platform("Bitbucket", "https://bitbucket.org/{username}", "developer_platforms"),
    Platform("SourceForge", "https://sourceforge.net/u/{username}/profile", "developer_platforms"),
    Platform("Docker Hub", "https://hub.docker.com/u/{username}", "developer_platforms"),
    Platform("npm", "https://www.npmjs.com/~{username}", "developer_platforms"),
    Platform("PyPI", "https://pypi.org/user/{username}/", "developer_platforms"),
    Platform("RubyGems", "https://rubygems.org/profiles/{username}", "developer_platforms"),
    Platform("Packagist", "https://packagist.org/users/{username}", "developer_platforms"),
    Platform("crates.io", "https://crates.io/users/{username}", "developer_platforms"),
    Platform("Hugging Face", "https://huggingface.co/{username}", "developer_platforms"),
    Platform("Kaggle", "https://www.kaggle.com/{username}", "developer_platforms"),
    Platform("LeetCode", "https://leetcode.com/{username}", "developer_platforms"),
    Platform("CodePen", "https://codepen.io/{username}", "developer_platforms"),
    Platform("JSFiddle", "https://jsfiddle.net/user/{username}", "developer_platforms"),
    Platform("dev.to", "https://dev.to/{username}", "developer_platforms"),
    Platform("Hashnode", "https://hashnode.com/@{username}", "developer_platforms"),
    Platform("HackerOne", "https://hackerone.com/{username}", "developer_platforms"),
    Platform("Bugcrowd", "https://bugcrowd.com/{username}", "developer_platforms"),
    Platform("Codecademy", "https://www.codecademy.com/profiles/{username}", "developer_platforms"),
]

PROFESSIONAL_PLATFORMS = [
    Platform("LinkedIn", "https://www.linkedin.com/in/{username}", "professional_accounts"),
    Platform("Wellfound", "https://wellfound.com/u/{username}", "professional_accounts"),
    Platform("Xing", "https://www.xing.com/profile/{username}", "professional_accounts"),
    Platform("Polywork", "https://www.polywork.com/{username}", "professional_accounts"),
    Platform("ResearchGate", "https://www.researchgate.net/profile/{username}", "professional_accounts"),
    Platform("ORCID", "https://orcid.org/{username}", "professional_accounts"),
]

FORUM_PLATFORMS = [
    Platform("Quora", "https://www.quora.com/profile/{username}", "forums"),
    Platform("Disqus", "https://disqus.com/by/{username}", "forums"),
    Platform("freeCodeCamp Forum", "https://forum.freecodecamp.org/u/{username}", "forums"),
    Platform("DevRant", "https://devrant.com/users/{username}", "forums"),
    Platform("XDA", "https://forum.xda-developers.com/m/{username}", "forums"),
    Platform("Scratch", "https://scratch.mit.edu/users/{username}", "forums"),
    Platform("HN", "https://news.ycombinator.com/user?id={username}", "forums"),
    Platform("Spiceworks", "https://community.spiceworks.com/people/{username}", "forums"),
    Platform("MacRumors", "https://forums.macrumors.com/members/{username}", "forums"),
    Platform("RedFlagDeals", "https://forums.redflagdeals.com/memberlist.php?mode=viewprofile&u={username}", "forums"),
    Platform("MyAnimeList", "https://myanimelist.net/profile/{username}", "forums"),
    Platform("AniList", "https://anilist.co/user/{username}", "forums"),
]

GAMING_PLATFORMS = [
    Platform("Twitch", "https://www.twitch.tv/{username}", "gaming"),
    Platform("Steam", "https://steamcommunity.com/id/{username}", "gaming"),
    Platform("Chess.com", "https://www.chess.com/member/{username}", "gaming"),
    Platform("Lichess", "https://lichess.org/@/{username}", "gaming"),
    Platform("Faceit", "https://www.faceit.com/en/players/{username}", "gaming"),
    Platform("Speedrun.com", "https://www.speedrun.com/users/{username}", "gaming"),
    Platform("Roblox", "https://www.roblox.com/users/profile?username={username}", "gaming"),
    Platform("Planet Minecraft", "https://www.planetminecraft.com/member/{username}", "gaming"),
    Platform("Mod DB", "https://www.moddb.com/members/{username}", "gaming"),
    Platform("IGN", "https://www.ign.com/person/{username}", "gaming"),
    Platform("GOG", "https://www.gog.com/u/{username}", "gaming"),
    Platform("Nexus Mods", "https://www.nexusmods.com/users/{username}", "gaming"),
    Platform("Tracker.gg", "https://tracker.gg/{username}", "gaming"),
]

ADULT_SOCIAL_PLATFORMS = [
    Platform("OnlyFans", "https://onlyfans.com/{username}", "adult_platforms", adult=True),
    Platform("Chaturbate", "https://chaturbate.com/{username}", "adult_platforms", adult=True),
    Platform("CamSoda", "https://www.camsoda.com/{username}", "adult_platforms", adult=True),
    Platform("Cam4", "https://www.cam4.com/{username}", "adult_platforms", adult=True),
    Platform("Stripchat", "https://stripchat.com/{username}", "adult_platforms", adult=True),
    Platform("BongaCams", "https://bongacams.com/profile/{username}", "adult_platforms", adult=True),
    Platform("LiveJasmin", "https://www.livejasmin.com/en/profile/{username}", "adult_platforms", adult=True),
    Platform("MyFreeCams", "https://profiles.myfreecams.com/{username}", "adult_platforms", adult=True),
    Platform("JustForFans", "https://justfor.fans/{username}", "adult_platforms", adult=True),
    Platform("FetLife", "https://fetlife.com/users/{username}", "adult_platforms", adult=True),
    Platform("ManyVids", "https://www.manyvids.com/Profile/{username}", "adult_platforms", adult=True),
    Platform("iWantClips", "https://iwantclips.com/store/{username}", "adult_platforms", adult=True),
]

ADULT_GENERAL_PLATFORMS = [
    Platform("Pornhub", "https://www.pornhub.com/users/{username}", "adult_platforms", adult=True),
    Platform("XVideos", "https://www.xvideos.com/profiles/{username}", "adult_platforms", adult=True),
    Platform("RedTube", "https://www.redtube.com/users/{username}", "adult_platforms", adult=True),
    Platform("FapHouse", "https://faphouse.com/{username}", "adult_platforms", adult=True),
    Platform("Clips4Sale", "https://www.clips4sale.com/studio/{username}", "adult_platforms", adult=True),
    Platform("AdultFriendFinder", "https://adultfriendfinder.com/profile/{username}", "adult_platforms", adult=True),
    Platform("Seeking", "https://www.seeking.com/member/{username}", "adult_platforms", adult=True),
    Platform("Alt.com", "https://alt.com/profile/{username}", "adult_platforms", adult=True),
    Platform("Ashley Madison", "https://www.ashleymadison.com/profile/{username}", "adult_platforms", adult=True),
    Platform("Modelhub", "https://www.modelhub.com/{username}", "adult_platforms", adult=True),
]

ALL_PLATFORMS = {
    "social": SOCIAL_MEDIA_PLATFORMS,
    "general": GENERAL_PLATFORMS,
    "developer": DEVELOPER_PLATFORMS,
    "professional": PROFESSIONAL_PLATFORMS,
    "forums": FORUM_PLATFORMS,
    "gaming": GAMING_PLATFORMS,
    "adult_social": ADULT_SOCIAL_PLATFORMS,
    "adult_general": ADULT_GENERAL_PLATFORMS,
}

DISPOSABLE_DOMAINS = {
    "10minutemail.com",
    "guerrillamail.com",
    "mailinator.com",
    "temp-mail.org",
    "tempmail.com",
    "yopmail.com",
    "sharklasers.com",
    "trashmail.com",
    "getnada.com",
}


@dataclass
class Config:
    threads: int = 50
    timeout: int = 10
    user_agent: str = "Gotcha-Setup/1.0"

    @classmethod
    def from_args(cls, args):
        return cls(threads=args.threads, timeout=args.timeout)

    @property
    def headers(self):
        return {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def get_platforms(self, *groups, include_adult=False):
        platforms = []
        for group in groups:
            platforms.extend(ALL_PLATFORMS.get(group, []))
        if include_adult:
            for group in ("adult_social", "adult_general"):
                platforms.extend(ALL_PLATFORMS[group])
        return platforms
