import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from .models import AITool

logger = logging.getLogger(__name__)


class ToolUpdater:
    def update_all_tools(self):
        """Update all tools with auto-update enabled"""
        tools = AITool.objects.filter(has_auto_update=True)
        success_count = 0
        for tool in tools:
            if self.update_tool_details(tool):
                success_count += 1
        return success_count, len(tools)
    
    def update_tool_details(self, tool):
        """Update details for a single tool"""
        try:
            # Fetch tool website
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; TechyViaBot/1.0; +https://techyvia.com/bot)'
            }
            response = requests.get(tool.website, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract pricing information
            pricing_info = self.extract_pricing(soup)
            if pricing_info:
                tool.pricing_type = pricing_info['type']
                tool.price_range = pricing_info['range']
            
            # Extract description
            description = self.extract_description(soup)
            if description and len(description) > 50:
                tool.description = description
            
            # Mark as verified
            tool.verification_status = 'VER'
            tool.last_verified = datetime.now()
            tool.save()
            return True
        except Exception as e:
            logger.error(f"Update failed for {tool.name}: {str(e)}")
            return False
    
    def extract_pricing(self, soup):
        """Extract pricing information from page"""
        # Strategy 1: Look for pricing in meta tags
        meta_pricing = soup.find('meta', attrs={'name': 'pricing'})
        if meta_pricing and meta_pricing.get('content'):
            return self.parse_pricing(meta_pricing['content'])
        
        # Strategy 2: Look for common pricing class names
        pricing_elements = soup.find_all(class_=lambda c: c and 'pric' in c.lower())
        for element in pricing_elements:
            text = element.get_text().strip()
            parsed = self.parse_pricing(text)
            if parsed:
                return parsed
        
        # Strategy 3: Look for pricing tables
        pricing_table = soup.find('table', class_=lambda c: c and 'pric' in c.lower())
        if pricing_table:
            # Extract text from first row
            first_row = pricing_table.find('tr')
            if first_row:
                text = first_row.get_text().strip()
                parsed = self.parse_pricing(text)
                if parsed:
                    return parsed
        
        return None
    
    def parse_pricing(self, text):
        """Parse pricing text into structured data"""
        text = text.lower()
        
        # Check for free
        if 'free' in text:
            return {'type': 'FRE', 'range': 'Free'}
        
        # Check for freemium
        if 'freemium' in text:
            return {'type': 'FRP', 'range': 'Freemium'}
        
        # Check for subscription
        if 'subscription' in text or '/mo' in text or 'monthly' in text:
            # Try to extract price
            import re
            match = re.search(r'\$(\d+(\.\d+)?', text)
            if match:
                price = match.group(0)
                return {'type': 'SUB', 'range': f"{price}/mo"}
            return {'type': 'SUB', 'range': 'Subscription'}
        
        # Check for one-time purchase
        if 'one-time' in text or 'purchase' in text:
            match = re.search(r'\$(\d+(\.\d+)?', text)
            if match:
                price = match.group(0)
                return {'type': 'PAY', 'range': f"{price} one-time"}
        
        return None
    
    def extract_description(self, soup):
        """Extract description from page"""
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']
        
        # Try OpenGraph description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content']
        
        # Try first paragraph
        first_p = soup.find('p')
        if first_p and first_p.get_text().strip():
            return first_p.get_text().strip()
        
        return None