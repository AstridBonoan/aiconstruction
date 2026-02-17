#!/bin/bash
# Run demo - backend and frontend (Linux/macOS)
# Access: http://localhost:3000 or http://<this-machine-ip>:3000

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Starting Construction AI Suite Demo..."
echo "Backend: http://0.0.0.0:8000"
echo "Frontend: http://0.0.0.0:3000"
echo ""

cd "$ROOT/backend"
python run.py &
BACKEND_PID=$!
sleep 3

cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo "Demo running. PIDs: $BACKEND_PID $FRONTEND_PID"
echo "From network: http://$(hostname -I | awk '{print $1}'):3000"
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
