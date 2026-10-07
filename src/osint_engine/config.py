import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SHODAN_API_KEY: str = os.getenv("SHODAN_API_KEY", "")
    VIRUSTOTAL_API_KEY: str = os.getenv("VIRUSTOTAL_API_KEY", "")
    REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "10.0"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

config = Config()