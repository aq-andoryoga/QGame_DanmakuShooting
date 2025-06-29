"""
Log Helper for QGamen_DanmakuShooting
Provides logging utilities for development and debugging
"""

import datetime
import os

class LogHelper:
    """Helper class for logging game events and development progress."""
    
    def __init__(self, log_file="development_log.txt"):
        """Initialize the log helper."""
        self.log_file = log_file
        self.ensure_log_file()
    
    def ensure_log_file(self):
        """Ensure the log file exists."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("# QGamen Development Log\n")
                f.write(f"Log started: {datetime.datetime.now()}\n\n")
    
    def log(self, message, level="INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # Print to console
        print(log_entry.strip())
        
        # Write to file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def log_info(self, message):
        """Log an info message."""
        self.log(message, "INFO")
    
    def log_warning(self, message):
        """Log a warning message."""
        self.log(message, "WARNING")
    
    def log_error(self, message):
        """Log an error message."""
        self.log(message, "ERROR")
    
    def log_debug(self, message):
        """Log a debug message."""
        self.log(message, "DEBUG")
    
    def log_game_event(self, event_type, details):
        """Log a game event."""
        message = f"GAME_EVENT - {event_type}: {details}"
        self.log(message, "GAME")
    
    def log_performance(self, function_name, execution_time):
        """Log performance metrics."""
        message = f"PERFORMANCE - {function_name}: {execution_time:.4f}s"
        self.log(message, "PERF")
    
    def log_user_action(self, action, context=""):
        """Log user actions."""
        message = f"USER_ACTION - {action}"
        if context:
            message += f" ({context})"
        self.log(message, "USER")
    
    def log_system_info(self, info):
        """Log system information."""
        self.log(f"SYSTEM_INFO - {info}", "SYSTEM")
    
    def add_separator(self, title=""):
        """Add a separator line to the log."""
        separator = "=" * 50
        if title:
            separator = f"=== {title} " + "=" * (50 - len(title) - 5)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{separator}\n")
    
    def log_milestone(self, milestone):
        """Log a development milestone."""
        self.add_separator(f"MILESTONE: {milestone}")
        self.log(f"🎯 MILESTONE REACHED: {milestone}", "MILESTONE")
        self.add_separator()

# Global log helper instance
logger = LogHelper()

# Convenience functions
def log_info(message):
    """Log an info message."""
    logger.log_info(message)

def log_warning(message):
    """Log a warning message."""
    logger.log_warning(message)

def log_error(message):
    """Log an error message."""
    logger.log_error(message)

def log_debug(message):
    """Log a debug message."""
    logger.log_debug(message)

def log_game_event(event_type, details):
    """Log a game event."""
    logger.log_game_event(event_type, details)

def log_performance(function_name, execution_time):
    """Log performance metrics."""
    logger.log_performance(function_name, execution_time)

def log_user_action(action, context=""):
    """Log user actions."""
    logger.log_user_action(action, context)

def log_milestone(milestone):
    """Log a development milestone."""
    logger.log_milestone(milestone)

# Example usage:
if __name__ == "__main__":
    log_info("Log helper initialized")
    log_game_event("PLAYER_SPAWN", "Player spawned at (400, 600)")
    log_user_action("BOMB_USED", "2 bombs remaining")
    log_performance("draw_game", 0.0167)
    log_milestone("UI System Completed")
