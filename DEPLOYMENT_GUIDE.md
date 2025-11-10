# 🚀 SABRINA Deployment Guide

## Overview
This guide will help you deploy SABRINA to `sabrina.study` using Porkbun DNS management and a Flask-compatible hosting service.

## Option 1: Deploy to Render (Recommended - Free Tier Available)

### Step 1: Prepare Your App for Render

1. **Create a `render.yaml` file** (optional, for easier setup):
```yaml
services:
  - type: web
    name: sabrina
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

2. **Create a `Procfile`**:
```
web: gunicorn app:app
```

3. **Update `requirements.txt`** to include `gunicorn`:
```
gunicorn==21.2.0
```

### Step 2: Deploy to Render

1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: sabrina
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or paid for better performance)

5. **Add Environment Variables**:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `SECRET_KEY`: Generate a random secret key

6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Your app will be available at: `https://sabrina.onrender.com`

### Step 3: Configure Porkbun DNS

1. Log into Porkbun
2. Go to your domain: `sabrina.study`
3. Click "DNS" or "DNS Management"
4. Add/Edit DNS records:

**Option A: Use CNAME (Recommended)**
```
Type: CNAME
Name: @ (or leave blank for root domain)
Content: sabrina.onrender.com
TTL: 600
```

**Option B: Use A Record (If CNAME doesn't work for root)**
```
Type: A
Name: @
Content: [Render's IP address - get from Render dashboard]
TTL: 600
```

**For www subdomain:**
```
Type: CNAME
Name: www
Content: sabrina.onrender.com
TTL: 600
```

5. Save the DNS records
6. Wait 5-30 minutes for DNS propagation
7. Your site should be accessible at `https://sabrina.study`

### Step 4: Configure SSL on Render

1. In Render dashboard, go to your service
2. Go to "Settings" → "Custom Domains"
3. Add custom domain: `sabrina.study`
4. Render will automatically provision SSL certificate (can take a few minutes)

---

## Option 2: Deploy to Railway (Alternative - Free Tier Available)

### Step 1: Prepare Your App

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Update `requirements.txt` to include `gunicorn`

### Step 2: Deploy to Railway

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python
5. Add environment variables:
   - `GEMINI_API_KEY`
   - `SECRET_KEY`
6. Railway will auto-deploy
7. Get your Railway URL: `https://sabrina-production.up.railway.app`

### Step 3: Configure Porkbun DNS

1. In Railway, go to your project → Settings → Networking
2. Add custom domain: `sabrina.study`
3. Railway will provide DNS instructions
4. In Porkbun DNS, add the CNAME record Railway provides

---

## Option 3: Deploy to PythonAnywhere (Beginner-Friendly)

### Step 1: Sign up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Sign up for free "Beginner" account
3. Verify email

### Step 2: Upload Your Code

1. Open Bash console in PythonAnywhere
2. Clone your repository:
```bash
git clone https://github.com/noormiz/sabrina.git
cd sabrina
```

3. Install dependencies:
```bash
pip3.10 install --user -r requirements.txt
```

### Step 3: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Select Python 3.10
5. Set path to: `/home/yourusername/sabrina/app.py`
6. Set working directory: `/home/yourusername/sabrina`

### Step 4: Set Environment Variables

1. Go to "Web" → "Environment variables"
2. Add:
   - `GEMINI_API_KEY`: Your API key
   - `SECRET_KEY`: Random secret key

### Step 5: Configure Domain

1. In PythonAnywhere, go to "Web" → "Static files"
2. Add your static files mapping
3. Go to "Web" → "Web app"
4. Add your domain: `sabrina.study`
5. PythonAnywhere will provide DNS instructions
6. Configure Porkbun DNS as instructed

---

## Option 4: Deploy to Fly.io (Good Free Tier)

### Step 1: Install Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Or download from https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Create Fly App

1. Sign up at https://fly.io
2. Login:
```bash
flyctl auth login
```

3. Create app:
```bash
flyctl launch
```

4. Follow prompts and configure

### Step 3: Configure for Flask

Create `fly.toml`:
```toml
app = "sabrina"
primary_region = "iad"

[build]

[env]
  GEMINI_API_KEY = "your-key-here"
  SECRET_KEY = "your-secret-key"

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Step 4: Deploy

```bash
flyctl deploy
```

### Step 5: Add Domain

```bash
flyctl domains add sabrina.study
```

Fly.io will provide DNS instructions. Configure Porkbun DNS accordingly.

---

## Quick Setup: Adding Files for Render (Easiest)

Let me create the necessary files for you to deploy to Render:

### Files to Create:

1. **Procfile** - Tells Render how to run your app
2. **runtime.txt** - Specifies Python version (optional)
3. **Update requirements.txt** - Add gunicorn

---

## DNS Configuration in Porkbun

### General Steps:

1. Log into Porkbun account
2. Find your domain `sabrina.study`
3. Click on "DNS" or "DNS Records"
4. You'll see existing records (usually A records pointing to Porkbun's servers)

### For Render/Railway/Fly.io:

**Add CNAME Record:**
```
Type: CNAME
Host: @ (or leave blank for root domain)
Answer: your-app-url.onrender.com (or railway.app, fly.dev, etc.)
TTL: 600 (or 3600)
```

**If CNAME doesn't work for root domain, use A record:**
```
Type: A
Host: @
Answer: [IP address from hosting provider]
TTL: 600
```

**Add www subdomain:**
```
Type: CNAME
Host: www
Answer: your-app-url.onrender.com
TTL: 600
```

### DNS Propagation:

- DNS changes can take 5 minutes to 48 hours
- Usually takes 15-30 minutes
- Check propagation: https://www.whatsmydns.net

---

## Testing Your Deployment

1. **Test the hosting service URL first** (e.g., `sabrina.onrender.com`)
2. **Then test your custom domain** (`sabrina.study`)
3. **Check SSL certificate** (should be automatic with most services)
4. **Test all features**: mission flow, AI tutor, activities

---

## Troubleshooting

### DNS Not Working:
- Wait longer (up to 48 hours)
- Check DNS records are correct
- Clear browser cache
- Try different DNS server (8.8.8.8)

### App Not Loading:
- Check hosting service logs
- Verify environment variables are set
- Check start command is correct
- Verify requirements.txt is correct

### SSL Certificate Issues:
- Wait for automatic provisioning (can take hours)
- Check hosting service SSL settings
- Verify DNS is pointing correctly

---

## Recommended: Render Setup

Render is the easiest and most beginner-friendly option with a good free tier. Let me create the necessary files for you!

