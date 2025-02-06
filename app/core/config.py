from typing import Optional

from pydantic import BaseSettings

from app.constants import (
    DEFAULT_APP_TITLE, DEFAULT_APP_DESCRIPTION, DEFAULT_DATABASE_URL,
    DEFAULT_SECRET
)


class Settings(BaseSettings):
    app_title: str = DEFAULT_APP_TITLE
    app_description: str = DEFAULT_APP_DESCRIPTION
    database_url: str = DEFAULT_DATABASE_URL
    secret: str = DEFAULT_SECRET
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
