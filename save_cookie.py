from playwright.sync_api import Playwright, sync_playwright
import time, json

def save_cookie(page, context):
    with open('info.json', 'r') as f:
        data = json.load(f)

        page.goto("https://my.urbanco.mv/")
        page.get_by_role("link", name="Login").click()
        page.get_by_role("button", name="eFaas").click()
        time.sleep(10)
        page.get_by_role("tab", name="Password Login").click()
        page.get_by_role("tab", name="Password Login").click()
        time.sleep(1)
        page.get_by_placeholder("Username").click()
        time.sleep(1)
        page.get_by_placeholder("Username").fill(data["name"])
        time.sleep(1)
        page.get_by_placeholder("Username").press("Tab")
        time.sleep(1)
        page.get_by_placeholder("Password").fill(data["password"])
        time.sleep(1)
        page.get_by_role("button", name="LOGIN").click()
        time.sleep(1)
        page.get_by_label("Email").check()
        time.sleep(1)
        page.get_by_role("button", name="CONTINUE").click()
        time.sleep(1)
        page.get_by_placeholder("OTP").click()
        time.sleep(100)

    with open("cookies.json", "w") as f:
        f.write(json.dumps(context.cookies()))
        print("Saved cookies")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    save_cookie(page, context)
    context.close()
    browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    main()


