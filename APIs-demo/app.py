from fastapi import FastAPI
from config  import config



app = FastAPI( 
        title="FastAPI inventory management",
        description="FastAPI rest endpoints by Bradley Kibwana",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc"
        )
