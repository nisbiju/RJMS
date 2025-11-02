#!/usr/bin/env python3
"""
RJMS Application Launcher
Starts Flask backend and Vue.js frontend
"""

import subprocess
import sys
import time
import signal
import os

# Process references
backend_process = None
frontend_process = None

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print('\n\nShutting down services...')
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    global backend_process, frontend_process
    
    print('=' * 50)
    print('Starting RJMS Application')
    print('=' * 50)
    print()
    
    # Start Flask backend
    print('▶ Starting Flask backend (port 5000)...')
    backend_process = subprocess.Popen(
        ['python', 'run.py'],
        cwd=os.path.join(os.path.dirname(__file__), 'backend'),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Wait for backend to start
    time.sleep(3)
    
    if backend_process.poll() is not None:
        print('✗ Backend failed to start')
        sys.exit(1)
    
    print('✓ Backend started')
    print()
    
    # Start Vue.js frontend
    print('▶ Starting Vue.js frontend (port 5173)...')
    frontend_process = subprocess.Popen(
        ['npm', '--prefix', 'frontend', 'run', 'dev'],
        cwd=os.path.dirname(__file__),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    print('✓ Frontend starting...')
    print()
    print('=' * 50)
    print('✓ RJMS is running!')
    print('=' * 50)
    print()
    print('Backend API:  http://localhost:5000')
    print('Frontend UI:  http://localhost:5173')
    print()
    print('Open the Webview tab to access the application')
    print()
    print('Press Ctrl+C to stop')
    print('=' * 50)
    print()
    
    # Stream output from both processes
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print('Backend process exited unexpectedly')
                break
            
            if frontend_process.poll() is not None:
                print('Frontend process exited unexpectedly')
                break
            
            # Read and print backend output
            if backend_process.stdout:
                line = backend_process.stdout.readline()
                if line:
                    print(f'[Backend] {line.strip()}')
            
            # Read and print frontend output
            if frontend_process.stdout:
                line = frontend_process.stdout.readline()
                if line:
                    print(f'[Frontend] {line.strip()}')
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        signal_handler(None, None)
    
    # Clean up
    if backend_process:
        backend_process.terminate()
        backend_process.wait()
    
    if frontend_process:
        frontend_process.terminate()
        frontend_process.wait()

if __name__ == '__main__':
    main()
