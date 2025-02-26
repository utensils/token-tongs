#!/usr/bin/env python3
import rumps
import requests
import os
from datetime import datetime

class TokenTongs(rumps.App):
    def __init__(self):
        # Initialize menu items first
        self._credits_item = rumps.MenuItem("Credits: $0.00")
        self._usage_item = rumps.MenuItem("Usage: $0.00")
        self._last_updated_item = rumps.MenuItem("Last Updated: Never")
        self._provider_item = rumps.MenuItem("Provider: OpenRouter")
        
        # Initialize the app with menu structure
        menu = [
            self._provider_item,
            self._credits_item,
            self._usage_item,
            None,  # Separator
            self._last_updated_item
        ]
        super(TokenTongs, self).__init__("Loading...", menu=menu)
        
        # Set default provider
        self.provider = "OpenRouter"
        
        # Get API key from environment variable
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        print(f"Environment variables: {[k for k in os.environ.keys() if 'API' in k]}")
        if not self.api_key:
            self.title = "No API Key"
            print("No API key found. Please set the OPENROUTER_API_KEY environment variable.")
            return
            
        self.endpoint = "https://openrouter.ai/api/v1/credits"
        
        self.update_timer = rumps.Timer(self.update_balance, 1800)  # 30 minutes
        self.update_timer.start()
        self.update_balance()

    def get_balance(self):
        """Fetch the current balance from OpenRouter API"""
        if not self.api_key:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(
                self.endpoint,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json().get('data', {})
            return {
                'total_credits': data.get('total_credits', 0.0),
                'total_usage': data.get('total_usage', 0.0)
            }
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

    @rumps.timer(1800)  # 30 minutes
    def update_balance(self, _=None):
        """Update the displayed balance"""
        balance_data = self.get_balance()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if balance_data is not None:
            credits = balance_data['total_credits']
            usage = balance_data['total_usage']
            remaining = credits - usage
            
            self.title = f"${remaining:.2f}"
            self._credits_item.title = f"Credits: ${credits:.2f}"
            self._usage_item.title = f"Usage: ${usage:.2f}"
            self._last_updated_item.title = f"Last Updated: {now}"
            self._provider_item.title = f"Provider: {self.provider}"
        else:
            self.title = "API Error"
            self._credits_item.title = "Credits: Error"
            self._usage_item.title = "Usage: Error"
            self._last_updated_item.title = f"Error at: {now}"
            self._provider_item.title = f"Provider: {self.provider}"

def main():
    TokenTongs().run()

if __name__ == "__main__":
    main()