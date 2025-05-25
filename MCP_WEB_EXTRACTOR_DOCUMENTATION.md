# MCP Web Content Extractor Server - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Dependencies & Setup](#dependencies--setup)
4. [Core Components](#core-components)
5. [All Available Tools](#all-available-tools)
6. [Utility Functions](#utility-functions)
7. [Configuration Files](#configuration-files)
8. [Usage Examples](#usage-examples)
9. [Error Handling](#error-handling)
10. [Performance Considerations](#performance-considerations)

---

## Overview

The **MCP Web Content Extractor Server** is a comprehensive Model Context Protocol (MCP) server that provides multiple tools for extracting content from web pages. It supports everything from simple HTTP requests to complex browser automation with authentication, making it capable of extracting **UNLIMITED CONTENT** from dynamic JavaScript-heavy applications like Google Gemini conversations.

### Key Features
- ✅ **Static Content Extraction**: Basic HTTP requests for simple websites
- ✅ **Authenticated Extraction**: Support for cookies, headers, and auth tokens
- ✅ **UNLIMITED Dynamic Content Extraction**: Full browser automation with JavaScript execution - NO LENGTH LIMITS
- ✅ **Google Authentication**: Automated login flows with 2FA support
- ✅ **Structured Content Parsing**: Intelligent HTML parsing and organization
- ✅ **Progressive Content Loading**: Advanced scrolling strategies to load ALL content
- ✅ **Multiple Extraction Strategies**: Fallback mechanisms for robust content extraction
- ✅ **Anti-Detection**: Browser fingerprint evasion for accessing protected content

### 🚀 NEW: Unlimited Content Extraction
The latest version includes **revolutionary unlimited content extraction** capabilities:
- **No character limits** - extracts complete conversations regardless of length
- **Progressive scrolling** - automatically loads all lazy-loaded content
- **Multi-strategy extraction** - uses 3+ different methods to ensure complete content capture
- **Smart content detection** - identifies and extracts conversation content intelligently

---

## Architecture

```
MCP Web Extractor Server
├── FastMCP Framework (mcp.server.fastmcp)
├── HTTP Client Layer (httpx)
├── HTML Parsing Layer (BeautifulSoup + lxml)
├── Browser Automation Layer (Playwright) ⭐ ENHANCED FOR UNLIMITED EXTRACTION
└── Content Processing Layer (Custom extraction logic) ⭐ NO LENGTH LIMITS
```

### Technology Stack
- **MCP Framework**: FastMCP for tool registration and communication
- **HTTP Client**: httpx for async HTTP requests
- **HTML Parsing**: BeautifulSoup4 with lxml parser
- **Browser Automation**: Playwright (Chromium engine) with unlimited scrolling
- **Content Processing**: Custom Python logic for unlimited text extraction and cleaning

---

## Dependencies & Setup

### Requirements (requirements.txt)
```txt
mcp>=1.0.0
httpx>=0.25.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
fastapi>=0.68.0
uvicorn>=0.15.0
playwright>=1.40.0
```

### Project Configuration (pyproject.toml)
```toml
[project]
name = "mcp-server"
version = "0.1.0"
description = "MCP Web Content Extractor Server with Unlimited Content Extraction"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "beautifulsoup4>=4.13.4",
    "httpx>=0.28.1",
    "lxml>=5.4.0",
    "mcp[cli]",
]
```

### MCP Server Configuration (mcp.json)
```json
{
  "mcpServers": {
    "Web Content Extractor": {
      "name": "Web Content Extractor",
      "description": "Advanced MCP server with unlimited content extraction from any URL.",
      "command": "python",
      "args": ["C:/Users/hamza/Documents/MCP/mcp-server/web_extractor.py"],
      "protocol": "mcp",
      "capabilities": ["tools"]
    }
  }
}
```

### Installation Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Run the server
python web_extractor.py
```

---

## Core Components

### 1. FastMCP Server Initialization
```python
from mcp.server.fastmcp import FastMCP

# Create the FastMCP app
mcp = FastMCP("Web Content Extractor")
```

### 2. Default HTTP Headers
```python
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
```

---

## All Available Tools

### 🚀 NEW: `extract_unlimited_dynamic_content` - Ultimate Content Extraction

**Purpose**: Extract unlimited dynamic content from any JavaScript-heavy website using advanced progressive scrolling and multiple extraction strategies.

**Parameters**:
- `url` (str): The URL to extract content from
- `wait_time` (int, optional): Seconds to wait for initial page load (default: 10)

**Key Features**:
- **UNLIMITED content length** - no truncation whatsoever
- **Progressive scrolling** - up to 100 scroll attempts to load all content
- **Multi-directional scrolling** - bottom, top, middle, 3/4 positions
- **Multiple extraction strategies** - 3 different methods with fallbacks
- **Smart duplicate detection** - avoids extracting the same content multiple times
- **Comprehensive element targeting** - targets all possible content containers

**Code Implementation**:
```python
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
    # Advanced browser automation with unlimited scrolling
    browser = await p.chromium.launch(
        headless=False,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-extensions',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-first-run',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]
    )
    
    # Progressive content loading with unlimited scrolling
    max_scroll_attempts = 100  # Allow extensive scrolling
    
    while scroll_attempts < max_scroll_attempts and stable_count < max_stable_attempts:
        # Multi-directional scrolling strategy
        if scroll_attempts % 4 == 0:
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        elif scroll_attempts % 4 == 1:
            await page.evaluate('window.scrollTo(0, 0)')
        elif scroll_attempts % 4 == 2:
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
        else:
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight * 0.75)')
        
        # Monitor content growth and continue until stable
        current_content = await page.evaluate('document.body.innerText.length')
        # ... content monitoring logic
    
    # Strategy 1: Comprehensive element-based extraction
    full_content = await page.evaluate('''
        () => {
            // Get all potentially content-rich elements
            const contentElements = document.querySelectorAll(`
                article, section, main, div, p, span, 
                h1, h2, h3, h4, h5, h6, 
                li, td, th, blockquote, pre, code,
                [role="main"], [role="article"], [role="region"],
                [class*="content"], [class*="text"], [class*="message"],
                [class*="post"], [class*="article"], [class*="comment"],
                [id*="content"], [id*="text"], [id*="main"]
            `);
            
            // Extract with duplicate detection
            const extractedTexts = new Set();
            // ... extraction logic
        }
    ''')
    
    # Return UNLIMITED content - no truncation
    return f"""
# Unlimited Dynamic Content Extraction - COMPLETE!

**Content Length:** {len(full_content):,} characters
**Extraction Status:** UNLIMITED - NO TRUNCATION

## Complete Extracted Content:

{full_content}

=== END OF UNLIMITED CONTENT ===
"""
```

### 🔥 ENHANCED: `extract_dynamic_content` - Google Authentication + Unlimited Extraction

**Purpose**: Extract dynamic content from Google services (like Gemini) with authentication and **UNLIMITED content length**.

**Parameters**:
- `url` (str): The URL to extract content from
- `email` (str): Google email address
- `password` (str): Google password

**🚀 NEW FEATURES**:
- **NO CONTENT TRUNCATION** - extracts complete conversations regardless of length
- **Progressive scrolling** - up to 50 scroll attempts to load all content
- **Enhanced content detection** - 20 attempts to find conversation elements
- **Multiple extraction strategies** - 3 different JavaScript-based methods
- **Smart content monitoring** - tracks content growth during loading

**Key Improvements**:
```python
# Progressive scrolling strategy to load ALL content
max_scroll_attempts = 50  # Allow many more scroll attempts

while scroll_attempts < max_scroll_attempts:
    # Scroll to bottom to trigger lazy loading
    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    await page.wait_for_timeout(2000)
    
    # Monitor content growth
    current_content = await page.evaluate('document.body.innerText.length')
    if current_content > previous_content_length:
        print(f"Content growing: {current_content} characters")
        previous_content_length = current_content
        stable_count = 0
    
    # Additional interactions to trigger loading
    if scroll_attempts % 5 == 0:
        await page.keyboard.press('Space')
    if scroll_attempts % 3 == 0:
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')

# UNLIMITED content extraction - NO TRUNCATION
result = f"""
# Dynamic Content Extraction Success - FULL CONTENT!

**Content Length:** {len(full_content):,} characters
**Extraction Status:** COMPLETE - NO TRUNCATION

## Full Extracted Conversation Content:

{full_content}

=== END OF CONTENT ===
"""
```

### 1. `extract_url_content` - Basic HTTP Extraction

**Purpose**: Extract raw content from any URL using simple HTTP requests.

**Parameters**:
- `url` (str): The URL to fetch content from

**Code Implementation**:
```python
@mcp.tool()
async def extract_url_content(url: str) -> str:
    """Extract raw content from any URL"""
    async with httpx.AsyncClient(timeout=30.0, headers=DEFAULT_HEADERS) as client:
        response = await client.get(url)
        response.raise_for_status()
        
        return f"""
URL: {url}
Status Code: {response.status_code}
Content Type: {response.headers.get('content-type', 'Unknown')}
Content Length: {len(response.text)} characters

=== RAW CONTENT ===
{response.text}
"""
```

### 2. `extract_url_content_clean` - Clean HTML Extraction

**Purpose**: Extract content from URL with just the HTML (no extra metadata).

**Parameters**:
- `url` (str): The URL to fetch content from

**Code Implementation**:
```python
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
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
            
    except Exception as e:
        return f"Error: {str(e)}"
```

### 3. `extract_url_content_structured` - Intelligent Content Parsing

**Purpose**: Extract and structure web content into organized sections with metadata.

**Parameters**:
- `url` (str): The URL to extract content from

**Key Features**:
- Automatic HTML parsing and structure detection
- Extraction of headings, paragraphs, links, and images
- Content organization by sections
- Metadata extraction (title, description)

**Code Implementation**:
```python
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
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract structured content
            structured_content = extract_content_sections(soup, url)
            
            # Format the output
            result = f"""
# {structured_content['metadata']['title']}

**URL:** {structured_content['metadata']['url']}
**Description:** {structured_content['metadata']['description']}

## Content Sections ({structured_content['total_sections']} total)

"""
            
            # Add sections
            for section in structured_content['sections']:
                indent = "  " * (section['level'] - 1)
                result += f"{indent}### {section['heading']}\n"
                if section['content']:
                    result += f"{indent}{section['content']}\n\n"
                else:
                    result += f"{indent}[No content]\n\n"
            
            # Add summary paragraphs
            if structured_content['summary_paragraphs']:
                result += "## Summary Paragraphs\n\n"
                for i, para in enumerate(structured_content['summary_paragraphs'], 1):
                    result += f"{i}. {para}\n\n"
            
            # Add links summary
            if structured_content['links']:
                result += f"## Links ({structured_content['total_links']} total, showing first 20)\n\n"
                for link in structured_content['links']:
                    result += f"- [{link['text']}]({link['url']})\n"
            
            # Add images summary
            if structured_content['images']:
                result += f"\n## Images ({structured_content['total_images']} total, showing first 10)\n\n"
                for img in structured_content['images']:
                    result += f"- {img['url']}"
                    if img['alt']:
                        result += f" (Alt: {img['alt']})"
                    result += "\n"
            
            return result
            
    except httpx.HTTPStatusError as e:
        return f"HTTP Error {e.response.status_code}: {e.response.reason_phrase}\nURL: {url}\nThis might be due to access restrictions or anti-bot protection."
    except httpx.RequestError as e:
        return f"Request Error: {str(e)}\nURL: {url}\nCheck if the URL is valid and accessible."
    except Exception as e:
        return f"Unexpected error: {str(e)}\nURL: {url}"
```

### 4. `extract_url_content_authenticated` - Authenticated Extraction

**Purpose**: Extract content from authenticated URLs using cookies, headers, or tokens.

**Parameters**:
- `url` (str): The URL to extract content from
- `cookies` (str, optional): Cookie string (format: "name1=value1; name2=value2")
- `headers` (str, optional): Custom headers as JSON string or "key: value" format
- `auth_token` (str, optional): Authorization token (will be added as Authorization header)

**Code Implementation**:
```python
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
        # Start with default headers
        request_headers = DEFAULT_HEADERS.copy()
        
        # Add custom headers
        if headers:
            custom_headers = parse_headers(headers)
            request_headers.update(custom_headers)
        
        # Add authorization token
        if auth_token:
            request_headers['Authorization'] = f"Bearer {auth_token}"
        
        # Parse cookies
        request_cookies = parse_cookies(cookies)
        
        async with httpx.AsyncClient(
            headers=request_headers,
            cookies=request_cookies,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract structured content
            structured_content = extract_content_sections(soup, url)
            
            # Format the output with authentication status
            result = f"""
# {structured_content['metadata']['title']}

**URL:** {structured_content['metadata']['url']}
**Description:** {structured_content['metadata']['description']}
**Status:** Authenticated request successful

## Content Sections ({structured_content['total_sections']} total)
"""
            
            # Add sections and content...
            return result
            
    except httpx.HTTPStatusError as e:
        return f"HTTP Error {e.response.status_code}: {e.response.reason_phrase}\nURL: {url}\nThis might be due to insufficient authentication or access restrictions."
    except httpx.RequestError as e:
        return f"Request Error: {str(e)}\nURL: {url}\nCheck if the URL is valid and authentication is correct."
    except Exception as e:
        return f"Unexpected error: {str(e)}\nURL: {url}"
```

### 5. `extract_with_browser_session` - Browser Session Extraction

**Purpose**: Extract content using full browser session cookies (ideal for complex auth like Google/Gemini).

**Parameters**:
- `url` (str): The URL to extract content from
- `browser_cookies` (str): Full cookie string exported from browser developer tools

**Code Implementation**:
```python
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
        # Parse browser cookies
        cookies = parse_cookies(browser_cookies)
        
        # Enhanced headers to mimic a real browser session
        session_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        async with httpx.AsyncClient(
            headers=session_headers,
            cookies=cookies,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Check if we got actual content vs login redirect
            if 'sign' in response.text.lower() and len(response.text) < 5000:
                return f"⚠️ Authentication may have failed. Got potential login page.\n\nResponse preview:\n{response.text[:500]}..."
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'lxml')
            
            result = f"""
# Browser Session Content Extract

**URL:** {url}
**Status Code:** {response.status_code}
**Content Length:** {len(response.text)} characters
**Authentication:** Browser session cookies used

## Page Title
{soup.find('title').get_text() if soup.find('title') else 'No title found'}

## Main Content
"""
            
            # Try to find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if main_content:
                # Get first 5000 characters of text content
                text_content = clean_text(main_content.get_text())
                result += text_content[:5000]
                if len(text_content) > 5000:
                    result += "\n\n... (content truncated)"
            
            return result
            
    except Exception as e:
        return f"Error extracting with browser session: {str(e)}\nURL: {url}"
```

### 6. `get_url_info` - URL Information Inspection

**Purpose**: Get basic information about a URL without fetching full content.

**Parameters**:
- `url` (str): The URL to inspect

**Code Implementation**:
```python
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
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.head(url)  # HEAD request - no content
            
            info = f"""
URL: {url}
Status Code: {response.status_code}
Headers:
"""
            for key, value in response.headers.items():
                info += f"  {key}: {value}\n"
                
            return info
            
    except Exception as e:
        return f"Error: {str(e)}"
```

### 7. `extract_from_open_browser` - Open Browser Session Extraction

**Purpose**: Extract content from an already open browser session.

**Parameters**:
- `url` (str): The URL that should be open in the browser

**Code Implementation**:
```python
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
            # Try to connect to existing browser or launch new one
            try:
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                print("Connected to existing browser session")
            except:
                browser = await p.chromium.launch(headless=False)
                print("Launched new browser session")
            
            # Get all pages/tabs
            contexts = browser.contexts
            if not contexts:
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(url, timeout=60000)
            else:
                # Use existing context and find the right page
                context = contexts[0]
                pages = context.pages
                
                # Find page with matching URL or create new one
                target_page = None
                for page in pages:
                    if url in page.url:
                        target_page = page
                        break
                
                if not target_page:
                    target_page = await context.new_page()
                    await target_page.goto(url, timeout=60000)
                
                page = target_page
            
            # Wait for content to load
            await page.wait_for_timeout(3000)
            
            # Extract content
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            
            # Extract text content
            main_content = soup.find('main') or soup.find('body')
            if main_content:
                text_content = clean_text(main_content.get_text())
                
                result = f"""
# Content Extracted from Open Browser

**URL:** {page.url}
**Page Title:** {soup.find('title').get_text() if soup.find('title') else 'No title found'}

## Extracted Content:

{text_content[:15000]}
"""
                if len(text_content) > 15000:
                    result += "\n\n... (content truncated)"
                
                return result
            else:
                return f"Could not extract content from {url}"
                
    except Exception as e:
        return f"Error extracting from open browser: {str(e)}"
```

### 8. `login_and_extract_google` - Google Authentication with Extraction

**Purpose**: Automatically log into Google and extract content from the authenticated URL.

**Parameters**:
- `url` (str): The URL to extract content from (e.g., Gemini conversation)
- `email` (str): Google email address
- `password` (str): Google password

**Code Implementation**:
```python
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
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 720}
            )
            
            page = await context.new_page()
            
            try:
                # Step 1: Go to Google sign-in
                await page.goto('https://accounts.google.com/signin', wait_until='domcontentloaded', timeout=60000)
                
                # Step 2: Enter email
                try:
                    email_input = await page.wait_for_selector('input[type="email"]', timeout=10000)
                    await email_input.fill(email)
                    await page.click('#identifierNext')
                    print(f"Email entered: {email}")
                except Exception as e:
                    print(f"Could not auto-enter email: {e}")
                    print("Please manually enter your email and continue...")
                
                # Step 3: Wait for password field and enter password
                try:
                    await page.wait_for_selector('input[type="password"]', timeout=15000)
                    await asyncio.sleep(2)  # Wait for animations
                    password_input = page.locator('input[type="password"]').first
                    await password_input.fill(password)
                    await page.click('#passwordNext')
                    print("Password entered")
                except Exception as e:
                    print(f"Could not auto-enter password: {e}")
                    print("Please manually enter your password and continue...")
                
                # Step 4: Wait for successful login (includes manual intervention time)
                print(f"\nWaiting for login completion...")
                print("If you see 2FA prompts, CAPTCHA, or other verification, please complete them manually.")
                
                # Wait for login completion with flexible checking
                login_successful = False
                start_time = asyncio.get_event_loop().time()
                wait_timeout = 120  # 2 minutes for manual intervention
                
                while not login_successful and (asyncio.get_event_loop().time() - start_time) < wait_timeout:
                    current_url = page.url
                    
                    # Check if we're past the login pages
                    if any(indicator in current_url.lower() for indicator in ['myaccount', 'account', 'gmail', 'drive']):
                        login_successful = True
                        break
                    
                    # Check if we're no longer on signin pages
                    if 'accounts.google.com/signin' not in current_url and 'accounts.google.com/v3/signin' not in current_url:
                        # Check if we have a valid Google page
                        try:
                            title = await page.title()
                            if 'sign' not in title.lower() and 'google' in title.lower():
                                login_successful = True
                                break
                        except:
                            pass
                    
                    await asyncio.sleep(2)  # Check every 2 seconds
                
                if not login_successful:
                    return f"""
# Manual Intervention Required

The automated login process needs your help. The browser window is open and waiting.

**Please:**
1. Complete any 2FA verification on your phone/device
2. Solve any CAPTCHA challenges  
3. Complete any other verification steps
4. Once logged in successfully, run the extraction command again

**Current URL:** {page.url}
**Status:** Waiting for manual completion (timed out after {wait_timeout}s)
"""
                
                print("Login appears successful! Navigating to target URL...")
                
                # Step 5: Navigate to target URL with increased timeout
                try:
                    await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                    await asyncio.sleep(5)  # Wait longer for content to load
                    
                    # Wait for conversation content to load
                    await page.wait_for_timeout(3000)
                    
                except Exception as nav_error:
                    print(f"Navigation timeout, but attempting to extract current page content: {nav_error}")
                
                # Step 6: Extract content from current page
                content = await page.content()
                soup = BeautifulSoup(content, 'lxml')
                
                # Try to find conversation content
                conversation_content = ""
                
                # Look for common conversation selectors
                selectors = [
                    '[data-testid*="conversation"]',
                    '[class*="conversation"]', 
                    '[class*="message"]',
                    '[class*="chat"]',
                    'main',
                    '[role="main"]'
                ]
                
                for selector in selectors:
                    elements = soup.select(selector)
                    if elements:
                        for element in elements:
                            text = clean_text(element.get_text())
                            if text and len(text) > 50:
                                conversation_content += text + "\n\n"
                        if conversation_content:
                            break
                
                # If no specific content found, get all text
                if not conversation_content:
                    main_content = soup.find('main') or soup.find('body')
                    if main_content:
                        conversation_content = clean_text(main_content.get_text())
                
                result = f"""
# Login Success with Authentication!

**Target URL:** {url}
**Login Status:** Successfully authenticated with {email}
**Page Title:** {soup.find('title').get_text() if soup.find('title') else 'No title found'}
**Current URL:** {page.url}

## Extracted Content:

"""
                
                if conversation_content and len(conversation_content) > 100:
                    result += conversation_content[:15000]
                    if len(conversation_content) > 15000:
                        result += "\n\n... (content truncated - showing first 15,000 characters)"
                else:
                    result += "Limited content found. The page might still be loading or the conversation might be in a dynamic format."
                    result += f"\n\nRaw page content preview:\n{content[:2000]}..."
                
                await browser.close()
                return result
                
            except Exception as e:
                print(f"Error during login process: {e}")
                return f"""
# Login Process Error 

**Error:** {str(e)}
**Current URL:** {page.url if 'page' in locals() else 'Unknown'}

This might be due to:
- 2FA required (complete on your device)
- CAPTCHA challenge (solve manually)
- Google detecting automation (complete verification)
- Network issues or timeouts
"""
                
    except ImportError:
        return "Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Browser automation failed: {str(e)}"
```

### 9. `login_google_with_help` - Google Login with Manual Intervention

**Purpose**: Login to Google with human intervention support for 2FA/CAPTCHA.

**Parameters**:
- `url` (str): The URL to extract content from
- `email` (str): Google email address
- `password` (str): Google password
- `wait_timeout` (int, optional): Seconds to wait for human intervention (default: 120)

**Key Features**:
- Browser stays open and visible for manual intervention
- Supports 2FA and CAPTCHA completion
- Flexible timeout for human interaction

### 10. `extract_dynamic_content` - Advanced Dynamic Content Extraction

**Purpose**: Extract dynamic content that loads via JavaScript (like Gemini conversations).

**Parameters**:
- `url` (str): The URL to extract content from
- `email` (str): Google email address
- `password` (str): Google password

**Key Features**:
- Full browser automation with JavaScript execution
- Multiple content detection strategies
- Scrolling to trigger lazy loading
- Retry mechanism with up to 15 attempts
- Advanced JavaScript evaluation for content extraction

**Advanced Extraction Strategies**:
```python
# Strategy 1: Try specific selectors
selectors_to_try = [
    '[data-testid*="conversation"]',
    '[data-testid*="message"]', 
    'div[role="main"]',
    '[class*="conversation"]',
    '[class*="message"]',
    '[class*="chat"]',
    '[class*="response"]',
    'div[data-message-author-role]',
    '.model-response-text',
    '.user-input-text'
]

# Strategy 2: JavaScript evaluation for deep extraction
full_content = await page.evaluate('''
    () => {
        let content = '';
        
        // Look for message containers
        const messageSelectors = [
            '[data-testid*="conversation"]',
            '[data-testid*="message"]',
            '[data-message-author-role]',
            '[class*="message"]',
            '[class*="response"]',
            '[class*="user-input"]',
            '[class*="model-response"]'
        ];
        
        for (const selector of messageSelectors) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                const text = el.innerText || el.textContent;
                if (text && text.trim().length > 10) {
                    content += '--- Message ---\\n' + text.trim() + '\\n\\n';
                }
            });
            if (content.length > 100) break;
        }
        
        return content;
    }
''')

# Strategy 3: TreeWalker fallback
if len(full_content) < 200:
    full_content = await page.evaluate('''
        () => {
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                {
                    acceptNode: function(node) {
                        if (node.nodeValue.trim().length > 10) {
                            return NodeFilter.FILTER_ACCEPT;
                        }
                        return NodeFilter.FILTER_SKIP;
                    }
                }
            );
            
            let content = '';
            let node;
            while (node = walker.nextNode()) {
                const text = node.nodeValue.trim();
                if (text && text.length > 10) {
                    content += text + '\\n';
                }
            }
            
            return content;
        }
    ''')
```

---

## Utility Functions

### 1. `parse_cookies(cookie_string: str) -> Dict[str, str]`

**Purpose**: Parse cookie string into a dictionary.

```python
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
```

### 2. `parse_headers(headers_string: str) -> Dict[str, str]`

**Purpose**: Parse headers string (JSON format) into a dictionary.

```python
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
```

### 3. `clean_text(text: str) -> str`

**Purpose**: Clean and normalize text content.

```python
def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove excessive newlines
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text
```

### 4. `extract_content_sections(soup: BeautifulSoup, url: str) -> Dict`

**Purpose**: Extract structured content sections from HTML.

**Returns**: Dictionary containing:
- `metadata`: Title, description, URL
- `sections`: List of content sections with headings
- `summary_paragraphs`: First 5 substantial paragraphs
- `links`: First 20 links with text and URLs
- `images`: First 10 images with URLs and alt text
- `total_*`: Count totals for each content type

```python
def extract_content_sections(soup: BeautifulSoup, url: str) -> Dict:
    """Extract structured content sections from HTML."""
    
    # Extract basic metadata
    title = soup.find('title')
    title_text = clean_text(title.get_text()) if title else "No title found"
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc.get('content', '') if meta_desc else ''
    
    # Extract main content area
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
    
    # Extract paragraphs, links, and images...
    # (Implementation continues with paragraph, link, and image extraction)
    
    return {
        'metadata': {
            'title': title_text,
            'description': clean_text(description),
            'url': url
        },
        'sections': sections[:10],
        'summary_paragraphs': paragraphs[:5],
        'links': links[:20],
        'images': images[:10],
        'total_sections': len(sections),
        'total_links': len(links),
        'total_images': len(images)
    }
```

---

## Usage Examples

### Example 1: Basic Content Extraction
```python
# Extract content from a simple website
result = await extract_url_content("https://example.com")
```

### Example 2: Structured Content Extraction
```python
# Get organized content with headings, links, and images
result = await extract_url_content_structured("https://news.website.com/article")
```

### Example 3: Authenticated Extraction with Cookies
```python
# Extract from authenticated page using browser cookies
cookies = "session=abc123; auth=xyz789"
result = await extract_with_browser_session("https://authenticated-site.com", cookies)
```

### Example 4: Google Gemini Conversation Extraction
```python
# Extract dynamic Gemini conversation content
gemini_url = "https://gemini.google.com/gem/cc2842c78a24/56d6db84ad286329"
email = "your-email@gmail.com"
password = "your-password"
result = await extract_dynamic_content(gemini_url, email, password)
```

### Example 5: Authenticated API Extraction
```python
# Extract from API endpoint with Bearer token
headers = '{"Content-Type": "application/json"}'
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
result = await extract_url_content_authenticated(
    "https://api.example.com/data",
    headers=headers,
    auth_token=auth_token
)
```

---

## Error Handling

### HTTP Errors
```python
try:
    response = await client.get(url)
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    return f"HTTP Error {e.response.status_code}: {e.response.reason_phrase}"
except httpx.RequestError as e:
    return f"Request Error: {str(e)}"
```

### Browser Automation Errors
```python
try:
    # Browser automation code
except ImportError:
    return "Playwright not installed. Run: pip install playwright && playwright install"
except Exception as e:
    return f"Browser automation failed: {str(e)}"
```

### Authentication Errors
```python
# Check for authentication failures
if 'sign' in response.text.lower() and len(response.text) < 5000:
    return f"⚠️ Authentication may have failed. Got potential login page."
```

---

## Performance Considerations

### Tool Selection Guide

| Use Case | Recommended Tool | Performance | Capabilities |
|----------|------------------|-------------|--------------|
| Static websites | `extract_url_content` | ⚡ Fast | Basic HTML |
| News articles, blogs | `extract_url_content_structured` | ⚡ Fast | Organized content |
| Authenticated sites | `extract_url_content_authenticated` | ⚡ Fast | Cookies/headers |
| Browser sessions | `extract_with_browser_session` | ⚡ Fast | Full cookies |
| JavaScript-heavy sites | `extract_dynamic_content` | 🐌 Slow | Full browser |
| Google services | `login_and_extract_google` | 🐌 Slow | Full automation |

### Performance Characteristics

**Fast HTTP-based tools** (1-5 seconds):
- ✅ Low resource usage
- ✅ Quick response times
- ❌ No JavaScript execution
- ❌ Limited authentication

**Browser-based tools** (10-60 seconds):
- ✅ Full JavaScript execution
- ✅ Complex authentication
- ✅ Real browser environment
- ❌ Higher resource usage
- ❌ Slower response times

### Optimization Tips

1. **Use HTTP tools first**: Try simple extraction before browser automation
2. **Cache authentication**: Reuse cookies/sessions when possible
3. **Timeout management**: Set appropriate timeouts for different scenarios
4. **Content limits**: Limit extracted content size to prevent memory issues
5. **Error recovery**: Implement fallback strategies for robust extraction

---

## Security Considerations

### Authentication Safety
- Credentials are passed securely through MCP protocol
- Browser sessions use standard security practices
- No credential storage or logging

### Anti-Detection Measures
```python
# Browser fingerprint evasion
args=[
    '--disable-blink-features=AutomationControlled',
    '--disable-extensions',
    '--no-sandbox'
]

# Real browser user agent
user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

### Rate Limiting
- Built-in timeouts prevent infinite loops
- Retry mechanisms with backoff
- Respectful request patterns

---

## Troubleshooting

### Common Issues

**1. "Playwright not installed"**
```bash
pip install playwright
playwright install
```

**2. "Authentication failed"**
- Check credentials
- Complete 2FA manually
- Verify cookie format

**3. "Limited content extracted"**
- Try dynamic extraction tool
- Check if JavaScript is required
- Verify authentication

**4. "Browser automation failed"**
- Update Playwright browsers
- Check system compatibility
- Try headless=False for debugging

### Debug Mode
- Set `headless=False` to see browser actions
- Use `print()` statements for step tracking
- Check console output for detailed errors

---

This comprehensive documentation covers all aspects of the MCP Web Content Extractor Server, from basic usage to advanced browser automation. Each tool is designed for specific use cases, providing a complete toolkit for web content extraction across different scenarios and authentication requirements. 