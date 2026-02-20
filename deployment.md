# Azure VM Deployment Guide

## Prerequisites
- Azure VM with Ubuntu 20.04/22.04 or similar Linux distribution
- SSH access to your VM
- Python 3.9+ installed

## Step 1: Prepare Your VM

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv

# Install nginx (optional, for reverse proxy)
sudo apt install -y nginx
```

## Step 2: Transfer Project to VM

```bash
# On your local machine, from project directory:
scp -r . azureuser@YOUR_VM_IP:~/simple-api/

# Or use git:
# ssh azureuser@YOUR_VM_IP
# git clone YOUR_REPO_URL ~/simple-api
```

## Step 3: Setup Application

```bash
# SSH into your VM
ssh azureuser@YOUR_VM_IP

# Navigate to project
cd ~/simple-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
nano .env  # Edit as needed
```

## Step 4: Test the Application

```bash
# Run temporarily
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test from another terminal
curl http://localhost:8000/health
```

## Step 5: Setup Systemd Service (Production)

Create service file:

```bash
sudo nano /etc/systemd/system/simple-api.service
```

Add this content (adjust paths for your username):

```ini
[Unit]
Description=Simple FastAPI Application
After=network.target

[Service]
Type=notify
User=azureuser
Group=azureuser
WorkingDirectory=/home/azureuser/simple-api
Environment="PATH=/home/azureuser/simple-api/venv/bin"
ExecStart=/home/azureuser/simple-api/venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable simple-api
sudo systemctl start simple-api
sudo systemctl status simple-api

# View logs
sudo journalctl -u simple-api -f
```

## Step 6: Configure Firewall

```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Or if using nginx on port 80/443:
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable
sudo ufw status
```

## Step 7: Configure Azure Network Security Group

In Azure Portal:
1. Go to your VM → Networking → Network settings
2. Add inbound port rule:
   - **Destination port ranges**: 8000 (or 80, 443)
   - **Protocol**: TCP
   - **Action**: Allow
   - **Priority**: 1000
   - **Name**: Allow-API

## Step 8: Access Your API

Your API is now accessible at:
- `http://YOUR_VM_PUBLIC_IP:8000`
- `http://YOUR_VM_PUBLIC_IP:8000/docs` (Swagger UI)
- `http://YOUR_VM_PUBLIC_IP:8000/health`

## Optional: Setup Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/simple-api
```

Add:

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/simple-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Optional: Setup HTTPS with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Troubleshooting

```bash
# Check if service is running
sudo systemctl status simple-api

# View recent logs
sudo journalctl -u simple-api -n 50

# Check if port is listening
sudo netstat -tlnp | grep 8000

# Test locally
curl http://localhost:8000/health
```