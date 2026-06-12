#!/usr/bin/env python3
"""Test script: scrape Sina article directly"""
import requests, json, re
from bs4 import BeautifulSoup

url = "https://finance.sina.com.cn/wm/2026-05-16/doc-inhyahas2588021.shtml"
print("Testing:", url)

# Try multiple UAs
for ua in [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": ua})
        print(f"UA: {ua[:50]}... -> Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 5000:
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            
            # Title
            title_tag = soup.find("title")
            if title_tag:
                t = title_tag.get_text().strip()
                print(f"Title: {t[:100]}")
            
            # Content
            for sel in [".article-content", "#artibody", ".article-body", ".article", "[class*='article']", "body"]:
                div = soup.select_one(sel)
                if div:
                    text = div.get_text().strip()
                    if len(text) > 200:
                        print(f"Found content in '{sel}': {len(text)} chars")
                        print(text[:500])
                        break
            else:
                print("No content found!")
            break
    except Exception as e:
        print(f"Error: {e}")

# Try Playwright
try:
    from playwright.sync_api import sync_playwright
    print("\nTrying Playwright...")
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page()
        page.goto(url, timeout=20000, wait_until="load")
        page.wait_for_timeout(3000)
        html = page.content()
        print(f"Playwright HTML: {len(html)} chars")
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        if title_tag: print(f"Title: {title_tag.get_text().strip()[:100]}")
        body = soup.find("body")
        if body:
            for t in body.find_all(['script','style','nav','header','footer']): t.decompose()
            text = ' '.join(body.get_text().split()[:200])
            print(f"Body text: {len(text)} chars")
            print(text[:500])
        b.close()
except Exception as e:
    print(f"Playwright error: {e}")
