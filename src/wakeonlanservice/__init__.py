import logging
from flask import Flask
import os
import re

from wakeonlanservice.logging_config import setup_logging

# Import blueprints
from wakeonlanservice.blueprints.status import parse_redirect_setting, status_bp

def create_app(test_config=None) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): Configuration dictionary for testing.
    
    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", os.urandom(24)),
        TESTING=False,
    )

    # Apply the test configuration if provided
    if test_config:
        app.config.update(test_config)

    # Set up logging
    setup_logging(app.debug)

    # Validate environment variables
    validate_env_variables()

    # Register blueprints
    app.register_blueprint(status_bp)

    logger = logging.getLogger(__name__)
    logger.info("App created successfully")

    return app

def validate_env_variables() -> None:
    """
    Validate the required environment variables.
    
    Raises:
        ValueError: If any required environment variable is missing or invalid.
    """
    logger = logging.getLogger(__name__)

    # Get MAC address and URL from environment variables
    mac_address = os.getenv("MAC_ADDRESS")
    url = os.getenv("URL")

    # Validate MAC address
    if not mac_address or not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address):
        logger.error("Invalid or missing MAC_ADDRESS environment variable")
        raise ValueError("Invalid or missing MAC_ADDRESS environment variable")

    # Validate URL
    if not url or not re.match(r"^(http|https)://", url):
        logger.error("Invalid or missing URL environment variable")
        raise ValueError("Invalid or missing URL environment variable")

    # Validate REDIRECT_ON_AVAILABLE (optional; unset or empty means true)
    if parse_redirect_setting(os.getenv("REDIRECT_ON_AVAILABLE")) is None:
        logger.error("Invalid REDIRECT_ON_AVAILABLE environment variable")
        raise ValueError("Invalid REDIRECT_ON_AVAILABLE environment variable")