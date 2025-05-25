# MCP Web Content Extractor Server

A comprehensive Model Context Protocol (MCP) server that provides unlimited content extraction from web pages, including dynamic JavaScript-heavy applications like Google Gemini conversations.

## 🚀 Features

- **Unlimited Content Extraction** - No character limits, extracts complete content
- **Dynamic JavaScript Support** - Full browser automation with Playwright
- **Google Authentication** - Automated login with 2FA support
- **Progressive Content Loading** - Advanced scrolling to load all lazy-loaded content
- **Multiple Extraction Strategies** - Fallback mechanisms for robust extraction
- **Privacy-Focused** - Completely local operation, no cloud dependencies
- **MCP Protocol Compliant** - Works with any MCP-compatible client

## 📋 Available Tools

### 🚀 **ULTIMATE TOOL (Recommended)**
- `extract_dynamic_content` - **THE ULTIMATE EXTRACTION TOOL**: Google authentication + 100 scroll attempts + 4 extraction strategies + unlimited content

### ⚡ Standard Extraction
- `extract_url_content` - Basic HTTP extraction
- `extract_url_content_clean` - Clean HTML only
- `extract_url_content_structured` - Organized content with sections
- `extract_url_content_authenticated` - Cookie/header-based authentication
- `extract_with_browser_session` - Browser session cookies
- `get_url_info` - URL metadata only
- `extract_from_open_browser` - Connect to existing browser sessions

### 🔐 Authentication Tools
- `login_and_extract_google` - Automated Google login + extraction
- `login_google_with_help` - Manual intervention support for 2FA/CAPTCHA

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Windows/macOS/Linux

### Quick Setup

**Tested on Cursor** ✅

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd mcp-server
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**:
```bash
playwright install
```

5. **Run the server**:
```bash
python main.py
```

## 🔧 Configuration

### MCP Client Setup
Add to your MCP client configuration (e.g., `mcp.json`):

**Note**: Copy `mcp.json.example` to `mcp.json` and update the paths for your system.

```json
{
  "mcpServers": {
    "Web Content Extractor": {
      "name": "Web Content Extractor",
      "description": "Advanced MCP server with unlimited content extraction",
      "command": "C:/full/path/to/your/venv/Scripts/python.exe",
      "args": ["C:/full/path/to/main.py"],
      "protocol": "mcp",
      "capabilities": ["tools"]
    }
  }
}
```

**Important Notes:**
- **Use full paths** to both the virtual environment Python and the script
- **Windows**: Use `venv/Scripts/python.exe`
- **macOS/Linux**: Use `venv/bin/python`
- **Replace paths** with your actual installation directories

**Example paths:**
```json
// Windows example:
"command": "C:/Users/YourName/Documents/mcp-server/venv/Scripts/python.exe",
"args": ["C:/Users/YourName/Documents/mcp-server/main.py"]

// macOS/Linux example:
"command": "/Users/YourName/Documents/mcp-server/venv/bin/python",
"args": ["/Users/YourName/Documents/mcp-server/main.py"]
```

## 📖 Usage Examples

### 🤖 AI Assistant Prompts

**For Cursor, Claude, or other AI assistants with MCP support:**

**Google/Gemini conversations (fully supported):**
```
Please extract the complete conversation content from this Gemini chat link, including all messages from the beginning to the most recent:

https://gemini.google.com/app/your-conversation-id-here

Credentials:
Username: your-email@gmail.com
Password: your-password-here

Use extract_dynamic_content for the ultimate extraction experience with unlimited content and Google authentication.
```

**For any public JavaScript-heavy sites (no authentication):**
```
Extract all content from this dynamic website, ensuring complete loading of lazy-loaded elements:

https://complex-website.com/long-article

Use extract_dynamic_content with empty credentials for unlimited extraction of public sites.
Wait time: 15 seconds for initial load, then use progressive scrolling to capture everything.
```

