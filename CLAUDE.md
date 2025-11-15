# CLAUDE.md - Apache Access Log Parser

## Project Overview

This is an Apache web server access log parser with a plugin-based architecture for data extraction and enrichment. The application reads Apache access logs and processes them through customizable plugins to generate various statistics and visualizations.

**Primary Language**: Python 3
**License**: Apache 2.0
**Key Dependencies**: pygeoip (>=0.3.2), pygmaps (>=0.1.1)

## Codebase Structure

```
Apache-access-log-parser/
├── http_log_parser.py          # Main application entry point
├── manager.py                   # Plugin framework manager
├── requirements.txt             # Python dependencies
├── plugins/                     # Plugin modules directory
│   ├── __init__.py
│   ├── plugin_count_200.py     # Count HTTP 200 responses
│   ├── plugin_count_404.py     # Count HTTP 404 responses
│   ├── plugin_count_500.py     # Count HTTP 500 responses
│   ├── plugin_geoip_stats.py   # GeoIP country statistics
│   ├── plugin_geoip_stats_city.py  # GeoIP city statistics
│   └── plugin_map_cities.py    # Generate HTML maps with pygmaps
├── logs/                        # Apache log files directory
│   └── access.log              # Sample log file
├── geo_data_files/             # GeoIP database files
│   ├── GeoIP.dat               # Country-level GeoIP database
│   └── GeoLiteCity.dat         # City-level GeoIP database
├── maps/                        # Generated map output
├── tests/                       # Test suite
│   └── unitTests/
│       ├── test_calculations.py  # Main unit tests
│       └── test_me.py
├── superlists/                  # Django project (unrelated to main app)
└── README.md                    # Project documentation
```

## Architecture

### Three-Tier Plugin Architecture

1. **Main Application (`http_log_parser.py`)**
   - Reads Apache access log files
   - Parses log lines using configurable format strings
   - Invokes plugin framework for each log entry
   - Entry point: `main()` function

2. **Plugin Manager (`manager.py`)**
   - Discovers and loads plugin modules from `plugins/` directory
   - Manages plugin lifecycle (initialization, processing, reporting)
   - Provides base `Plugin` class for all plugins
   - Uses Python's dynamic import and class introspection

3. **Plugins (`plugins/plugin_*.py`)**
   - Self-contained modules for specific analysis tasks
   - Must inherit from `Plugin` base class
   - Implement three lifecycle methods: `__init__()`, `process()`, `report()`

### Log Format Handling

The application uses Apache's combined log format by default:

```
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
```

**Field Mappings** (defined in `http_log_parser.py:10-18`):
- `%h` → `remote_host`
- `%l` → `remote_logname`
- `%u` → `remote_user`
- `%t` → `time_stamp`
- `%r` → `request_line`
- `%>s` → `status`
- `%b` → `response_size`
- `%{Referer}i` → `referer_url`
- `%{User-Agent}i` → `user_agent`

## Plugin Development Guide

### Plugin Structure Template

All plugins must follow this structure:

```python
#!/usr/bin/env python3

from manager import Plugin

class MyPlugin(Plugin):
    """
    Brief description of what this plugin does
    """

    def __init__(self, **kwargs):
        """
        Plugin initialization - set up instance variables
        Optional: self.keywords = ['tag1', 'tag2'] for categorization
        """
        self.keywords = ['category']  # Optional
        # Initialize counters, data structures, etc.

    def process(self, **kwargs):
        """
        Called for EACH log line
        Access log fields via kwargs:
        - kwargs['remote_host']
        - kwargs['status']
        - kwargs['request_line']
        etc.
        """
        # Process individual log line
        pass

    def report(self, **kwargs):
        """
        Called ONCE after all log lines processed
        Generate and print final statistics/reports
        """
        # Print summary, generate files, etc.
        pass
```

### Plugin Naming Convention

- **File name**: `plugin_<descriptive_name>.py`
- **Location**: Must be in `plugins/` directory
- **Class name**: Capitalized, descriptive (e.g., `CountHTTP200`, `GeoIPStats`)
- **Automatic loading**: Plugin manager auto-discovers all `plugin_*.py` files

### Plugin Examples

**Simple Counter Plugin** (`plugin_count_200.py`):
- Counts HTTP 200 status codes
- Demonstrates basic counter pattern
- Uses `self.counter_200` and `self.counter_total`

