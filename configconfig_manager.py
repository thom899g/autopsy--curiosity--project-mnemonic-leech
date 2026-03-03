"""
Configuration Manager for Project Mnemonic Leech
Handles environment variables, validation, and provides typed configuration
"""
import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    client_x509_cert_url: str
    
    def validate(self) -> None:
        """Validate Firebase configuration"""
        required_fields = [
            ('project_id', self.project_id),
            ('private_key', self.private_key),
            ('client_email', self.client_email)
        ]
        
        for field_name, value in required_fields:
            if not value or value.startswith('your-'):
                raise ValueError(f"Invalid Firebase configuration: {field_name} is not set")

@dataclass
class SystemConfig:
    """System-wide configuration"""
    log_level: str
    max_retries: int
    retry_delay_seconds: int
    batch_size: int
    
    @classmethod
    def from_env(cls) -> 'SystemConfig':
        """Create SystemConfig from environment variables"""
        return cls(
            log_level=os.getenv('MNEMONIC_LEECH_LOG_LEVEL', 'INFO').upper(),
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            retry_delay_seconds=int(os.getenv('RETRY_DELAY_SECONDS', '5')),
            batch_size=int(os.getenv('BATCH_SIZE', '100'))
        )

class ConfigManager:
    """Centralized configuration management with validation"""
    
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize configuration with validation"""
        try:
            # Initialize Firebase config
            self.firebase = FirebaseConfig(
                project_id=os.getenv('FIREBASE_PROJECT_ID', ''),
                private_key_id=os.getenv('FIREBASE_PRIVATE_KEY_ID', ''),
                private_key=os.getenv('FIREBASE_PRIVATE_KEY', ''),
                client_email=os.getenv('FIREBASE_CLIENT_EMAIL', ''),
                client_id=os.getenv('FIREBASE_CLIENT_ID', ''),
                client_x509_cert_url=os.getenv('FIREBASE_CLIENT_X509_CERT_URL', '')
            )
            
            # Validate Firebase config
            self.firebase.validate()
            
            # Initialize system config
            self.system = SystemConfig.from_env()
            
            # Initialize optional configurations with defaults
            self.feature_flags: Dict[str, bool] = {
                'enable_backup': True,
                'enable_compression': False,
                'enable_encryption': True
            }
            
        except ValueError as e:
            logging.error(f"Configuration validation failed: {e}")
            raise
    
    def get_feature_flag(self, flag_name: str) -> bool:
        """Get feature flag value with fallback"""
        return self.feature_flags.get(flag_name, False)
    
    def reload(self) -> None:
        """Reload configuration from environment"""
        self._initialize()