"""
Test script for the Web Extractor MCP Server
============================================

This script shows you how to test the web extractor tools.
"""

import asyncio
import httpx

async def test_direct():
    """
    Test the extraction directly (simulating what MCP does)
    """
    print("🧪 Testing Direct Web Extraction")
    print("=================================")
    
    # Test URLs
    test_urls = [
        "https://httpbin.org/html",  # Simple test page
        "https://espn.com",          # ESPN homepage
        "https://httpbin.org/json",  # JSON response
    ]
    
    for url in test_urls:
        print(f"\n📡 Testing: {url}")
        print("-" * 50)
        
        try:
            async with httpx.AsyncClient(
                timeout=10.0,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            ) as client:
                response = await client.get(url)
                
                print(f"✅ Status: {response.status_code}")
                print(f"📄 Content-Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"📏 Content Length: {len(response.text)} characters")
                
                # Show first 500 characters of content
                content_preview = response.text[:500]
                if len(response.text) > 500:
                    content_preview += "... [truncated]"
                
                print(f"\n🔍 Content Preview:")
                print(content_preview)
                
        except Exception as e:
            print(f"❌ Error: {e}")

def show_mcp_usage():
    """
    Show how to use the MCP server
    """
    print("\n" + "="*60)
    print("🚀 How to Use the MCP Web Extractor")
    print("="*60)
    
    print("""
1. The MCP server is running in development mode
2. You can interact with it using MCP-compatible tools
3. Available tools:

   📥 extract_url_content(url)
   - Gets full content with metadata
   - Perfect for seeing exactly what gets extracted
   
   🧹 extract_url_content_clean(url) 
   - Gets just the raw HTML
   - No extra formatting
   
   ℹ️  get_url_info(url)
   - Gets just headers and basic info
   - No content download

4. Example ESPN URLs to test:
   • https://espn.com
   • https://espn.com/nfl
   • https://espn.com/nba/scoreboard

5. The server will show you EXACTLY what content it can extract
   from any website you give it.
""")

if __name__ == "__main__":
    print("🌐 Web Extractor Test Suite")
    print("============================")
    
    # Show usage instructions
    show_mcp_usage()
    
    # Ask user if they want to run direct tests
    print("\n" + "="*60)
    user_input = input("Want to run direct extraction tests? (y/n): ").lower().strip()
    
    if user_input == 'y':
        # Run direct tests
        asyncio.run(test_direct())
    
    print("\n✨ Ready to test with your ESPN URLs!")
    print("The MCP server is running and waiting for requests.") 