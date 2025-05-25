"""
Web Content Extractor MCP Server
================================

A comprehensive MCP server that provides unlimited content extraction from web pages, 
including dynamic JavaScript-heavy applications like Google Gemini conversations.
"""

import asyncio
import httpx
from mcp.server.fastmcp import FastMCP
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Optional

# Create the FastMCP app
mcp = FastMCP("Web Content Extractor")

# Default headers to mimic a real browser
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def parse_cookies(cookie_string: str) -> Dict[str, str]:
    """Parse cookie string into a dictionary."""
    if not cookie_string:
        return {}
    
    cookies = {}
    for item in cookie_string.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return cookies

def parse_headers(headers_string: str) -> Dict[str, str]:
    """Parse headers string (JSON format) into a dictionary."""
    if not headers_string:
        return {}
    
    try:
        return json.loads(headers_string)
    except json.JSONDecodeError:
        # Try to parse as simple key:value format
        headers = {}
        for line in headers_string.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove excessive newlines
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text

def extract_content_sections(soup: BeautifulSoup, url: str) -> Dict:
    """Extract structured content sections from HTML."""
    
    # Extract basic metadata
    title = soup.find('title')
    title_text = clean_text(title.get_text()) if title else "No title found"
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc.get('content', '') if meta_desc else ''
    
    # Extract main content area (try common content containers)
    main_content = None
    content_selectors = [
        'main', 'article', '.main-content', '#main-content', 
        '.content', '#content', '.post-content', '.entry-content'
    ]
    
    for selector in content_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break
    
    if not main_content:
        main_content = soup.find('body')
    
    # Extract headings and their content
    sections = []
    if main_content:
        headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for i, heading in enumerate(headings):
            level = int(heading.name[1])
            heading_text = clean_text(heading.get_text())
            
            # Get content until next heading of same or higher level
            content_elements = []
            current = heading.find_next_sibling()
            
            while current:
                if current.name and current.name.startswith('h') and int(current.name[1]) <= level:
                    break
                if current.name in ['p', 'div', 'ul', 'ol', 'blockquote']:
                    text = clean_text(current.get_text())
                    if text:
                        content_elements.append(text)
                current = current.find_next_sibling()
            
            sections.append({
                'level': level,
                'heading': heading_text,
                'content': ' '.join(content_elements)[:1000] + ('...' if len(' '.join(content_elements)) > 1000 else '')
            })
    
    # Extract all paragraphs for summary
    paragraphs = []
    if main_content:
        for p in main_content.find_all('p'):
            text = clean_text(p.get_text())
            if text and len(text) > 50:  # Only substantial paragraphs
                paragraphs.append(text)
    
    # Extract links
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = clean_text(link.get_text())
        if href and text:
            # Convert relative URLs to absolute
            full_url = urljoin(url, href)
            links.append({
                'text': text,
                'url': full_url
            })
    
    # Extract images
    images = []
    for img in soup.find_all('img', src=True):
        src = img.get('src')
        alt = img.get('alt', '')
        if src:
            full_url = urljoin(url, src)
            images.append({
                'url': full_url,
                'alt': clean_text(alt)
            })
    
    return {
        'metadata': {
            'title': title_text,
            'description': clean_text(description),
            'url': url
        },
        'sections': sections[:10],  # Limit to first 10 sections
        'summary_paragraphs': paragraphs[:5],  # First 5 substantial paragraphs
        'links': links[:20],  # First 20 links
        'images': images[:10],  # First 10 images
        'total_sections': len(sections),
        'total_links': len(links),
        'total_images': len(images)
    }

