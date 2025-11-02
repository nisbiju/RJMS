#!/bin/bash

echo "================================================"
echo "Starting RJMS Application"
echo "================================================"
echo ""

# Kill any existing processes
pkill -f "python run.py" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Start Flask backend
echo "▶ Starting Flask backend (port 5000)..."
cd backend
python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 3
echo "✓ Backend started (PID: $BACKEND_PID)"

# Start Vue.js frontend  
echo "▶ Starting Vue.js frontend (port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 2
echo "✓ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "================================================"
echo "✓ RJMS is now running!"
echo "================================================"
echo ""
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:5173"
echo ""
echo "Open the Webview tab to access the application"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================"

# Wait and handle cleanup
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
