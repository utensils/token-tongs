import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import rumps
import requests
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from token_tongs import TokenTongs, main

class TestTokenTongs(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        os.environ['OPENROUTER_API_KEY'] = 'test_key'
        # Mock rumps.App and prevent initial update_balance call
        with patch('rumps.App'), patch('token_tongs.TokenTongs.update_balance'):
            self.app = TokenTongs()

    def tearDown(self):
        """Clean up after each test method."""
        if 'OPENROUTER_API_KEY' in os.environ:
            del os.environ['OPENROUTER_API_KEY']

    @patch('requests.get')
    def test_successful_balance_fetch(self, mock_get):
        """Test successful balance fetch from API"""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'total_credits': 100.50,
                'total_usage': 25.25
            }
        }
        mock_get.return_value = mock_response

        balance = self.app.get_balance()
        self.assertEqual(balance['total_credits'], 100.50)
        self.assertEqual(balance['total_usage'], 25.25)

        # Verify GET was called with correct headers
        mock_get.assert_called_once_with(
            "https://openrouter.ai/api/v1/credits",
            headers={
                "Authorization": "Bearer test_key"
            },
            timeout=10
        )

    @patch('requests.get')
    def test_failed_balance_fetch(self, mock_get):
        """Test failed balance fetch from API"""
        mock_get.side_effect = requests.exceptions.RequestException()
        
        balance = self.app.get_balance()
        self.assertIsNone(balance)

    def test_balance_display(self):
        """Test balance update in the menu"""
        with patch('token_tongs.TokenTongs.get_balance') as mock_get_balance:
            mock_get_balance.return_value = {
                'total_credits': 100.00,
                'total_usage': 25.50
            }
            
            self.app.update_balance()
            self.assertEqual(self.app.title, "$74.50")  # Remaining balance
            self.assertEqual(self.app._credits_item.title, "Credits: $100.00")
            self.assertEqual(self.app._usage_item.title, "Usage: $25.50")
            self.assertEqual(self.app._provider_item.title, "Provider: OpenRouter")
            self.assertEqual(self.app._last_updated_item.title.startswith("Last Updated:"), True)

    def test_error_display(self):
        """Test error display in the menu"""
        with patch('token_tongs.TokenTongs.get_balance') as mock_get_balance:
            mock_get_balance.return_value = None
            
            self.app.update_balance()
            self.assertEqual(self.app.title, "API Error")
            self.assertEqual(self.app._credits_item.title, "Credits: Error")
            self.assertEqual(self.app._usage_item.title, "Usage: Error")
            self.assertEqual(self.app._provider_item.title, "Provider: OpenRouter")
            self.assertTrue(self.app._last_updated_item.title.startswith("Error at:"))

    def test_menu_structure(self):
        """Test the menu structure and ensure menu items are properly initialized"""
        # Test menu item instances
        self.assertTrue(isinstance(self.app._credits_item, rumps.MenuItem))
        self.assertTrue(isinstance(self.app._usage_item, rumps.MenuItem))
        self.assertTrue(isinstance(self.app._provider_item, rumps.MenuItem))
        self.assertTrue(isinstance(self.app._last_updated_item, rumps.MenuItem))
        
        # Test initial menu item titles
        self.assertEqual(self.app._credits_item.title, "Credits: $0.00")
        self.assertEqual(self.app._usage_item.title, "Usage: $0.00")
        self.assertEqual(self.app._provider_item.title, "Provider: OpenRouter")
        self.assertEqual(self.app._last_updated_item.title, "Last Updated: Never")

    def test_no_api_key(self):
        """Test behavior when no API key is provided"""
        # Remove API key from environment
        if 'OPENROUTER_API_KEY' in os.environ:
            del os.environ['OPENROUTER_API_KEY']
            
        # Create a new instance without an API key
        with patch('rumps.App'):
            app = TokenTongs()
            self.assertEqual(app.title, "No API Key")
            self.assertIsNone(app.api_key)
    
    @patch('token_tongs.TokenTongs.run')
    def test_main_function(self, mock_run):
        """Test the main function"""
        with patch('token_tongs.TokenTongs', return_value=MagicMock()) as mock_app:
            main()
            mock_app.assert_called_once()
            mock_app.return_value.run.assert_called_once()

    def test_api_key_none_in_get_balance(self):
        """Test get_balance when api_key is None"""
        self.app.api_key = None
        self.assertIsNone(self.app.get_balance())

if __name__ == '__main__':
    unittest.main()