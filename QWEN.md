# MDM Web UI Automation Testing Framework

## Project Overview

This is a **Playwright-based UI automation testing framework** for MDM (Mobile Device Management) web applications. It provides automated login with OCR captcha recognition, session-scoped browser fixtures, and multi-environment configuration.

**Key Features:**
- **Multi-environment configuration** (`config/env.yaml`) — centralized management of URLs, usernames, and passwords
- **Session-scoped browser and page** — single Chromium instance shared across all tests for speed
- **Auto-login with OCR captcha** (`ddddocr`) — automatic captcha recognition with retry logic
- **Screenshot capture on failure** — `@capture_exceptions` decorator auto-captures failure screenshots
- **OpenSpec workflow integration** — structured feature development via `openspec/`

**Tech Stack:**
| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.7+ | Runtime (tested on 3.7, 3.9) |
| Playwright | 1.35.0 | Browser automation (Chromium) |
| pytest | 7.0.0 | Test runner and fixture management |
| ddddocr | latest | OCR captcha recognition |
| PyYAML | 5.4.1 | Environment config parsing |

## Project Structure

```
D:\mdm\
├── conftest.py           # pytest fixtures: browser, page, auto_login, env_config
── requirements.txt      # Python dependencies
├── .gitignore
├── README.md
├── QWEN.md               # This file — project context
├── config/
│   ├── __init__.py
│   └── env.yaml          # Environment URLs, usernames, passwords (CURRENT_ENV in conftest.py)
├── utils/
│   ├── __init__.py
│   └── toolkit.py        # Utils: logger, screenshot, file finder, @capture_exceptions
├── TestCase/
│   ├── __init__.py
│   └── test_*.py         # Test cases
├── screenshots/          # Auto-generated failure screenshots (git-ignored)
└── openspec/             # OpenSpec workflow files (config.yaml, changes/, specs/)
```

## Environment Configuration

### Switching Environments

Edit `CURRENT_ENV` at the top of `conftest.py`:

```python
CURRENT_ENV = "test"  # "dev", "test", "prod"
```

### Config File (`config/env.yaml`)

```yaml
environments:
  test:
    base_url: "https://test-platform.easycontrol.io/mdm-web/Login"
    username: "ui"
    password: "Admin@135790"
```

Currently configured environments:
- **test**: `https://test-platform.easycontrol.io/mdm-web/Login` (user: `ui`)
- Additional environments can be added to `env.yaml`

## Running Tests

### Prerequisites

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install ddddocr

# Install Playwright browser
playwright install chromium
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest TestCase/test_login_verify.py -v

# Run tests matching a keyword
pytest -k "login" -v

# Debug mode (browser stays open after tests)
DEBUG=1 pytest -v -s
```

## Writing New Tests

1. Create `test_<feature>_<scenario>.py` in `TestCase/`
2. Import required fixtures: `page`, `env_config`
3. Use `@capture_exceptions` decorator for auto-screenshot on failure

### Template

```python
from utils.toolkit import capture_exceptions

@capture_exceptions
def test_my_feature(page, env_config):
    """Test description here"""
    page.goto(f"{env_config.base_url}/#/my-page")
    page.wait_for_selector(".expected-element")
    assert "Expected Title" in page.title()
```

### Key Fixtures (from `conftest.py`)

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `env_config` | session | Loads environment config from `env.yaml` |
| `browser` | session | Launches Chromium (headed, 1920x1080, `--no-sandbox`) |
| `page` | session | Creates single browser page shared by all tests |
| `auto_login` | session | Auto-logs in before tests run (OCR captcha + retry logic) |

### Architecture Notes

- **Session-scoped page**: All tests share one page context. This is fast but means tests can interfere with each other. Consider switching to `function` scope if test isolation becomes an issue.
- **Auto-login**: Uses `ddddocr` for captcha recognition. Login form uses placeholder-based selectors.
- **Error handling**: The `@capture_exceptions` decorator automatically captures screenshots on test failure and saves them to `screenshots/`.

## AI Visual Verification (Disabled)

The `utils/toolkit.py` contains commented-out code for AI-assisted visual verification using DashScope's `qwen-vl-plus` model. It can check screenshots for "success" messages. To re-enable:

1. Set `DASHSCOPE_API_KEY` environment variable
2. Uncomment the `ai_check_success` function and imports
3. Call `ai_check_success(screenshot_path)` in tests

## Development Conventions

- **File naming**: `test_*.py` for pytest discovery
- **Fixtures**: Use `page` and `env_config` from `conftest.py`
- **Screenshots**: Saved to `screenshots/` with safe filenames (alphanumeric + underscores)
- **Logging**: Use `Utils.get_logger(__name__)` for structured output
- **Error handling**: Use `@capture_exceptions` decorator for automatic failure capture
- **Helper scripts**: Place debug/exploration scripts in `scripts/` — they are NOT collected by pytest

## Known Issues / TODOs

1. **Session-scoped page**: All tests share one page context; may need function scope for isolation
2. **AI verification**: DashScope AI integration is commented out — needs API key to enable
3. **Captcha OCR accuracy**: `ddddocr` recognition rate varies; retry logic helps but not 100% reliable