**GeoIP Plugin** (`plugin_geoip_stats.py`):
- Performs IP-to-country lookups using GeoIP database
- Demonstrates external library integration (pygeoip)
- Uses proper path resolution for data files
- Handles missing database files gracefully

## Development Workflow

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd Apache-access-log-parser

# Install dependencies
pip install -r requirements.txt

# Verify GeoIP database files exist
ls geo_data_files/
```

### Running the Application

```bash
# Process logs in the logs/ directory
python ./http_log_parser.py

# The application automatically:
# 1. Loads all plugins from plugins/
# 2. Processes all log files in logs/
# 3. Calls process() for each log line
# 4. Calls report() when complete
```

### Creating a New Plugin

1. Create file: `plugins/plugin_<name>.py`
2. Import Plugin base class: `from manager import Plugin`
3. Define class inheriting from Plugin
4. Implement `__init__()`, `process()`, `report()` methods
5. No registration needed - auto-discovered on next run

### Testing

**Test Framework**: unittest (Python standard library)

**Test Location**: `tests/unitTests/test_calculations.py`

**Running Tests**:
```bash
cd tests/unitTests
python test_calculations.py
```

**Test Pattern**:
```python
import unittest
from plugins.plugin_count_200 import CountHTTP200
from manager import PluginManager

class TestApacheLogParser(unittest.TestCase):
    def test_plugin(self):
        simple = {'status': '200'}
        plugin_manager = PluginManager()
        plugin_manager.call_method(method='process', args=simple)

        for item in plugin_manager.plugins:
            if isinstance(item, CountHTTP200):
                self.assertEqual(1, item.counter_total)
                self.assertEqual(1, item.counter_200)
```

## Code Style and Conventions

### Python Version
- **Python 3** (migrated from Python 2 in commit d1acaf4)
- Use Python 3 syntax and features
- Shebang: `#!/usr/bin/env python3`

### Code Style
- **String formatting**: Use f-strings (e.g., `f"HTTP 200 responses: {self.counter_200}"`)
- **Imports**: Standard library first, then third-party, then local
- **Docstrings**: Use triple-quoted strings for class documentation
- **Error handling**: Main application has comprehensive exception handling

### Error Handling Pattern

The main application uses structured error handling:

```python
try:
    main()
except FileNotFoundError as e:
    print(f"Error: Log file or directory not found - {e}")
    sys.exit(1)
except KeyError as e:
    print(f"Error: Invalid log format or missing field - {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: An unexpected error occurred - {e}")
    traceback.print_exc()
    sys.exit(1)
```

### Path Resolution Best Practices

For plugins accessing data files:

```python
import os

# Get project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(project_root, 'geo_data_files', 'GeoIP.dat')

# Always check if file exists
if not os.path.exists(data_path):
    print(f"Warning: Data file not found at {data_path}")
    # Handle gracefully
```

## Key Components Deep Dive

### LogLineGenerator Class

**Purpose**: Parses Apache log files into structured dictionaries

**Key Methods**:
- `__init__(log_format=None, log_dir='logs')`: Configure format and log directory
- `get_loglines()`: Generator that yields parsed log dictionaries
- `_quote_translator()`: Internal - converts Apache timestamp brackets to quotes
- `_get_file_list()`: Internal - discovers log files in directory

**Usage**:
```python
# Default combined format
log_generator = LogLineGenerator()

# Custom log format
log_generator = LogLineGenerator(log_format='%h %l %u %t %r %>s %b')

# Iterate through parsed lines
for log_line in log_generator.get_loglines():
    # log_line is a dict with keys: remote_host, status, etc.
    pass
```

### PluginManager Class

**Purpose**: Dynamic plugin discovery and lifecycle management

**Key Methods**:
- `__init__(path=None, plugin_init_args={})`: Load and register plugins
- `_load_plugins()`: Discovers and imports plugin modules
- `_register_plugins(**kwargs)`: Instantiates plugin classes
- `call_method(method, args={})`: Invokes method on all plugins

**Plugin Discovery Mechanism**:
1. Lists all files in `plugins/` directory
2. Filters for files matching `plugin_*.py`
3. Dynamically imports each module
4. Uses `Plugin.__subclasses__()` to find plugin classes
5. Instantiates each plugin with optional init args

## Common Tasks for AI Assistants

### 1. Adding a New Plugin

**Task**: Create a plugin to count HTTP 500 errors

