import os
from typing import Optional

class DatabaseConfig:
    """Database configuration settings"""
    
    # Database connection settings - Updated for existing SmartTransitApp database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "SmartTransitApp")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "palak003")
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the complete database URL"""
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @classmethod
    def update_connection(cls, host: str, port: str, database: str, username: str, password: str):
        """Update database connection settings"""
        cls.DB_HOST = host
        cls.DB_PORT = port
        cls.DB_NAME = database
        cls.DB_USER = username
        cls.DB_PASSWORD = password

# Default configuration for existing SmartTransitApp database
DatabaseConfig.update_connection("localhost", "3306", "SmartTransitApp", "root", "palak003") 