@mcp.tool()
async def login_and_extract_google(url: str, email: str, password: str) -> str:
    """
    Automatically log into Google and extract content from the authenticated URL.
    
    Args:
        url: The URL to extract content from (e.g., Gemini conversation)
        email: Google email address
        password: Google password
    
    Returns:
        Content from the authenticated page
    """
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Launch browser in non-headless mode for better success rate
            browser = await p.chromium.launch(
                headless=False,  # Visible browser to avoid detection
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            try:
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                
                # Navigate to Google login
                await page.goto('https://accounts.google.com/signin')
                await page.wait_for_load_state('networkidle')
                
                # Enter email
                email_input = await page.wait_for_selector('input[type="email"]', timeout=10000)
                await email_input.fill(email)
                await page.click('button:has-text("Next"), #identifierNext')
                
                # Wait for password field
                await page.wait_for_load_state('networkidle')
                password_input = await page.wait_for_selector('input[type="password"]', timeout=10000)
                await password_input.fill(password)
                await page.click('button:has-text("Next"), #passwordNext')
                
                # Wait for login to complete
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(3)
                
                # Navigate to target URL
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(5)  # Wait for dynamic content
                
                # Extract content
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return f"Successfully extracted content from {url}:\n\n{text}"
                
            finally:
                await browser.close()
                
    except ImportError:
        return "Error: Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Error during Google login and extraction: {str(e)}"

@mcp.tool()
async def login_google_with_help(url: str, email: str, password: str, wait_timeout: int = 120) -> str:
    """
    Login to Google with human intervention support for 2FA/CAPTCHA.
    The browser stays open and visible for manual intervention when needed.
    
    Args:
        url: The URL to extract content from (e.g., Gemini conversation)
        email: Google email address
        password: Google password
        wait_timeout: Seconds to wait for human intervention (default: 120)
    
    Returns:
        Content from the authenticated page
    """
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Launch browser in visible mode for human intervention
            browser = await p.chromium.launch(
                headless=False,  # Keep visible for manual intervention
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions'
                ]
            )
            
            try:
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                
                # Navigate to Google login
                await page.goto('https://accounts.google.com/signin')
                await page.wait_for_load_state('networkidle')
                
                try:
                    # Try automated login first
                    email_input = await page.wait_for_selector('input[type="email"]', timeout=5000)
                    await email_input.fill(email)
                    await page.click('button:has-text("Next"), #identifierNext')
                    
                    await page.wait_for_load_state('networkidle')
                    password_input = await page.wait_for_selector('input[type="password"]', timeout=5000)
                    await password_input.fill(password)
                    await page.click('button:has-text("Next"), #passwordNext')
                    
                except Exception:
                    # If automated login fails, let user handle it manually
                    print("Automated login failed. Please complete login manually in the browser window.")
                
                # Wait for user to complete any 2FA/CAPTCHA manually
                print(f"Waiting up to {wait_timeout} seconds for manual intervention...")
                print("Please complete any 2FA, CAPTCHA, or other verification steps in the browser.")
                print("The script will continue automatically once you're logged in.")
                
                # Wait for login completion (check for Google account indicators)
                login_complete = False
                for i in range(wait_timeout):
                    try:
                        # Check if we're logged in by looking for account indicators
                        current_url = page.url
                        if 'accounts.google.com' not in current_url or 'myaccount.google.com' in current_url:
                            login_complete = True
                            break
                        
                        # Also check for common post-login elements
                        account_elements = await page.query_selector_all('[data-email], .gb_A, .gb_B, [aria-label*="Account"]')
                        if account_elements:
                            login_complete = True
                            break
                            
                    except Exception:
                        pass
                    
                    await asyncio.sleep(1)
                
                if not login_complete:
                    return f"Login timeout after {wait_timeout} seconds. Please try again."
                
                print("Login detected! Navigating to target URL...")
                
                # Navigate to target URL
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(5)  # Wait for dynamic content
                
                # Extract content
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return f"Successfully extracted content from {url} after manual login:\n\n{text}"
                
            finally:
                # Keep browser open for a moment to see results
                await asyncio.sleep(2)
                await browser.close()
                
    except ImportError:
        return "Error: Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Error during Google login with help: {str(e)}"

@mcp.tool()
async def extract_url_content_structured(url: str) -> str:
    """
    Extract and structure web content into organized sections.
    Automatically parses HTML and organizes content into:
    - Metadata (title, description)
    - Sections with headings and content
    - Summary paragraphs
    - Links and images
    
    Args:
        url: The URL to extract content from
    
    Returns:
        Structured content organized into sections
    """
    try:
        async with httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract structured content
            structured_content = extract_content_sections(soup, url)
            
            # Format the output
            result = []
            result.append(f"# {structured_content['metadata']['title']}")
            result.append(f"**URL:** {structured_content['metadata']['url']}")
            
            if structured_content['metadata']['description']:
                result.append(f"**Description:** {structured_content['metadata']['description']}")
            
            result.append("")
            
            # Add sections
            if structured_content['sections']:
                result.append("## Content Sections")
                for section in structured_content['sections']:
                    heading_prefix = "#" * (section['level'] + 1)
                    result.append(f"{heading_prefix} {section['heading']}")
                    if section['content']:
                        result.append(section['content'])
                    result.append("")
            
            # Add summary paragraphs
            if structured_content['summary_paragraphs']:
                result.append("## Key Content")
                for i, para in enumerate(structured_content['summary_paragraphs'], 1):
                    result.append(f"{i}. {para}")
                result.append("")
            
            # Add statistics
            result.append("## Content Statistics")
            result.append(f"- Total sections: {structured_content['total_sections']}")
            result.append(f"- Total links: {structured_content['total_links']}")
            result.append(f"- Total images: {structured_content['total_images']}")
            
            return '\n'.join(result)
            
    except Exception as e:
        return f"Error extracting structured content from {url}: {str(e)}"

