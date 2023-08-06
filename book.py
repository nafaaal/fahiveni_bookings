from playwright.sync_api import Playwright, sync_playwright, expect
import time, json
from datetime import date

TIMES = {
    "10am": "10:0011:00",
    "11am": "11:0012:00",
    "12pm": "12:0013:00",
    "1pm": "13:0014:00",
    "2pm": "14:0015:00",
    "3pm": "15:0016:00",
    "4pm": "16:0017:00",
    "5pm": "17:0018:00",
    "6pm": "18:0019:00",
    "7pm": "19:0020:00",
    "8pm": "20:0021:00",
    "9pm": "21:0022:00",
    "10pm": "22:0023:00",
}

COURTS = {
    "c1" : "https://ems.urbanco.mv/spaces/51f0b555-4de6-4160-7a33-08d81366a016",
    "c2" : "https://ems.urbanco.mv/spaces/810f69b6-fd1e-41ec-af95-08d814e092f5"
}

CURRENT_DATE = date.today().strftime("%d/%m/%Y")
BOOKED = False

def book(page):
    with open('info.json', 'r') as f:
        data = json.load(f)

        page.goto(COURTS[data["court"]])
        page.get_by_placeholder("Search for any service you prefer").click()
        page.get_by_placeholder("Search for any service you prefer").fill("badminton")
        page.get_by_text("Fahiveni").click()
        page.get_by_text("Sports and Leisure").click()
        page.get_by_text("Fahiveni Community Center").first.click()
        page.get_by_text("Badminton Court 1").click()
        time.sleep(1)

        global BOOKED
        while not BOOKED:
            page.locator("section").filter(has_text=f"Badminton Court 1Date{CURRENT_DATE} Change dates RateMVR 51 / hourPlease select a ti").locator("svg").nth(3).click() #switch to next date
            time.sleep(2) # can make lower but will be buggy if time slot is availible for current day
            if page.get_by_text(TIMES[data["time"]]).is_visible():
                print("IS VISIBLE")
                page.get_by_text(TIMES[data["time"]]).click()
                page.get_by_label("Name").click()
                page.get_by_label("Name").fill(data["name"])
                page.get_by_label("Email").click()
                page.get_by_label("Email").fill(data["email"])
                page.get_by_role("button", name="Submit").click()
                time.sleep(600)
                BOOKED = True
            else:
                print("NOT VISIBLE")
                page.reload()


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    with open("cookies.json", "r") as f:
        cookies = json.loads(f.read())
        context.add_cookies(cookies)

    book(page)

    context.close()
    browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()


