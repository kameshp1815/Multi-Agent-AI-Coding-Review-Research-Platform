import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_name = os.getenv("DB_NAME", "bean_brew_db")
        self.db_username = os.getenv("DB_USERNAME", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "Admin123")

        self.port = int(os.getenv("PORT", "8080"))
        self.host = os.getenv("HOST", "0.0.0.0")

        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.model_id = os.getenv("MODEL_ID", "")
        self.provider = os.getenv("MODEL_PROVIDER", "amazon")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.3"))
        self.mcp_server_url=os.getenv("MCP_SERVER_PEP8_URL","")
        self.mcp_server_url_ddg=os.getenv("MCP_DUCK_DUCK_GO_URL","")

settings = Settings()