@mcp.tool()
async def extract_url_content_authenticated(
    url: str, 
    cookies: str = "", 
    headers: str = "", 
    auth_token: str = ""
) -> str:
    """
    Extract content from authenticated URLs using cookies, headers, or tokens.
    
    Args:
        url: The URL to extract content from
        cookies: Cookie string (format: "name1=value1; name2=value2") 
        headers: Custom headers as JSON string or "key: value" format
        auth_token: Authorization token (will be added as Authorization header)
    
    Returns:
        Structured content from the authenticated page
    """
    try:
        # Prepare headers
        request_headers = DEFAULT_HEADERS.copy()
        
        # Add custom headers
        if headers:
            custom_headers = parse_headers(headers)
            request_headers.update(custom_headers)
        
        # Add authorization token
        if auth_token:
            request_headers['Authorization'] = f'Bearer {auth_token}'
        
        # Prepare cookies
        request_cookies = parse_cookies(cookies) if cookies else None
        
        async with httpx.AsyncClient(
            headers=request_headers,
            cookies=request_cookies,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return f"Successfully extracted authenticated content from {url}:\n\n{text}"
            
    except Exception as e:
        return f"Error extracting authenticated content from {url}: {str(e)}"

@mcp.tool()
async def extract_with_browser_session(url: str, browser_cookies: str) -> str:
    """
    Extract content using full browser session cookies (ideal for complex auth like Google/Gemini).
    
    Args:
        url: The URL to extract content from
        browser_cookies: Full cookie string exported from browser developer tools
    
    Returns:
        Content from the authenticated session
    """
    try:
        from playwright.async_api import async_playwright
        
        # Parse cookies from browser export format
        cookies = []
        for cookie_line in browser_cookies.split(';'):
            if '=' in cookie_line:
                name, value = cookie_line.strip().split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': urlparse(url).netloc,
                    'path': '/'
                })
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            # Add cookies to context
            await context.add_cookies(cookies)
            
            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
            # Extract content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            await browser.close()
            
            return f"Successfully extracted content using browser session from {url}:\n\n{text}"
            
    except ImportError:
        return "Error: Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Error extracting content with browser session from {url}: {str(e)}"

@mcp.tool()
async def extract_url_content(url: str) -> str:
    """
    Extract raw content from any URL
    
    Args:
        url: The URL to fetch content from (e.g., https://www.espncricinfo.com/)
    
    Returns:
        The raw HTML/text content from the website
    """
    try:
        async with httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return f"Content from {url}:\n\n{text}"
            
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"

@mcp.tool()
async def extract_url_content_clean(url: str) -> str:
    """
    Extract content from URL with just the HTML (no extra info)
    
    Args:
        url: The URL to fetch content from
    
    Returns:
        Just the raw HTML content
    """
    try:
        async with httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
            
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_url_info(url: str) -> str:
    """
    Get basic information about a URL without fetching full content
    
    Args:
        url: The URL to inspect
    
    Returns:
        Headers and basic response information
    """
    try:
        async with httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.head(url)
            
            info = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'url': str(response.url),
                'content_type': response.headers.get('content-type', 'Unknown')
            }
            
            return f"URL Info for {url}:\n{json.dumps(info, indent=2)}"
            
    except Exception as e:
        return f"Error getting info for {url}: {str(e)}"

