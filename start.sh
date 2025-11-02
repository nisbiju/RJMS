#!/bin/bash

echo "Starting RJMS Application..."
echo "=============================="

# Start Flask backend in background
echo "Starting Flask backend on port 5000..."
cd backend
python run.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Vue.js frontend in background
echo "Starting Vue.js frontend on port 5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=============================="
echo "RJMS is now running!"
echo "=============================="
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
