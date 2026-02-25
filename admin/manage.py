import threading
import time
import requests
import os
import sys

def keep_alive_loop():
    # Pings both sites every 14 minutes to reset Render's 15-minute sleep timer
    targets = [
        "https://accountingexpert.onrender.com/admin/",
        "https://newtool.streamlit.app/"
    ]
    time.sleep(20) # Wait for startup
    while True:
        for url in targets:
            try:
                requests.get(url, timeout=10)
            except:
                pass
        time.sleep(840) # 14 minutes

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    # Start the pinger background thread
    threading.Thread(target=keep_alive_loop, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not found.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
