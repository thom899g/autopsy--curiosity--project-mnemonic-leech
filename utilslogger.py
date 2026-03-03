"""
Robust logging utility with structured logging and error tracking
"""
import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
from config.config_manager import ConfigManager

class StructuredFormatter(logging.Formatter):
    """JSON-formatted structured logging for better parsing and analysis"""
    
    def format(self