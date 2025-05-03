# lambda_function.py

from src.watcher import run_daily_check
import logging

if __name__ == "__main__":
    run_daily_check()