#!/bin/bash

# Kill any existing processes on ports 5000 and 5173
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo "=========================================="
echo "Starting RJMS Application"
echo "=========================================="

# Start Flask backend
echo "Starting Flask backend on port 5000..."
cd backend
python run.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start Vue.js frontend  
echo "Starting Vue.js frontend on port 5173..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "RJMS is Running!"
echo "=========================================="
echo "✓ Backend API: http://localhost:5000"
echo "✓ Frontend UI: http://localhost:5173"
echo ""
echo "View logs:"
echo "  Backend: tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="

# Keep script running and handle cleanup
trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
