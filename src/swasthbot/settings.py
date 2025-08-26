from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = Field(default='SwasthBot')
    app_env: str = Field(default='dev')

    auth_disabled: bool = Field(default=False, alias='AUTH_DISABLED')
    jwt_secret: str = Field(default='change-me', alias='JWT_SECRET')
    jwt_issuer: str = Field(default='swasthbot', alias='JWT_ISSUER')

    rate_limit_per_min: int = Field(default=60, alias='RATE_LIMIT_PER_MIN')

    llm_provider: str = Field(default='offline', alias='LLM_PROVIDER')
    openai_api_key: str | None = Field(default=None, alias='OPENAI_API_KEY')
    openai_model: str = Field(default='gpt-4o-mini', alias='OPENAI_MODEL')

    redact_logs: bool = Field(default=True, alias='REDACT_LOGS')

settings = Settings()
