"""DEFAULT VARIABLES"""
import os


# >>>>>>>>>API CONFIGS>>>>>>>>>
STOP_JWT_SECRET_KEY = os.getenv("STOP_JWT_SECRET_KEY", "")
# <<<<<<<<<API CONFIGS<<<<<<<<<

# >>>>>>>>>DATABASE CONFIGS>>>>>>>>>
STOP_SQLALCHEMY_DATABASE_URI = os.getenv("STOP_SQLALCHEMY_DATABASE_URI", "")
STOP_SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("STOP_SQLALCHEMY_TRACK_MODIFICATIONS", "")
# <<<<<<<<<DATABASE CONFIGS<<<<<<<<<
