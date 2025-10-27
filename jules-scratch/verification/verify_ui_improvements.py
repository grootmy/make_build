from playwright.sync_api import sync_playwright, expect
import random
import string

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Generate a unique username for this test run
    username = f"testuser_{random_string()}"
    password = "password123"

    # 1. Sign Up
    # Use 'domcontentloaded' to avoid 'networkidle' issues with the dev server.
    page.goto("http://localhost:8000/signup/", wait_until="domcontentloaded")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.fill('input[name="password2"]', password)
    page.click('button[type="submit"]')
    expect(page.locator("h1:has-text('My Projects')")).to_be_visible()

    # 2. Project List Page (after signup)
    page.screenshot(path="jules-scratch/verification/01_project_list_bootstrap.png")

    # 3. Create and go to Design Page
    page.fill('input[name="name"]', 'My New Design')
    page.click('button:has-text("Create")')
    expect(page.locator('a:has-text("My New Design")')).to_be_visible()
    page.click('a:has-text("My New Design")')
    expect(page.locator("h1:has-text('Design for My New Design')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/02_design_page_bootstrap.png")

    # 4. Profile Page
    page.goto("http://localhost:8000/profile/", wait_until="domcontentloaded")
    expect(page.locator(f"text={username}")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/03_profile_page_bootstrap.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
