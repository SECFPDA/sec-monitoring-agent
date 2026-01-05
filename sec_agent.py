#!/usr/bin/env python3
"""
SEC 13F Monitoring Agent - Runs 24/7 for FREE
"""

import requests
import json
import time
from datetime import datetime
import os

class SECMonitoringAgent:
    def __init__(self):
        self.base_url = "https://data.sec.gov/api/xbrl/companyconcept"
        self.user_agent = "YourName your.email@example.com"
        
    def get_latest_filings(self):
        """Get latest 13F filings from SEC"""
        try:
            # Get recent 13F filings (free endpoint)
            headers = {'User-Agent': self.user_agent}
            
            # Example: Get BlackRock filings (CIK: 0001364742)
            cik = "0001364742"  # BlackRock
            url = f"{self.base_url}/CIK{cik}/us-gaap/Assets.json"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract recent filings
                filings = []
                for filing in data.get('units', {}).get('USD', [])[:10]:  # Last 10
                    filings.append({
                        'date': filing.get('end'),
                        'value': filing.get('val'),
                        'form': filing.get('form', '13F-HR')
                    })
                
                return filings
            else:
                return []
                
        except Exception as e:
            print(f"Error getting filings: {e}")
            return []
    
    def analyze_filing(self, filing_data):
        """Simple analysis without OpenAI API (free)"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'filing_date': filing_data.get('date', ''),
            'assets': filing_data.get('value', 0),
            'action': 'HOLD'  # Default
        }
        
        # Simple rule-based analysis (FREE)
        if filing_data.get('value', 0) > 1000000000:  # Over $1B
            analysis['action'] = 'MAJOR_BUY'
        elif filing_data.get('value', 0) > 100000000:  # Over $100M
            analysis['action'] = 'BUY'
        elif filing_data.get('value', 0) < 0:
            analysis['action'] = 'SELL'
            
        return analysis
    
    def save_to_file(self, analysis):
        """Save analysis to file (for GitHub Actions)"""
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"Saved analysis to {filename}")
        return filename

def main():
    print("Starting SEC Monitoring Agent...")
    
    agent = SECMonitoringAgent()
    
    # Get latest filings
    filings = agent.get_latest_filings()
    
    print(f"Found {len(filings)} filings")
    
    # Analyze each filing
    for filing in filings:
        analysis = agent.analyze_filing(filing)
        print(f"Analysis: {analysis}")
        
        # Save to file
        agent.save_to_file(analysis)
    
    print("Agent run complete!")

if __name__ == "__main__":
    main()