**Steps**:
1. Create `plugins/plugin_count_500.py`
2. Copy structure from `plugin_count_404.py`
3. Modify to check `kwargs['status'] == '500'`
4. Update class name and docstring
5. Test by running main application

### 2. Modifying Log Format

**Task**: Support Common Log Format (without referrer/user-agent)

**Steps**:
1. Identify the format string: `%h %l %u %t %r %>s %b`
2. Ensure FIELD_MAPPINGS has all required fields
3. Modify LogLineGenerator initialization in `main()`:
   ```python
   log_generator = LogLineGenerator(log_format='%h %l %u %t %r %>s %b')
   ```

### 3. Adding New Field Mapping

**Task**: Support response time logging

**Steps**:
1. Add to FIELD_MAPPINGS in `http_log_parser.py`:
   ```python
   '%T': 'response_time',  # or %D for microseconds
   ```
2. Update log format string when initializing LogLineGenerator
3. Access in plugins via `kwargs['response_time']`

### 4. Debugging Plugin Issues

**Common Issues**:
- Plugin not loading: Check file naming (`plugin_*.py`)
- Missing data: Check kwargs keys in `process()` method
- Import errors: Ensure `from manager import Plugin` is present
- Path errors: Use absolute path resolution from project root

### 5. Writing Tests for New Plugins

**Pattern**:
```python
def test_my_plugin(self):
    test_data = {'status': '500', 'remote_host': '127.0.0.1'}
    plugin_manager = PluginManager()
    plugin_manager.call_method(method='process', args=test_data)

    for item in plugin_manager.plugins:
        if isinstance(item, MyPlugin):
            self.assertEqual(expected_value, item.some_counter)
```

## Important Notes for AI Assistants

### Recent Changes (Commit d1acaf4)
- **Python 3 migration**: All code now uses Python 3 syntax
- **f-strings**: Updated from %-formatting to f-strings
- **print statements**: Changed from Python 2 print to Python 3 print()
- **Error handling**: Added comprehensive exception handling to main application

### File Organization
- **Main application files**: Root directory
- **Plugins**: `plugins/` directory only
- **Tests**: `tests/unitTests/`
- **Data files**: `geo_data_files/`
- **Logs**: `logs/` directory

### Unrelated Components
- **`superlists/` directory**: Contains a Django project unrelated to the log parser
- **Action**: Ignore this directory when working on log parser functionality
- **Note**: This appears to be test/demo code that should potentially be removed

### Git Workflow
- **Main branch**: Use for stable releases
- **Feature branches**: Prefix with `claude/` for AI-generated work
- **Commit messages**: Descriptive, focus on "why" not "what"
- **Testing**: Run unit tests before committing

### Dependencies Management
- **requirements.txt**: Add new dependencies here
- **GeoIP databases**: Binary files, not in version control (should be downloaded separately)
- **pygeoip**: Required for GeoIP plugins
- **pygmaps**: Required for map generation plugins

### Performance Considerations
- Uses generators for memory-efficient log processing
- Can handle large log files without loading entire file into memory
- Plugin architecture allows selective feature enabling

### Security Considerations
- Input validation: Ensure plugins handle malformed log lines gracefully
- Path traversal: Always use os.path.join() for file paths
- External data: GeoIP databases should be from trusted sources
- No user input: Application reads log files only, no interactive input

## Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run log parser
python ./http_log_parser.py

# Run tests
cd tests/unitTests && python test_calculations.py

# View available plugins
ls plugins/plugin_*.py

# Check Python version
python --version  # Should be Python 3.x

# Git workflow
git checkout -b claude/feature-name
git add .
git commit -m "Descriptive message"
git push -u origin claude/feature-name
```

## Troubleshooting

### "No module named 'manager'"
- Ensure you're running from project root directory
- Check that `manager.py` exists in current directory

### "FileNotFoundError: logs"
- Create `logs/` directory
- Add Apache access log files to `logs/` directory

### "GeoIP database not found"
- Download GeoIP database files
- Place in `geo_data_files/` directory
- Plugins should handle gracefully with warning message

### Plugin not executing
- Check filename starts with `plugin_`
- Verify class inherits from `Plugin`
- Ensure `process()` and `report()` methods exist
- Check for Python syntax errors in plugin file

---

**Last Updated**: 2025-11-15
**Current Branch**: claude/claude-md-mhzn5yajllh4y5xh-01Nhn1RHoPnfKCRG35ZTEAXz
**Recent Commits**: Python 3 migration, bug fixes, test additions