**For ChatGPT conversations:**
```
Note: ChatGPT authentication not yet supported. 
Coming in future updates - will support OpenAI login flow.

For now, use browser session extraction if you're already logged in.
```

### 💡 Quick Tips

**🚀 RECOMMENDED: Use extract_dynamic_content for everything:**
- **THE ULTIMATE TOOL** - Works for both authenticated AND public sites
- **With Google credentials** → Perfect for Google/Gemini with unlimited extraction
- **For public sites** → Just use it without credentials for any JavaScript-heavy site

**Currently supported authentication:**
- ✅ **Google services** (Gemini, Google Docs, etc.) → Use `extract_dynamic_content` with credentials
- ✅ **Public JavaScript sites** → Use `extract_dynamic_content` without credentials  
- ✅ **Static websites** → `extract_url_content` (fastest for simple sites)
- ✅ **Browser sessions** → `extract_with_browser_session` (if you have cookies)

**Coming soon:**
- 🔄 **ChatGPT/OpenAI** authentication
- 🔄 **Twitter/X** authentication  
- 🔄 **LinkedIn** authentication
- 🔄 **Other social platforms**

### 🔧 Direct API Usage

### Extract Unlimited Content from Any Site
```python
# For any JavaScript-heavy website
result = await extract_dynamic_content(
    "https://complex-website.com/long-content",
    wait_time=15
)
```

### Extract Google Gemini Conversations
```python
# Complete Gemini conversation with authentication
result = await extract_dynamic_content(
    "https://gemini.google.com/app/conversation-id",
    "your-email@gmail.com",
    "your-password"
)
```

### Extract with Browser Session
```python
# Using exported browser cookies
result = await extract_with_browser_session(
    "https://authenticated-site.com",
    "session=abc123; auth=xyz789"
)
```

## 🎯 Key Capabilities

### Unlimited Content Extraction
- **No character limits** - extracts complete conversations/articles
- **Progressive scrolling** - up to 100 scroll attempts for complete loading
- **Multi-strategy extraction** - 4 different methods with intelligent fallbacks
- **Smart content detection** - identifies and extracts relevant content

### Authentication Support
- **Google OAuth** - automated login with 2FA support
- **Browser sessions** - use exported cookies from developer tools
- **Custom headers** - API tokens and custom authentication
- **Manual intervention** - browser stays open for CAPTCHA/2FA completion

### Performance Characteristics
| Tool Type | Speed | Content Limits | Use Case |
|-----------|-------|----------------|----------|
| HTTP-based | ⚡ Fast (1-5s) | None | Static sites |
| Browser-based | 🐌 Slow (30-300s) | **NONE** | Dynamic sites |

## 🔍 Troubleshooting

### Common Issues

**"Playwright not installed"**
```bash
pip install playwright
playwright install
```

**"Authentication failed"**
- Check credentials
- Complete 2FA manually in browser
- Verify cookie format

**"Limited content extracted"**
- Try unlimited extraction tools
- Check if authentication is required
- Increase `wait_time` parameter

### Debug Mode
Set `headless=False` in browser tools to see what's happening:
- Browser window will be visible
- You can manually complete 2FA/CAPTCHA
- Watch the extraction process in real-time

## 📊 Performance Examples

**Before vs After Unlimited Extraction:**
- Google Gemini: 20,000 → 58,629+ characters (193% improvement)
- Long articles: 15,000 → 150,000+ characters (900% improvement)
- Social feeds: 5,000 → 75,000+ characters (1400% improvement)

## 🔒 Privacy & Security

- **Completely local** - all processing happens on your machine
- **No telemetry** - no data sent to external services
- **Credential safety** - credentials only used for direct authentication
- **No storage** - extracted content returned directly, not stored

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk)
- Browser automation powered by [Playwright](https://playwright.dev/)
- HTML parsing with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

**Note**: This tool is designed for legitimate content extraction and research purposes. Always respect website terms of service and robots.txt files. 