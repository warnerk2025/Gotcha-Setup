"""Email reconnaissance engine."""

import hashlib

import aiohttp
import dns.resolver

from core.config import Config, DISPOSABLE_DOMAINS
from engines.social_media import SocialMediaHunter
from engines.username_hunter import UsernameHunter
from utils.validator import Validator


class EmailHunter:
    def __init__(self, config: Config | None = None, logger=None):
        self.config = config or Config()
        self.logger = logger
        self._session = None

    async def hunt_social_accounts(self, email):
        results = await self._hunt_social_local_part(email)
        gravatar = await self._check_gravatar(email)
        if gravatar:
            results.append(gravatar)
        return results

    async def hunt_general_sites(self, email):
        return await self._hunt_username_group(email, "general")

    async def hunt_developer_accounts(self, email):
        return await self._hunt_username_group(email, "developer")

    async def hunt_forum_accounts(self, email):
        return await self._hunt_username_group(email, "forums")

    async def hunt_gaming_accounts(self, email):
        return await self._hunt_username_group(email, "gaming")

    async def hunt_professional_accounts(self, email):
        return await self._hunt_username_group(email, "professional")

    async def analyze_domain(self, email):
        domain = email.split("@", 1)[1].lower()
        info = {
            "domain": domain,
            "disposable": domain in DISPOSABLE_DOMAINS,
            "mx_records": self._resolve(domain, "MX"),
            "ns_records": self._resolve(domain, "NS"),
            "txt_records": self._resolve(domain, "TXT"),
            "spf": [],
            "dmarc": self._resolve(f"_dmarc.{domain}", "TXT"),
            "has_website": False,
        }
        info["spf"] = [record for record in info["txt_records"] if "v=spf1" in record.lower()]
        info["has_website"] = await self._check_website(domain)
        return info

    async def close_session(self):
        if self._session and not self._session.closed:
            await self._session.close()

    def _resolve(self, target, record_type):
        try:
            answers = dns.resolver.resolve(target, record_type, lifetime=self.config.timeout)
            return [str(answer).strip('"') for answer in answers]
        except Exception:
            return []

    async def _get_session(self):
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self._session = aiohttp.ClientSession(headers=self.config.headers, timeout=timeout)
        return self._session

    async def _check_gravatar(self, email):
        digest = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
        url = f"https://www.gravatar.com/avatar/{digest}?d=404"
        session = await self._get_session()
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return {
                        "platform": "Gravatar",
                        "category": "social_media",
                        "adult": False,
                        "url": url,
                        "status": "found",
                        "http_status": 200,
                    }
        except Exception:
            return None
        return None

    async def _hunt_social_local_part(self, email):
        local_part = self._get_local_part_username(email)
        if not local_part:
            return []
        hunter = SocialMediaHunter(self.config, self.logger)
        return await hunter.hunt_username(local_part)

    async def _hunt_username_group(self, email, group):
        local_part = self._get_local_part_username(email)
        if not local_part:
            return []
        hunter = UsernameHunter(self.config, self.logger)
        method_map = {
            "general": hunter.hunt_general_sites,
            "developer": hunter.hunt_developer_platforms,
            "forums": hunter.hunt_forums,
            "gaming": hunter.hunt_gaming_platforms,
            "professional": hunter.hunt_professional_platforms,
        }
        return await method_map[group](local_part)

    @staticmethod
    def _get_local_part_username(email):
        local_part = email.split("@", 1)[0]
        if not Validator.is_valid_username(local_part):
            return None
        return local_part

    async def _check_website(self, domain):
        session = await self._get_session()
        for scheme in ("https", "http"):
            try:
                async with session.get(f"{scheme}://{domain}") as response:
                    if response.status < 500:
                        return True
            except Exception:
                continue
        return False
