"""Username reconnaissance engine."""

import asyncio

import aiohttp

from core.config import Config


NEGATIVE_MARKERS = (
    "not found",
    "page not found",
    "doesn't exist",
    "does not exist",
    "unavailable",
    "sorry, this page",
    "this account doesn't exist",
    "user not found",
)


class UsernameHunter:
    def __init__(self, config: Config | None = None, logger=None):
        self.config = config or Config()
        self.logger = logger
        self.semaphore = asyncio.Semaphore(self.config.threads)

    async def hunt_general_sites(self, username, include_adult=False):
        return await self._scan_platforms(username, self.config.get_platforms("general", include_adult=include_adult))

    async def hunt_developer_platforms(self, username):
        return await self._scan_platforms(username, self.config.get_platforms("developer"))

    async def hunt_forums(self, username):
        return await self._scan_platforms(username, self.config.get_platforms("forums"))

    async def hunt_gaming_platforms(self, username):
        return await self._scan_platforms(username, self.config.get_platforms("gaming"))

    async def hunt_adult_platforms(self, username):
        return await self._scan_platforms(username, self.config.get_platforms("adult_social", "adult_general"), positive_only=False)

    async def _scan_platforms(self, username, platforms, positive_only=True):
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        async with aiohttp.ClientSession(headers=self.config.headers, timeout=timeout) as session:
            tasks = [self._check_platform(session, username, platform) for platform in platforms]
            results = await asyncio.gather(*tasks)
        filtered = [result for result in results if result]
        if positive_only:
            filtered = [result for result in filtered if result["status"] in {"found", "possible"}]
        return sorted(filtered, key=lambda item: (item["status"] != "found", item["platform"]))

    async def _check_platform(self, session, username, platform):
        url = platform.url.format(username=username)
        async with self.semaphore:
            try:
                async with session.get(url, allow_redirects=True, ssl=False) as response:
                    text = await response.text(errors="ignore")
                    status = self._classify_response(response.status, text)
                    if status == "not_found":
                        return None
                    return {
                        "platform": platform.name,
                        "category": platform.category,
                        "adult": platform.adult,
                        "url": str(response.url),
                        "status": status,
                        "http_status": response.status,
                    }
            except asyncio.TimeoutError:
                return {
                    "platform": platform.name,
                    "category": platform.category,
                    "adult": platform.adult,
                    "url": url,
                    "status": "timeout",
                    "http_status": None,
                }
            except aiohttp.ClientError as exc:
                if self.logger:
                    self.logger.debug("%s check failed: %s", platform.name, exc)
                return {
                    "platform": platform.name,
                    "category": platform.category,
                    "adult": platform.adult,
                    "url": url,
                    "status": "error",
                    "http_status": None,
                    "details": str(exc),
                }

    @staticmethod
    def _classify_response(http_status, body):
        lowered = body.lower()
        if http_status == 404:
            return "not_found"
        if http_status in {200, 201}:
            if any(marker in lowered for marker in NEGATIVE_MARKERS):
                return "not_found"
            return "found"
        if http_status in {401, 403, 405, 429}:
            return "possible"
        if http_status in {301, 302, 307, 308}:
            return "possible"
        return "possible" if http_status and http_status < 500 else "error"
