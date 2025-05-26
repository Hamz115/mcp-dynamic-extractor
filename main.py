"""
Web Content Extractor MCP Server
================================

A simple MCP server that extracts raw content from any URL.
Perfect for testing what content can be retrieved from websites like ESPN.
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
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Return basic info + content
            result = f"""
URL: {url}
Status Code: {response.status_code}
Content Type: {response.headers.get('content-type', 'Unknown')}
Content Length: {len(response.text)} characters

=== RAW CONTENT ===
{response.text}
"""
            return result
            
    except httpx.RequestError as e:
        return f"Request failed: {str(e)}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

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
            
            # Format the output
            result = f"""
# {structured_content['metadata']['title']}

**URL:** {structured_content['metadata']['url']}
**Description:** {structured_content['metadata']['description']}
**Status:** Authenticated request successful

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
            
            return result
            
    except httpx.HTTPStatusError as e:
        return f"HTTP Error {e.response.status_code}: {e.response.reason_phrase}\nURL: {url}\nThis might be due to insufficient authentication or access restrictions."
    except httpx.RequestError as e:
        return f"Request Error: {str(e)}\nURL: {url}\nCheck if the URL is valid and authentication is correct."
    except Exception as e:
        return f"Unexpected error: {str(e)}\nURL: {url}"

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
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--no-first-run'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                # Step 1: Login process with extended timeouts
                await page.goto('https://accounts.google.com/signin', wait_until='domcontentloaded', timeout=120000)  # Increased to 2 minutes
                
                # Enter email with longer timeout
                email_input = await page.wait_for_selector('input[type="email"]', timeout=30000)  # Increased timeout
                await email_input.fill(email)
                await page.click('#identifierNext')
                
                # Enter password with longer timeout
                await page.wait_for_selector('input[type="password"]', timeout=30000)  # Increased timeout
                await asyncio.sleep(3)  # Longer wait for animations
                password_input = page.locator('input[type="password"]').first
                await password_input.fill(password)
                await page.click('#passwordNext')
                
                # Wait for login to complete with much longer timeout
                await page.wait_for_timeout(10000)  # Increased wait time
                
                # Step 2: Navigate to target URL
                await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                # Step 2.5: Wait for the page to fully load and show chat content
                # Wait for common Gemini chat elements to appear
                chat_loaded = False
                load_attempts = 0
                max_load_attempts = 30  # 30 attempts = up to 60 seconds
                
                while not chat_loaded and load_attempts < max_load_attempts:
                    try:
                        # Check for various Gemini chat indicators
                        chat_indicators = [
                            '[data-testid*="conversation"]',
                            '[class*="conversation"]', 
                            '[class*="message"]',
                            'main[role="main"]',
                            '[role="main"]'
                        ]
                        
                        for indicator in chat_indicators:
                            elements = await page.query_selector_all(indicator)
                            if elements and len(elements) > 0:
                                # Check if any element has substantial text content
                                for element in elements:
                                    text_content = await element.inner_text()
                                    if text_content and len(text_content.strip()) > 50:
                                        chat_loaded = True
                                        break
                                if chat_loaded:
                                    break
                        
                        if not chat_loaded:
                            load_attempts += 1
                            await page.wait_for_timeout(2000)  # Wait 2 seconds between checks
                            
                    except Exception as e:
                        load_attempts += 1
                        await page.wait_for_timeout(2000)
                
                # Additional wait to ensure everything is rendered
                await page.wait_for_timeout(5000)  # Extra 5 seconds for full rendering
                
                # Step 6: MANUAL SCROLL WAIT - Give user time to scroll to the top
                # Wait exactly 90 seconds for manual scrolling
                for countdown in range(90, 0, -1):
                    await page.wait_for_timeout(1000)  # Wait 1 second
                
                # Step 7: Extract content from current page
                content = await page.content()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'lxml')
                
                # Try to find Gemini-specific content areas
                conversation_content = ""
                
                # Look for common Gemini conversation selectors
                gemini_selectors = [
                    '[data-testid*="conversation"]',
                    '[class*="conversation"]', 
                    '[class*="message"]',
                    '[class*="chat"]',
                    'main',
                    '[role="main"]'
                ]
                
                for selector in gemini_selectors:
                    elements = soup.select(selector)
                    if elements:
                        for element in elements:
                            text = clean_text(element.get_text())
                            if text and len(text) > 50:  # Only substantial content
                                conversation_content += text + "\n\n"
                        if conversation_content:
                            break
                
                # If no specific content found, get all text
                if not conversation_content:
                    main_content = soup.find('main') or soup.find('body')
                    if main_content:
                        conversation_content = clean_text(main_content.get_text())
                
                result = f"""
# Dynamic Content Extraction Success - FULL CONTENT!

**Target URL:** {url}
**Current URL:** {page.url}
**Page Title:** {page.title}
**Content Length:** {len(conversation_content):,} characters
**Extraction Status:** COMPLETE - NO TRUNCATION

## Full Extracted Conversation Content:

{conversation_content}

=== END OF CONTENT ===
"""
                
                # Add extraction statistics
                result += f"""

## Extraction Statistics:
- **Total Characters:** {len(conversation_content):,}
- **Total Words:** {len(conversation_content.split()):,}
- **Total Lines:** {len(conversation_content.splitlines()):,}
- **Content Status:** FULLY EXTRACTED (no limits applied)
"""
                
                if len(conversation_content) < 500:
                    result += f"\n\n**Note:** Limited content extracted ({len(conversation_content)} chars). Page might still be loading or require additional authentication.\n\nRaw page text preview:\n{conversation_content}"
                
                await browser.close()
                return result
                
            except Exception as e:
                await browser.close()
                return f"Error during dynamic extraction: {str(e)}\n\nCurrent URL: {page.url if 'page' in locals() else 'Unknown'}"
                
    except ImportError:
        return "Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Dynamic extraction failed: {str(e)}"

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
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                # Initial wait for page to load
                await page.wait_for_timeout(wait_time * 1000)
                
                # Progressive content loading with unlimited scrolling
                previous_content_length = 0
                stable_count = 0
                max_stable_attempts = 8  # More attempts for complex sites
                scroll_attempts = 0
                max_scroll_attempts = 100  # Allow extensive scrolling
                
                while scroll_attempts < max_scroll_attempts and stable_count < max_stable_attempts:
                    # Multi-directional scrolling strategy
                    if scroll_attempts % 4 == 0:
                        # Scroll to bottom
                        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    elif scroll_attempts % 4 == 1:
                        # Scroll to top
                        await page.evaluate('window.scrollTo(0, 0)')
                    elif scroll_attempts % 4 == 2:
                        # Scroll to middle
                        await page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
                    else:
                        # Scroll to 3/4 position
                        await page.evaluate('window.scrollTo(0, document.body.scrollHeight * 0.75)')
                    
                    await page.wait_for_timeout(1500)  # Wait for content to load
                    
                    # Check current content length
                    current_content = await page.evaluate('document.body.innerText.length')
                    
                    if current_content > previous_content_length:
                        previous_content_length = current_content
                        stable_count = 0  # Reset stable count
                    else:
                        stable_count += 1
                    
                    scroll_attempts += 1
                    
                    # Try various interactions to trigger content loading
                    if scroll_attempts % 5 == 0:
                        await page.keyboard.press('Space')
                        await page.wait_for_timeout(500)
                    
                    if scroll_attempts % 7 == 0:
                        await page.keyboard.press('PageDown')
                        await page.wait_for_timeout(500)
                    
                    if scroll_attempts % 10 == 0:
                        # Try clicking on the page to trigger any click-based loading
                        try:
                            await page.click('body')
                            await page.wait_for_timeout(500)
                        except:
                            pass
                
                # UNLIMITED content extraction using multiple comprehensive strategies
                # Strategy 1: Comprehensive element-based extraction
                full_content = await page.evaluate('''
                    () => {
                        let content = '';
                        let extractedSections = 0;
                        
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
                        
                        // Extract text from each element, avoiding duplicates
                        const extractedTexts = new Set();
                        
                        contentElements.forEach((element, index) => {
                            const text = element.innerText || element.textContent;
                            if (text && text.trim().length > 20) {
                                const trimmedText = text.trim();
                                
                                // Skip if we've already extracted this text
                                if (!extractedTexts.has(trimmedText)) {
                                    // Check if this is not a child of already extracted content
                                    let isChildContent = false;
                                    for (const existingText of extractedTexts) {
                                        if (existingText.includes(trimmedText) || trimmedText.includes(existingText)) {
                                            isChildContent = true;
                                            break;
                                        }
                                    }
                                    
                                    if (!isChildContent) {
                                        extractedTexts.add(trimmedText);
                                        extractedSections++;
                                        content += `\\n=== Section ${extractedSections} ===\\n`;
                                        content += trimmedText + '\\n\\n';
                                    }
                                }
                            }
                        });
                        
                        return content;
                    }
                ''')
                
                # Strategy 2: If content is still limited, use TreeWalker for deep extraction
                if len(full_content) < 2000:
                    additional_content = await page.evaluate('''
                        () => {
                            const walker = document.createTreeWalker(
                                document.body,
                                NodeFilter.SHOW_TEXT,
                                {
                                    acceptNode: function(node) {
                                        const text = node.nodeValue.trim();
                                        if (text.length > 3 && 
                                            !text.match(/^[\\s\\n\\r]*$/) &&
                                            !text.includes('©') && 
                                            !text.includes('cookie') &&
                                            !text.includes('privacy policy')) {
                                            return NodeFilter.FILTER_ACCEPT;
                                        }
                                        return NodeFilter.FILTER_SKIP;
                                    }
                                }
                            );
                            
                            let content = '';
                            let node;
                            let nodeCount = 0;
                            const processedTexts = new Set();
                            
                            while (node = walker.nextNode()) {
                                const text = node.nodeValue.trim();
                                if (text && text.length > 3 && !processedTexts.has(text)) {
                                    processedTexts.add(text);
                                    content += text + ' ';
                                    nodeCount++;
                                }
                            }
                            
                            return content;
                        }
                    ''')
                    
                    if len(additional_content) > len(full_content):
                        full_content = additional_content
                
                # Strategy 3: Raw HTML parsing as final fallback
                if len(full_content) < 1000:
                    html_content = await page.content()
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html_content, 'lxml')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style", "nav", "header", "footer"]):
                        script.decompose()
                    
                    # Get all text
                    full_content = soup.get_text()
                    # Clean up whitespace
                    import re
                    full_content = re.sub(r'\s+', ' ', full_content).strip()
                
                # Get page metadata
                title = await page.title()
                current_url = page.url
                
                # Return UNLIMITED content
                result = f"""
# Unlimited Dynamic Content Extraction - COMPLETE!

**Target URL:** {url}
**Current URL:** {current_url}
**Page Title:** {title}
**Content Length:** {len(full_content):,} characters
**Scroll Attempts:** {scroll_attempts}
**Extraction Status:** UNLIMITED - NO TRUNCATION

## Complete Extracted Content:

{full_content}

=== END OF UNLIMITED CONTENT ===
"""
                
                # Add detailed extraction statistics
                result += f"""

## Detailed Extraction Statistics:
- **Total Characters:** {len(full_content):,}
- **Total Words:** {len(full_content.split()):,}
- **Total Lines:** {len(full_content.splitlines()):,}
- **Scroll Attempts:** {scroll_attempts}
- **Final Content Length:** {previous_content_length:,} characters
- **Content Status:** FULLY EXTRACTED (unlimited)
- **Extraction Method:** Progressive scrolling + Multi-strategy extraction
"""
                
                if len(full_content) < 500:
                    result += f"\n\n**Note:** Limited content extracted ({len(full_content)} chars). This might be a simple page or content might be behind authentication."
                
                await browser.close()
                return result
                
            except Exception as e:
                await browser.close()
                return f"Error during unlimited extraction: {str(e)}\n\nCurrent URL: {page.url if 'page' in locals() else 'Unknown'}"
                
    except ImportError:
        return "Playwright not installed. Run: pip install playwright && playwright install"
    except Exception as e:
        return f"Unlimited extraction failed: {str(e)}"

if __name__ == "__main__":
    mcp.run() 