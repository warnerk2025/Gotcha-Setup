"""Public breach lookup helpers."""

import os

import aiohttp

from core.config import Config


class BreachChecker:
    def __init__(self, config: Config | None = None, logger=None):
        self.config = config or Config()
        self.logger = logger
        self._session = None

    async def check_breaches(self, email):
        session = await self._get_session()
        results = []
        hibp_key = os.getenv("HIBP_API_KEY")
        if hibp_key:
            results.extend(await self._check_hibp(session, email, hibp_key))
        else:
            results.append({
                "source": "Have I Been Pwned",
                "status": "unavailable",
                "details": "Set HIBP_API_KEY to enable authenticated HIBP queries.",
            })
        results.extend(await self._check_xposedornot(session, email))
        return results

    async def close_session(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _get_session(self):
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self._session = aiohttp.ClientSession(headers=self.config.headers, timeout=timeout)
        return self._session

    async def _check_hibp(self, session, email, api_key):
        headers = {
            **self.config.headers,
            "hibp-api-key": api_key,
            "user-agent": self.config.user_agent,
        }
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        try:
            async with session.get(url, headers=headers, params={"truncateResponse": "false"}, ssl=False) as response:
                if response.status == 404:
                    return [{"source": "Have I Been Pwned", "status": "not_found", "details": "No breaches reported by HIBP."}]
                if response.status == 200:
                    payload = await response.json()
                    return [
                        {
                            "source": "Have I Been Pwned",
                            "status": "found",
                            "breach": item.get("Name") or item.get("Title"),
                            "domain": item.get("Domain"),
                            "breach_date": item.get("BreachDate"),
                            "exposed_data": item.get("DataClasses", []),
                        }
                        for item in payload
                    ]
                return [{"source": "Have I Been Pwned", "status": "error", "details": f"HTTP {response.status}"}]
        except Exception as exc:
            return [{"source": "Have I Been Pwned", "status": "error", "details": str(exc)}]

    async def _check_xposedornot(self, session, email):
        url = f"https://api.xposedornot.com/v1/check-email/{email}"
        try:
            async with session.get(url, ssl=False) as response:
                if response.status == 404:
                    return [{"source": "XposedOrNot", "status": "not_found", "details": "No breach records were reported."}]
                if response.status != 200:
                    return [{"source": "XposedOrNot", "status": "error", "details": f"HTTP {response.status}"}]
                payload = await response.json(content_type=None)
        except Exception as exc:
            return [{"source": "XposedOrNot", "status": "error", "details": str(exc)}]

        breaches = payload.get("breaches") or payload.get("exposed_breaches") or payload.get("data") or []
        if isinstance(breaches, dict):
            breaches = [breaches]
        if not breaches:
            summary = payload.get("message") or payload.get("Message") or "No public breach records were reported."
            return [{"source": "XposedOrNot", "status": "not_found", "details": summary}]

        normalized = []
        for item in breaches:
            if isinstance(item, str):
                normalized.append({"source": "XposedOrNot", "status": "found", "breach": item})
                continue
            normalized.append(
                {
                    "source": "XposedOrNot",
                    "status": "found",
                    "breach": item.get("breach") or item.get("name") or item.get("Name"),
                    "domain": item.get("domain") or item.get("Domain"),
                    "breach_date": item.get("breach_date") or item.get("BreachDate"),
                    "exposed_data": item.get("exposed_data") or item.get("exposedData") or item.get("DataClasses") or [],
                }
            )
        return normalized
