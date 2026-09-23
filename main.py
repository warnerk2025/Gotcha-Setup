#!/usr/bin/env python3
"""Gotcha! - Advanced Username & Email OSINT Tool."""

import argparse
import asyncio
import sys
import warnings
from pathlib import Path

from colorama import init as colorama_init

from core.banner import print_banner
from core.config import Config
from core.logger import setup_logger
from engines.breach_checker import BreachChecker
from engines.email_hunter import EmailHunter
from engines.social_media import SocialMediaHunter
from engines.username_hunter import UsernameHunter
from utils.reporter import Reporter
from utils.validator import Validator

warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*")
warnings.filterwarnings("ignore", category=ResourceWarning, message=".*client_session.*")
warnings.filterwarnings("ignore", category=ResourceWarning, message=".*connector.*")


class Gotcha:
    def __init__(self, config: Config, quiet: bool = False):
        self.config = config
        self.logger = setup_logger(quiet=quiet)
        self.reporter = Reporter()

    async def run_username_scan(self, username, options):
        """Run comprehensive username reconnaissance."""
        if not Validator.is_valid_username(username):
            self.logger.error("Invalid username: %s", username)
            return None

        self.logger.info("Starting username scan for: %s", username)
        username_hunter = UsernameHunter(self.config, self.logger)
        social_hunter = SocialMediaHunter(self.config, self.logger)

        tasks = {}
        if options.social:
            tasks["social_media"] = social_hunter.hunt_username(username, include_adult=False)
        if options.general:
            tasks["general_sites"] = username_hunter.hunt_general_sites(username, include_adult=False)
        if options.developer:
            tasks["developer_platforms"] = username_hunter.hunt_developer_platforms(username)
        if options.forums:
            tasks["forums"] = username_hunter.hunt_forums(username)
        if options.gaming:
            tasks["gaming"] = username_hunter.hunt_gaming_platforms(username)
        if options.adult:
            tasks["adult_platforms"] = username_hunter.hunt_adult_platforms(username)

        gathered = await asyncio.gather(*tasks.values()) if tasks else []
        results = {
            "target_type": "username",
            "username": username,
            "social_media": [],
            "general_sites": [],
            "developer_platforms": [],
            "forums": [],
            "gaming": [],
            "adult_platforms": [],
            "misc": [],
        }
        for key, value in zip(tasks.keys(), gathered):
            results[key] = value
        return results

    async def run_email_scan(self, email, options):
        """Run comprehensive email reconnaissance."""
        if not Validator.is_valid_email(email):
            self.logger.error("Invalid email format: %s", email)
            return None

        self.logger.info("Starting email scan for: %s", email)
        email_hunter = EmailHunter(self.config, self.logger)
        breach_checker = BreachChecker(self.config, self.logger)

        tasks = {}
        if options.breaches:
            tasks["breaches"] = breach_checker.check_breaches(email)
        if options.social:
            tasks["social_accounts"] = email_hunter.hunt_social_accounts(email, include_adult=options.adult)
        if options.professional:
            tasks["professional_accounts"] = email_hunter.hunt_professional_accounts(email)
        if options.domain:
            tasks["domain_info"] = email_hunter.analyze_domain(email)

        try:
            gathered = await asyncio.gather(*tasks.values()) if tasks else []
        finally:
            await email_hunter.close_session()
            await breach_checker.close_session()

        results = {
            "target_type": "email",
            "email": email,
            "breaches": [],
            "social_accounts": [],
            "professional_accounts": [],
            "domain_info": {},
        }
        for key, value in zip(tasks.keys(), gathered):
            results[key] = value
        return results


async def run_scan(args):
    config = Config.from_args(args)
    gotcha = Gotcha(config, quiet=args.quiet)
    results = []

    async def process_target(target):
        if Validator.is_valid_email(target):
            return await gotcha.run_email_scan(target, args)
        return await gotcha.run_username_scan(target, args)

    if args.file:
        input_file = Path(args.file)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        targets = [line.strip() for line in input_file.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
        for target in targets:
            result = await process_target(target)
            if result:
                results.append(result)
    else:
        target_tasks = []
        if args.username:
            target_tasks.append(gotcha.run_username_scan(args.username, args))
        if args.email:
            target_tasks.append(gotcha.run_email_scan(args.email, args))
        for result in await asyncio.gather(*target_tasks):
            if result:
                results.append(result)

    if results:
        if args.output:
            gotcha.reporter.save_report(results, args.output, args.format)
        else:
            gotcha.reporter.print_report(results, quiet=args.quiet)
    else:
        gotcha.logger.warning("No results were collected.")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Gotcha! - Advanced Username & Email OSINT Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -u john_doe --social --developer
  %(prog)s -e john@example.com --breaches --domain
  %(prog)s -u username -e email@domain.com --all
  %(prog)s -u username --social --adult
  %(prog)s -f targets.txt --all -o report.json --format json

Note: adult/NSFW platforms are only queried when --adult is provided.
        """,
    )
    parser.add_argument("-u", "--username", help="Target username")
    parser.add_argument("-e", "--email", help="Target email address")
    parser.add_argument("-f", "--file", help="File containing usernames/emails (one per line)")

    parser.add_argument("--social", action="store_true", help="Search social media platforms")
    parser.add_argument("--general", action="store_true", help="Search general websites")
    parser.add_argument("--developer", action="store_true", help="Search developer platforms")
    parser.add_argument("--forums", action="store_true", help="Search forums and communities")
    parser.add_argument("--gaming", action="store_true", help="Search gaming platforms")
    parser.add_argument("--breaches", action="store_true", help="Check for public breach exposure records")
    parser.add_argument("--professional", action="store_true", help="Search professional networks from email local-parts")
    parser.add_argument("--domain", action="store_true", help="Analyze email domain configuration")
    parser.add_argument("--adult", action="store_true", help="Opt-in to adult/NSFW platform checks (18+)")
    parser.add_argument("--all", action="store_true", help="Enable all non-adult search modules")

    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--format", choices=["json", "csv", "txt"], default="json", help="Output format")
    parser.add_argument("--quiet", action="store_true", help="Suppress the banner and most log output")
    parser.add_argument("--threads", type=int, default=50, help="Maximum concurrent requests (default: 50)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    return parser


def main():
    colorama_init(autoreset=True)
    parser = build_parser()
    args = parser.parse_args()

    if not any([args.username, args.email, args.file]):
        parser.error("At least one target must be specified: -u/--username, -e/--email, or -f/--file")
    if args.username and not Validator.is_valid_username(args.username):
        parser.error("Username contains unsupported characters")
    if args.email and not Validator.is_valid_email(args.email):
        parser.error("Email address format is invalid")
    if args.threads < 1:
        parser.error("--threads must be greater than 0")
    if args.timeout < 1:
        parser.error("--timeout must be greater than 0")

    if args.all:
        args.social = True
        args.general = True
        args.developer = True
        args.forums = True
        args.gaming = True
        args.breaches = True
        args.professional = True
        args.domain = True

    if not any([args.social, args.general, args.developer, args.forums, args.gaming, args.breaches, args.professional, args.domain, args.adult]):
        parser.error("At least one scan option must be specified (or use --all)")

    if not args.quiet:
        print_banner()

    try:
        asyncio.run(run_scan(args))
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
