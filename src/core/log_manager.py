import logging
import os
from datetime import datetime

class LogManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not LogManager._initialized:
            self.setup_logging()
            LogManager._initialized = True
    
    def setup_logging(self):
        """Set up logging configuration."""
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Create a log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/system_changes_{timestamp}.log'
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also print to console
            ]
        )
    
    def get_logger(self, feature_name: str) -> logging.Logger:
        """
        Get a logger instance for a specific feature.
        
        Args:
            feature_name: Name of the feature (e.g., 'Cortana', 'Telemetry')
            
        Returns:
            logging.Logger: Configured logger instance
        """
        return logging.getLogger(feature_name)
    
    def log_operation(self, logger: logging.Logger, operation: str, status: str, details: str = None):
        """
        Log an operation with consistent formatting.
        
        Args:
            logger: Logger instance
            operation: Name of the operation being performed
            status: Status of the operation ('success' or 'error')
            details: Additional details about the operation
        """
        if status.lower() == 'success':
            logger.info(f"Operation '{operation}' completed successfully")
        else:
            logger.error(f"Operation '{operation}' failed")
        
        if details:
            logger.info(f"Details: {details}")
    
    def log_registry_change(self, logger: logging.Logger, path: str, values: dict, success: bool):
        """
        Log registry changes with consistent formatting.
        
        Args:
            logger: Logger instance
            path: Registry path being modified
            values: Dictionary of values being set
            success: Whether the operation was successful
        """
        if success:
            logger.info(f"Registry path modified: {path}")
            logger.info(f"Values set: {values}")
        else:
            logger.error(f"Failed to modify registry path: {path}")
    
    def log_service_change(self, logger: logging.Logger, service_name: str, action: str, success: bool):
        """
        Log service changes with consistent formatting.
        
        Args:
            logger: Logger instance
            service_name: Name of the service
            action: Action performed (e.g., 'stop', 'disable')
            success: Whether the operation was successful
        """
        if success:
            logger.info(f"Service '{service_name}' {action}ed successfully")
        else:
            logger.error(f"Failed to {action} service '{service_name}'")
    
    def log_task_change(self, logger: logging.Logger, task_name: str, action: str, success: bool):
        """
        Log task changes with consistent formatting.
        
        Args:
            logger: Logger instance
            task_name: Name of the task
            action: Action performed (e.g., 'disable', 'enable')
            success: Whether the operation was successful
        """
        if success:
            logger.info(f"Task '{task_name}' {action}ed successfully")
        else:
            logger.error(f"Failed to {action} task '{task_name}'") 