#!/usr/bin/env python3
"""
Test script for the enhanced web content extractor with intelligent parsing.
This demonstrates the automatic sectioning and content organization.
"""

import asyncio
from web_extractor import extract_url_content_structured

async def test_structured_extraction():
    """Test the structured content extraction."""
    
    print("🧪 Testing Intelligent Web Content Extraction\n")
    
    # Test URLs that should work well with structured parsing
    test_urls = [
        "https://en.wikipedia.org/wiki/The_Stormlight_Archive",
        
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"📖 Test {i}: Extracting structured content from:")
        print(f"   {url}")
        print("-" * 80)
        
        try:
            # Extract structured content
            result = await extract_url_content_structured(url)
            
            # Show first 2000 characters to see the structure
            if len(result) > 2000:
                print(result[:2000])
                print(f"\n... [Content truncated - showing first 2000 of {len(result)} characters]")
            else:
                print(result)
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_structured_extraction()) 