@mcp.tool()
async def extract_from_open_browser(url: str) -> str:
    """
    Extract content from an already open browser session.
    Use this when you have a browser window open with the content you want to extract.
    
    Args:
        url: The URL that should be open in the browser
    
    Returns:
        Content extracted from the open browser page
    """
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Connect to existing browser instance
            try:
                # Try to connect to an existing browser
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                contexts = browser.contexts
                
                if not contexts:
                    return "No browser contexts found. Please open a browser window first."
                
                # Use the first available context
                context = contexts[0]
                pages = context.pages
                
                if not pages:
                    return "No pages found in browser context."
                
                # Find page with matching URL or use the first page
                target_page = None
                for page in pages:
                    if url in page.url:
                        target_page = page
                        break
                
                if not target_page:
                    target_page = pages[0]
                    # Navigate to the target URL
                    await target_page.goto(url)
                    await target_page.wait_for_load_state('networkidle')
                
                # Extract content
                content = await target_page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return f"Successfully extracted content from open browser at {url}:\n\n{text}"
                
            except Exception as connect_error:
                # If connection fails, launch a new browser
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # Extract content
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                await browser.close()
                
                return f"Launched new browser and extracted content from {url}:\n\n{text}"
                
    except ImportError:
        return "Error: Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Error extracting from open browser: {str(e)}"

