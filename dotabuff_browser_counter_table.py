import argparse
import csv
import time
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from heores_list import heroes_list, normalize_hero_name


DOTABUFF_COUNTERS_URL = "https://www.dotabuff.com/heroes/{hero}/counters"
CHALLENGE_MARKERS = (
    "verify you are human",
    "checking your browser",
    "just a moment...",
    "ray id",
)


def build_url(hero, date):
    url = DOTABUFF_COUNTERS_URL.format(hero=normalize_hero_name(hero))
    if date:
        url += f"?date={date}"
    return url


def create_driver(profile_dir=None, headless=False, debugger_address=None):
    options = Options()
    options.add_argument("--start-maximized")

    if debugger_address:
        options.add_experimental_option("debuggerAddress", debugger_address)

    if profile_dir:
        options.add_argument(f"--user-data-dir={profile_dir}")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,1000")

    return webdriver.Chrome(options=options)


def wait_for_counter_table(driver, timeout):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table"))
    )
    WebDriverWait(driver, timeout).until(
        lambda browser: len(browser.find_elements(By.CSS_SELECTOR, "table")) >= 3
    )


def is_verification_page(driver):
    if len(driver.find_elements(By.CSS_SELECTOR, "table")) >= 3:
        return False

    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    except WebDriverException:
        body_text = ""

    title = driver.title.lower()
    current_url = driver.current_url.lower()

    if "cdn-cgi/challenge-platform" in current_url:
        return True

    return any(marker in body_text or marker in title for marker in CHALLENGE_MARKERS)


def wait_through_verification(driver, hero, challenge_timeout, headless):
    if not is_verification_page(driver):
        return

    if headless:
        raise TimeoutException(
            "Dotabuff opened a human verification page. Re-run without --headless "
            "so you can complete it in Chrome."
        )

    print("")
    print(f"human verification detected while loading {hero}")
    print("Complete the check in the opened Chrome window. The script will continue after the page clears.")

    end_time = time.monotonic() + challenge_timeout
    while time.monotonic() < end_time:
        if not is_verification_page(driver):
            print("verification cleared")
            return
        time.sleep(2)

    raise TimeoutException(
        f"verification did not clear within {int(challenge_timeout)} seconds for {hero}"
    )


def parse_counter_page(html, hero):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    if len(tables) < 3:
        raise ValueError(f"counter table not found for {hero}")

    rows = tables[2].find_all("tr")
    advantage_res = [hero] + [0] * len(heroes_list)

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        name = cols[0].get("data-value", "").lower()
        if name not in heroes_list:
            continue

        try:
            advantage = Decimal(cols[2]["data-value"]).quantize(Decimal(".01"))
        except (KeyError, InvalidOperation):
            continue

        index = heroes_list.index(name) + 1
        advantage_res[index] = str(advantage)

    return advantage_res


def counter_table(
    output_path="disadvantage.csv",
    date="month",
    delay=3,
    timeout=30,
    challenge_timeout=300,
    start=None,
    limit=None,
    profile_dir=None,
    headless=False,
    debugger_address=None,
):
    selected_heroes = heroes_list
    if start:
        if start not in heroes_list:
            raise ValueError(f"unknown start hero: {start}")
        selected_heroes = selected_heroes[heroes_list.index(start) :]
    if limit:
        selected_heroes = selected_heroes[:limit]

    driver = create_driver(
        profile_dir=profile_dir,
        headless=headless,
        debugger_address=debugger_address,
    )

    try:
        with open(output_path, "w", newline="", encoding="utf-8") as disadvantage_file:
            disadvantage_writer = csv.writer(disadvantage_file, delimiter=" ")
            disadvantage_writer.writerow([""] + heroes_list)

            for hero in selected_heroes:
                url = build_url(hero, date)
                print(f"open {hero}: {url}")

                try:
                    driver.get(url)
                    wait_through_verification(driver, hero, challenge_timeout, headless)
                    wait_for_counter_table(driver, timeout)
                    row = parse_counter_page(driver.page_source, hero)
                except TimeoutException:
                    print(f"timeout waiting for table: {hero}")
                    continue
                except WebDriverException as exc:
                    print(f"browser error for {hero}: {exc}")
                    continue
                except ValueError as exc:
                    print(exc)
                    continue

                disadvantage_writer.writerow(row)
                disadvantage_file.flush()
                print(f"finish {hero}")
                time.sleep(delay)
    finally:
        if not debugger_address:
            driver.quit()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build Dotabuff counter table by loading pages in a real browser."
    )
    parser.add_argument("--output", default="disadvantage.csv")
    parser.add_argument("--date", default="")
    parser.add_argument("--delay", type=float, default=3)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument(
        "--challenge-timeout",
        type=float,
        default=300,
        help="seconds to wait while you complete a browser verification page",
    )
    parser.add_argument("--start", help="resume from this hero name, for example: axe")
    parser.add_argument("--limit", type=int, help="only process this many heroes")
    parser.add_argument(
        "--profile-dir",
        help="Chrome user data directory to reuse your normal browser session/cookies.",
    )
    parser.add_argument(
        "--debugger-address",
        help="attach to an already-open Chrome, for example: 127.0.0.1:9222",
    )
    parser.add_argument("--headless", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    counter_table(
        output_path=args.output,
        date=args.date,
        delay=args.delay,
        timeout=args.timeout,
        challenge_timeout=args.challenge_timeout,
        start=args.start,
        limit=args.limit,
        profile_dir=args.profile_dir,
        headless=args.headless,
        debugger_address=args.debugger_address,
    )
