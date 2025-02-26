# TokenTongs

A system tray application that monitors and displays your AI provider balances.


## Description

TokenTongs is a lightweight system tray application that helps you monitor your AI service provider credits and usage. It sits quietly in your system tray/menu bar and displays your current balance, updating periodically to keep you informed about your AI credit usage.

Currently supported providers:
- OpenRouter

Future planned providers:
- Anthropic
- OpenAI

## Features

- Real-time balance monitoring in your system tray
- Periodic automatic updates (every 30 minutes)
- Detailed information including:
  - Current remaining balance
  - Total credits
  - Total usage
  - Last update time
  - Provider information

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/utensils/token-tongs
   cd token-tongs
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key as an environment variable:
   ```bash
   # For bash/zsh (make sure to export the variable)
   export OPENROUTER_API_KEY="your-api-key-here"
   
   # For Windows Command Prompt
   set OPENROUTER_API_KEY=your-api-key-here
   
   # For Windows PowerShell
   $env:OPENROUTER_API_KEY="your-api-key-here"
   ```

   **Important**: The environment variable must be exported in the same shell session where you run the application. If you're using a nix-shell or virtual environment, make sure to set the environment variable after activating the environment.

   You can also add the export command to your shell profile file (e.g., `~/.bashrc`, `~/.zshrc`) to make it persistent across sessions:
   ```bash
   echo 'export OPENROUTER_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

Run the application:

```bash
python token_tongs.py
```

Or if you've made the script executable:

```bash
./token_tongs.py
```

For convenience, you can also use the included helper script which will prompt for your API key if it's not set:

```bash
./run_token_tongs.sh
```

You can also pass your API key directly to the script:

```bash
./run_token_tongs.sh your-api-key-here
```

The application will appear in your system tray/menu bar, displaying your current balance. Click on the icon to see more detailed information.

## Development

### Creating a requirements.txt

```bash
pip freeze > requirements.txt
```

### Running Tests

TokenTongs comes with a comprehensive test suite that ensures the application works correctly. The tests use mocking to avoid making real API calls, so you don't need a real API key to run the tests.

To run the tests:

```bash
# Install test dependencies
pip install -r test-requirements.txt

# Run tests with pytest
pytest tests/

# Run tests with coverage report
./run_tests.sh
```

Current test coverage: 98%

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [rumps](https://github.com/jaredks/rumps) - Ridiculously Uncomplicated macOS Python Statusbar apps
- [OpenRouter](https://openrouter.ai) - API for accessing various AI models
