# Image Steganography v2.0 - Modular Architecture

## Overview

This is version 2.0 of the Image Steganography application, featuring a complete rewrite with a modular architecture designed for extensibility, maintainability, and code quality.

## Project Structure

```
.
├── gui/                 # Graphical User Interface module
│   ├── __init__.py     # GUI module interface
│   └── ...             # GUI components (windows, widgets, controllers)
│
├── core/               # Core steganography engine
│   ├── __init__.py    # Core module interface
│   ├── base.py        # Base classes and interfaces
│   └── ...            # Algorithms, encoders, decoders
│
├── plugins/            # Plugin system for extensibility
│   ├── __init__.py    # Plugin module interface
│   ├── base.py        # Plugin base classes
│   └── ...            # Custom plugins
│
├── utils/              # Utility functions and helpers
│   ├── __init__.py    # Utils module interface
│   └── ...            # Validators, file handlers, crypto helpers
│
├── tests/              # Test suite
│   ├── __init__.py    # Test configuration
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   ├── data/          # Test data
│   └── output/        # Test output directory
│
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── .flake8                  # Flake8 linting configuration
├── pyproject.toml           # Project metadata and tool configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── Makefile                 # Common development tasks
```

## Key Features of v2

### 1. Modular Architecture
- **Clear separation of concerns**: Each module has a specific responsibility
- **Well-defined interfaces**: All modules expose clear APIs through `__init__.py`
- **Plugin system**: Extensible architecture for adding new algorithms and filters

### 2. Code Quality Enforcement
Pre-commit hooks automatically enforce:
- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting
- **Flake8**: Linting with Google docstring convention
- **MyPy**: Static type checking

### 3. Module Interfaces

#### GUI Module (`gui/`)
- User interface components
- Event handling
- Visualization tools

#### Core Module (`core/`)
- Steganography algorithms
- Image processing
- Encoding/decoding engines

#### Plugins Module (`plugins/`)
- Plugin discovery and loading
- Custom algorithm plugins
- Image filter plugins

#### Utils Module (`utils/`)
- Common utilities
- File handling
- Validation
- Configuration management

## Development Setup

### 1. Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### 2. Install Pre-commit Hooks
```bash
pre-commit install
```

### 3. Run Code Quality Checks
```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Run all pre-commit hooks
make pre-commit
```

### 4. Running Tests
```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

## Development Workflow

1. **Create feature branch from v2**
   ```bash
   git checkout -b feature/your-feature v2
   ```

2. **Write code following the modular structure**
   - Place code in appropriate modules
   - Follow interface definitions
   - Add type hints
   - Write docstrings

3. **Pre-commit hooks run automatically on commit**
   - Fixes formatting issues
   - Checks for linting errors
   - Validates types

4. **Write tests**
   - Unit tests in `tests/unit/`
   - Integration tests in `tests/integration/`

5. **Submit pull request to v2 branch**

## Code Style Guidelines

- **PEP 8 compliant** with Black formatting
- **Google-style docstrings**
- **Type hints** for all functions
- **Maximum line length**: 88 characters
- **Import sorting**: isort with Black profile

## Migration from v1

The v2 architecture is a complete rewrite. Key differences:
- Modular structure vs monolithic
- Plugin system for extensibility
- Strict code quality enforcement
- Comprehensive test coverage
- Type safety with MyPy

## Contributing

Please ensure all code:
1. Passes pre-commit hooks
2. Has appropriate tests
3. Includes proper documentation
4. Follows the modular architecture

## License

[Your License Here]

## Version History

- **v2.0.0** - Complete rewrite with modular architecture
- **v1.x.x** - Original implementation
