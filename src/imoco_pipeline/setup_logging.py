import logging


logger = logging.getLogger('scan_logger')
logger.setLevel(logging.INFO)

# Check if handlers are already attached to avoid duplicate logs
if not logger.handlers:
    # Create a StreamHandler to log to the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Define the log message format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    # Attach the handler to the logger
    logger.addHandler(ch)

# Test 
logger.info("Logger setup complete.")
