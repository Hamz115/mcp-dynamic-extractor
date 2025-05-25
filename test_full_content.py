#!/usr/bin/env python3
"""
Test script to see the FULL structured content extraction.
Shows complete content without truncation.
"""

import asyncio
from web_extractor import extract_url_content_structured

async def test_full_content():
    """Test and display the complete structured content extraction."""
    
    print("🧪 Full Content Extraction Test\n")
    
    # Let's test with just one URL to see everything
    url = input("Enter a URL to extract (or press Enter for Wikipedia Python): ").strip()
    
    if not url:
        url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    print(f"\n📖 Extracting COMPLETE structured content from:")
    print(f"   {url}")
    print("=" * 100)
    
    try:
        # Extract structured content
        result = await extract_url_content_structured(url)
        
        # Show the COMPLETE result
        print(result)
        
        print("\n" + "=" * 100)
        print(f"✅ Complete extraction finished! Total length: {len(result)} characters")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_full_content()) 