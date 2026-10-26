import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp('http://localhost:9222')
            context = browser.contexts[0]
            fb_page = next((p for p in context.pages if 'facebook.com' in p.url), None)
            if not fb_page:
                print("FB_STATUS: NO_FB_TAB")
                return

            print(f"URL: {fb_page.url}")
            print(f"TITLE: {await fb_page.title()}")

            content = await fb_page.content()
            has_login_form = 'name="email"' in content or 'id="email"' in content or 'name="pass"' in content
            has_user_nav = 'aria-label="Your profile"' in content or 'aria-label="Trang cá nhân của bạn"' in content or 'aria-label="Account"' in content or 'aria-label="Tài khoản"' in content

            if has_login_form:
                print("FB_STATUS: REQUIRE_LOGIN")
            elif has_user_nav or 'messages' in content or 'watch' in content:
                print("FB_STATUS: LOGGED_IN")
            else:
                print("FB_STATUS: UNKNOWN")
        except Exception as e:
            print("ERROR:", e)

if __name__ == '__main__':
    asyncio.run(check())
