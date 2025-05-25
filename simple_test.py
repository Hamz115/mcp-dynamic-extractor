"""
Simple URL Content Extractor Test
=================================

Just paste any URL and see what gets extracted.
No MCP complexity - just direct testing.
"""

import asyncio
import httpx

async def extract_content(url: str):
    """
    Extract content from any URL - exactly what the MCP tool does
    """
    print(f"🌐 Extracting content from: {url}")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        ) as client:
            
            print("📡 Making request...")
            response = await client.get(url)
            response.raise_for_status()
            
            # Show basic info
            print(f"✅ Status Code: {response.status_code}")
            print(f"📄 Content Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"📏 Content Length: {len(response.text):,} characters")
            
            # Show first 1000 characters
            print(f"\n🔍 Content Preview (first 1000 chars):")
            print("-" * 50)
            preview = response.text[:1000]
            if len(response.text) > 1000:
                preview += "\n... [TRUNCATED - full content available]"
            print(preview)
            
            # Ask if user wants to see full content
            print(f"\n💾 Full content is {len(response.text):,} characters long.")
            show_full = input("Show full content? (y/n): ").lower().strip()
            
            if show_full == 'y':
                print(f"\n📄 FULL CONTENT:")
                print("=" * 60)
                print(response.text)
                print("=" * 60)
            
            return response.text
            
    except httpx.RequestError as e:
        print(f"❌ Request failed: {str(e)}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None

async def main():
    print("🚀 Simple URL Content Extractor")
    print("================================")
    print("This shows you exactly what content can be extracted from any website.")
    print()
    
    # Test URLs
    test_urls = [
        "https://espn.com",
        "https://espn.com/nfl", 
        "https://httpbin.org/html",  # Simple test page
    ]
    
    print("🎯 Suggested URLs to test:")
    for i, url in enumerate(test_urls, 1):
        print(f"  {i}. {url}")
    
    print("\n" + "="*50)
    
    while True:
        user_input = input("\nEnter a URL to extract (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
            
        # Add https:// if not present
        if not user_input.startswith(('http://', 'https://')):
            user_input = 'https://' + user_input
        
        print()
        await extract_content(user_input)
        print("\n" + "="*50)

if __name__ == "__main__":
    print("📝 NOTE: This is the same extraction logic that the MCP server uses.")
    print("       But simplified so you can test directly!\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped!") 