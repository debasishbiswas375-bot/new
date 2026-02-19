#!/usr/bin/env python
import os
import sys
import threading
import time
import requests

# --- KEEP ALIVE THREAD ---
def keep_alive():
    # Replace with your actual URLs
    RENDER_URL = "https://accountingexpert.onrender.com/admin/"
    STREAMLIT_URL = "https://tally-tools.streamlit.app"
    
    time.sleep(20) # Wait for server to boot
    while True:
        try:
            requests.get(RENDER_URL)
            requests.get(STREAMLIT_URL)
            # This will show in your Render logs
            print("Pinger: Both sites are awake.") 
        except Exception as e:
            print(f"Pinger Error: {e}")
        time.sleep(840) # 14 minutes

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    # Start the pinger only when running the server
    if 'runserver' in sys.argv:
        threading.Thread(target=keep_alive, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
