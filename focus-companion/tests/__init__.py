"""
Test package for Focus Companion application
Contains unit tests and integration tests for all components
"""

__version__ = "1.0.0"
__author__ = "Focus Companion Team"

# Test categories
TEST_CATEGORIES = {
    "unit": [
        "test_storage",
        "test_logic", 
        "test_fallback",
        "test_prompts"
    ],
    "integration": [
        "test_mood_logging"
    ]
}

# Test coverage targets
COVERAGE_TARGETS = {
    "data": 95,      # Storage system
    "assistant": 90,  # Assistant logic and prompts
    "overall": 85    # Overall application
} 