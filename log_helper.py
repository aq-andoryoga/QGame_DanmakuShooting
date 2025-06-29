#!/usr/bin/env python3
"""
Development Log Helper
Utility for logging development activities and prompts
"""

import datetime
import os

class DevLogger:
    """Helper class for logging development activities."""
    
    def __init__(self, log_file="development_log.txt"):
        """Initialize the logger with a log file."""
        self.log_file = log_file
        self.ensure_log_exists()
    
    def ensure_log_exists(self):
        """Ensure the log file exists."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("QGamen_DanmakuShooting Development Log\n")
                f.write("=====================================\n")
                f.write(f"Started: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
    
    def log_prompt(self, prompt_text):
        """Log a user prompt."""
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] USER PROMPT:\n")
            f.write(f"{prompt_text}\n\n")
    
    def log_output(self, output_text):
        """Log system output/response."""
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] SYSTEM OUTPUT:\n")
            f.write(f"{output_text}\n")
            f.write("=" * 50 + "\n\n")
    
    def log_activity(self, activity_description):
        """Log a development activity."""
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] ACTIVITY: {activity_description}\n\n")

# Create a global logger instance
logger = DevLogger()

def log_prompt_and_response(prompt, response):
    """Convenience function to log both prompt and response."""
    logger.log_prompt(prompt)
    logger.log_output(response)
