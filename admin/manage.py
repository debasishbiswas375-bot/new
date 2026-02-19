#!/usr/bin/env python
import os
import sys
import threading
import time
import requests

def keep_alive():
    # Pings both to keep them from sleeping
    urls = [
        "https://accountingexpert.onrender.com/admin/", 
        "https://tally-tools.streamlit.app/"
    ]
    time.sleep(30)
    while True:
        for url in urls:
            try:
                requests.get(url, timeout=10)
            except:
                pass
        time.sleep(840) # 14 minutes

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    # Start the pinger thread
    threading.Thread(target=keep_alive, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not found.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
