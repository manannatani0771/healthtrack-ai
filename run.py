import os
import sys
import webbrowser
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")
    print("=" * 62)
    print("  HEALTH TRACK AI — LOCAL DYNAMIC SERVER")
    print(f"  Interface: http://{host}:{port}")
    print("  Database : data/healthtrack.db (SQLite)")
    print("  Privacy  : 100% Local-First (DPDP Compliant, No Cloud Uploads)")
    print("=" * 62)
    
    # Automatically open default web browser
    webbrowser.open(f"http://{host}:{port}")
    
    # Start FastAPI server
    uvicorn.run("src.server:app", host=host, port=port, reload=False)