@mcp.tool()
async def extract_dynamic_content(url: str, email: str, password: str) -> str:
    """
    Extract dynamic content that loads via JavaScript (like Gemini conversations).
    Handles login and waits for content to fully load. EXTRACTS UNLIMITED CONTENT LENGTH.
    
    Args:
        url: The URL to extract content from
        email: Google email address  
        password: Google password
    
    Returns:
        Dynamically loaded content from the page - FULL CONTENT, NO TRUNCATION
    """
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Launch browser with anti-detection measures
            browser = await p.chromium.launch(
                headless=False,  # Keep visible for debugging
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            try:
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                
                # Navigate to Google login
                await page.goto('https://accounts.google.com/signin')
                await page.wait_for_load_state('networkidle')
                
                # Enter email
                email_input = await page.wait_for_selector('input[type="email"]', timeout=10000)
                await email_input.fill(email)
                await page.click('button:has-text("Next"), #identifierNext')
                
                # Wait for password field
                await page.wait_for_load_state('networkidle')
                password_input = await page.wait_for_selector('input[type="password"]', timeout=10000)
                await password_input.fill(password)
                await page.click('button:has-text("Next"), #passwordNext')
                
                # Wait for login to complete
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(3)
                
                # Navigate to target URL
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # Progressive scrolling to load all content - UP TO 50 ATTEMPTS
                print("Starting progressive content loading...")
                previous_content_length = 0
                stable_count = 0
                max_scroll_attempts = 50
                
                for scroll_attempt in range(max_scroll_attempts):
                    # Multi-directional scrolling strategy
                    if scroll_attempt % 4 == 0:
                        # Scroll to bottom
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    elif scroll_attempt % 4 == 1:
                        # Scroll to top
                        await page.evaluate("window.scrollTo(0, 0)")
                    elif scroll_attempt % 4 == 2:
                        # Scroll to middle
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    else:
                        # Scroll to 3/4 position
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.75)")
                    
                    await asyncio.sleep(2)  # Wait for content to load
                    
                    # Check content length growth
                    current_content = await page.content()
                    current_length = len(current_content)
                    
                    print(f"Scroll attempt {scroll_attempt + 1}/{max_scroll_attempts}: Content length = {current_length}")
                    
                    if current_length == previous_content_length:
                        stable_count += 1
                        if stable_count >= 3:  # Content stable for 3 attempts
                            print(f"Content stabilized after {scroll_attempt + 1} scroll attempts")
                            break
                    else:
                        stable_count = 0
                        previous_content_length = current_length
                
                # Enhanced content extraction with multiple strategies
                print("Extracting content using multiple strategies...")
                
                # Strategy 1: Look for conversation elements specifically
                conversation_content = ""
                for attempt in range(20):  # Try up to 20 times to find conversation
                    try:
                        # Multiple selectors for different conversation formats
                        conversation_selectors = [
                            '[data-message-author-role]',
                            '.conversation-turn',
                            '.message',
                            '[role="presentation"]',
                            '.model-response',
                            '.user-message',
                            '[data-testid*="conversation"]',
                            '[data-testid*="message"]',
                            '.chat-message',
                            '.response-container'
                        ]
                        
                        for selector in conversation_selectors:
                            elements = await page.query_selector_all(selector)
                            if elements:
                                print(f"Found {len(elements)} conversation elements with selector: {selector}")
                                for element in elements:
                                    text = await element.inner_text()
                                    if text and len(text.strip()) > 10:
                                        conversation_content += text + "\n\n"
                                break
                        
                        if conversation_content:
                            break
                            
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(1)
                
                # Strategy 2: JavaScript-based extraction
                js_extracted_content = ""
                try:
                    js_extraction_scripts = [
                        # Script 1: Comprehensive text extraction
                        """
                        function extractAllText() {
                            const walker = document.createTreeWalker(
                                document.body,
                                NodeFilter.SHOW_TEXT,
                                null,
                                false
                            );
                            let text = '';
                            let node;
                            while (node = walker.nextNode()) {
                                if (node.nodeValue.trim().length > 0) {
                                    text += node.nodeValue.trim() + ' ';
                                }
                            }
                            return text;
                        }
                        extractAllText();
                        """,
                        
                        # Script 2: Element-based extraction
                        """
                        Array.from(document.querySelectorAll('*'))
                            .filter(el => el.children.length === 0 && el.textContent.trim().length > 10)
                            .map(el => el.textContent.trim())
                            .join('\\n\\n');
                        """,
                        
                        # Script 3: Specific content areas
                        """
                        const contentAreas = document.querySelectorAll('main, article, .content, [role="main"], [role="article"]');
                        Array.from(contentAreas).map(area => area.textContent).join('\\n\\n');
                        """
                    ]
                    
                    for i, script in enumerate(js_extraction_scripts):
                        try:
                            result = await page.evaluate(script)
                            if result and len(str(result).strip()) > len(js_extracted_content):
                                js_extracted_content = str(result)
                                print(f"JavaScript extraction strategy {i+1} successful: {len(js_extracted_content)} characters")
                        except Exception as e:
                            print(f"JavaScript extraction strategy {i+1} failed: {e}")
                
                except Exception as e:
                    print(f"JavaScript extraction failed: {e}")
                
                # Strategy 3: Raw HTML parsing fallback
                raw_content = await page.content()
                soup = BeautifulSoup(raw_content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                html_text = soup.get_text()
                lines = (line.strip() for line in html_text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                html_extracted_content = ' '.join(chunk for chunk in chunks if chunk)
                
                # Choose the best extraction result
                final_content = ""
                if conversation_content and len(conversation_content.strip()) > 100:
                    final_content = conversation_content
                    extraction_method = "conversation-specific"
                elif js_extracted_content and len(js_extracted_content.strip()) > 100:
                    final_content = js_extracted_content
                    extraction_method = "javascript-based"
                else:
                    final_content = html_extracted_content
                    extraction_method = "html-parsing"
                
                print(f"Final extraction method: {extraction_method}")
                print(f"Final content length: {len(final_content)} characters")
                
                return f"Successfully extracted UNLIMITED dynamic content from {url} using {extraction_method} method:\n\nContent length: {len(final_content)} characters\n\n{final_content}"
                
            finally:
                await browser.close()
                
    except ImportError:
        return "Error: Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Error during dynamic content extraction: {str(e)}"

@mcp.tool()
async def extract_unlimited_dynamic_content(url: str, wait_time: int = 10) -> str:
    """
    Extract unlimited dynamic content from any JavaScript-heavy website.
    Uses progressive scrolling and multiple extraction strategies to get ALL content.
    
    Args:
        url: The URL to extract content from
        wait_time: Seconds to wait for initial page load (default: 10)
    
    Returns:
        Complete content from the page - NO LENGTH LIMITS
    """
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,  # Keep visible for debugging
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-sandbox'
                ]
            )
            
            try:
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                
                # Navigate to URL
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(wait_time)
                
                # Progressive scrolling to load ALL content - UP TO 100 ATTEMPTS
                print("Starting unlimited progressive content loading...")
                previous_content_length = 0
                stable_count = 0
                max_scroll_attempts = 100
                content_growth_history = []
                
                for scroll_attempt in range(max_scroll_attempts):
                    # Advanced scrolling strategy with multiple interactions
                    scroll_actions = [
                        # Basic scrolling
                        lambda: page.evaluate("window.scrollTo(0, document.body.scrollHeight)"),
                        lambda: page.evaluate("window.scrollTo(0, 0)"),
                        lambda: page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)"),
                        lambda: page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.25)"),
                        lambda: page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.75)"),
                        
                        # Keyboard interactions
                        lambda: page.keyboard.press('Space'),
                        lambda: page.keyboard.press('PageDown'),
                        lambda: page.keyboard.press('End'),
                        lambda: page.keyboard.press('Home'),
                        
                        # Click interactions to trigger lazy loading
                        lambda: page.click('body'),
                    ]
                    
                    # Execute scroll action
                    action = scroll_actions[scroll_attempt % len(scroll_actions)]
                    try:
                        await action()
                    except Exception:
                        pass
                    
                    await asyncio.sleep(2)  # Wait for content to load
                    
                    # Check content length growth
                    current_content = await page.content()
                    current_length = len(current_content)
                    content_growth_history.append(current_length)
                    
                    print(f"Scroll attempt {scroll_attempt + 1}/{max_scroll_attempts}: Content length = {current_length}")
                    
                    # Advanced stability detection
                    if len(content_growth_history) >= 5:
                        recent_growth = content_growth_history[-5:]
                        if all(length == recent_growth[0] for length in recent_growth):
                            print(f"Content stabilized after {scroll_attempt + 1} scroll attempts")
                            break
                    
                    previous_content_length = current_length
                
                # UNLIMITED content extraction with 3 comprehensive strategies
                print("Extracting UNLIMITED content using multiple comprehensive strategies...")
                
                all_extracted_content = set()  # Use set to avoid duplicates
                
                # Strategy 1: Comprehensive element-based extraction
                try:
                    elements = await page.query_selector_all('*')
                    print(f"Found {len(elements)} total elements")
                    
                    for element in elements:
                        try:
                            text = await element.inner_text()
                            if text and len(text.strip()) > 5:  # Only meaningful text
                                all_extracted_content.add(text.strip())
                        except Exception:
                            pass
                    
                    print(f"Strategy 1 (element-based): {len(all_extracted_content)} unique text blocks")
                    
                except Exception as e:
                    print(f"Strategy 1 failed: {e}")
                
                # Strategy 2: TreeWalker for aggressive text extraction
                try:
                    tree_walker_content = await page.evaluate("""
                        function extractAllTextNodes() {
                            const walker = document.createTreeWalker(
                                document.body,
                                NodeFilter.SHOW_TEXT,
                                {
                                    acceptNode: function(node) {
                                        // Accept all text nodes with meaningful content
                                        return node.nodeValue.trim().length > 3 ? 
                                            NodeFilter.FILTER_ACCEPT : 
                                            NodeFilter.FILTER_REJECT;
                                    }
                                },
                                false
                            );
                            
                            const textNodes = [];
                            let node;
                            while (node = walker.nextNode()) {
                                textNodes.push(node.nodeValue.trim());
                            }
                            return textNodes;
                        }
                        extractAllTextNodes();
                    """)
                    
                    if tree_walker_content:
                        for text in tree_walker_content:
                            if text and len(text.strip()) > 5:
                                all_extracted_content.add(text.strip())
                    
                    print(f"Strategy 2 (TreeWalker): {len(all_extracted_content)} unique text blocks")
                    
                except Exception as e:
                    print(f"Strategy 2 failed: {e}")
                
                # Strategy 3: Raw HTML parsing with BeautifulSoup
                try:
                    raw_content = await page.content()
                    soup = BeautifulSoup(raw_content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Extract all text content
                    all_text_elements = soup.find_all(text=True)
                    for text_element in all_text_elements:
                        text = text_element.strip()
                        if text and len(text) > 5:
                            all_extracted_content.add(text)
                    
                    print(f"Strategy 3 (BeautifulSoup): {len(all_extracted_content)} unique text blocks")
                    
                except Exception as e:
                    print(f"Strategy 3 failed: {e}")
                
                # Combine all extracted content
                final_content = '\n\n'.join(sorted(all_extracted_content, key=len, reverse=True))
                
                print(f"UNLIMITED extraction complete!")
                print(f"Total unique text blocks: {len(all_extracted_content)}")
                print(f"Final content length: {len(final_content)} characters")
                
                return f"Successfully extracted UNLIMITED dynamic content from {url}:\n\nTotal text blocks: {len(all_extracted_content)}\nContent length: {len(final_content)} characters\n\n{final_content}"
                
            finally:
                await browser.close()
                
    except ImportError:
        return "Error: Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Error during unlimited dynamic content extraction: {str(e)}"

if __name__ == "__main__":
    mcp.run()
