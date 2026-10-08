#!/bin/bash
set -e

mkdir -p /var/log/backend /var/run/fail2ban
touch /var/log/backend/access.log /var/log/fail2ban.log
rm -f /var/run/fail2ban/fail2ban.sock /var/run/fail2ban/fail2ban.pid

# Start FastAPI/Uvicorn on port 5000 in background
uvicorn app.main:app --host 0.0.0.0 --port 5000 &
sleep 2

# Start Fail2ban service
fail2ban-client -x start

echo "[pokemon-backend] FastAPI + Fail2Ban running. Following /var/log/fail2ban.log..."
exec tail -F /var/log/fail2ban.log
