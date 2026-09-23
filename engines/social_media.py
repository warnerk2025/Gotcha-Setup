"""Social media scanning engine."""

from core.config import Config
from engines.username_hunter import UsernameHunter


class SocialMediaHunter(UsernameHunter):
    def __init__(self, config: Config | None = None, logger=None):
        super().__init__(config=config, logger=logger)

    async def hunt_username(self, username, include_adult=False):
        platforms = self.config.get_platforms("social", include_adult=False)
        results = await self._scan_platforms(username, platforms)
        unique = {(item["platform"], item["url"]): item for item in results}
        return sorted(unique.values(), key=lambda item: item["platform"])
