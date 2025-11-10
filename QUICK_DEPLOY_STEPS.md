# 🚀 Quick Deployment Steps for sabrina.study

## Step-by-Step Guide to Deploy SABRINA to Render

### Prerequisites
- ✅ GitHub account
- ✅ Render account (free at https://render.com)
- ✅ Your `sabrina.study` domain on Porkbun

---

## Part 1: Push Code to GitHub

1. **Make sure all files are committed:**
   ```bash
   git add .
   git commit -m "Add deployment files for Render"
   git push origin main
   ```

---

## Part 2: Deploy to Render

### Step 1: Sign up for Render
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account (recommended)

### Step 2: Create New Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub account if not already connected
4. Select the `sabrina` repository
5. Click "Connect"

### Step 3: Configure Service
Fill in the following:

- **Name**: `sabrina` (or any name you like)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### Step 4: Add Environment Variables
Click "Advanced" → "Add Environment Variable"

Add these two:
1. **GEMINI_API_KEY**
   - Key: `GEMINI_API_KEY`
   - Value: `AIzaSyDZPEoBU-gGTjiPrxzdfrCd6fWmson0dw8` (or your API key)

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: Generate a random string (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)

### Step 5: Choose Plan
- Select **Free** plan (for testing)
- Or **Starter** plan ($7/month) for better performance

### Step 6: Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your app will be available at: `https://sabrina.onrender.com` (or your custom name)

---

## Part 3: Connect sabrina.study Domain

### Step 1: Add Custom Domain in Render
1. In Render dashboard, go to your service
2. Click "Settings" tab
3. Scroll down to "Custom Domains"
4. Click "Add Custom Domain"
5. Enter: `sabrina.study`
6. Click "Save"
7. Render will show you DNS instructions

### Step 2: Configure DNS in Porkbun
1. Log into Porkbun
2. Go to your domain: `sabrina.study`
3. Click "DNS" or "DNS Records"

### Step 3: Add DNS Records

**Option A: Use CNAME (Recommended if supported)**
```
Type: CNAME
Host: @ (or leave blank for root domain)
Answer: sabrina.onrender.com
TTL: 600
```

**Option B: Use A Record (If CNAME doesn't work)**
Render will provide you with IP addresses. Add:
```
Type: A
Host: @
Answer: [IP address from Render]
TTL: 600
```

Add multiple A records if Render provides multiple IPs.

**For www subdomain:**
```
Type: CNAME
Host: www
Answer: sabrina.onrender.com
TTL: 600
```

### Step 4: Wait for DNS Propagation
- DNS changes can take 5 minutes to 48 hours
- Usually takes 15-30 minutes
- Check status: https://www.whatsmydns.net

### Step 5: SSL Certificate
- Render automatically provisions SSL certificate
- This can take a few minutes to a few hours
- Check in Render dashboard under "Custom Domains"

---

## Part 4: Test Your Deployment

1. **Test Render URL first:**
   - Visit: `https://sabrina.onrender.com`
   - Make sure everything works

2. **Test your domain:**
   - Visit: `https://sabrina.study`
   - Test all features:
     - Welcome page
     - Planet selection
     - Mission flow
     - AI tutor
     - Activities
     - Sharing

---

## Troubleshooting

### DNS Not Working
- Wait longer (up to 48 hours)
- Double-check DNS records in Porkbun
- Verify records match Render's instructions
- Clear browser cache
- Try different DNS server (8.8.8.8)

### App Not Loading
- Check Render logs (in dashboard)
- Verify environment variables are set correctly
- Check build logs for errors
- Make sure `requirements.txt` includes `gunicorn`

### SSL Certificate Issues
- Wait for automatic provisioning (can take hours)
- Check Render dashboard for SSL status
- Verify DNS is pointing correctly
- Try accessing `http://sabrina.study` (should redirect to HTTPS)

### 502 Bad Gateway
- Check Render logs
- Verify start command is correct
- Check if app is listening on correct port
- Restart the service in Render

---

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Environment variables set
- [ ] Service deployed successfully
- [ ] Custom domain added in Render
- [ ] DNS records configured in Porkbun
- [ ] DNS propagated (checked with whatsmydns.net)
- [ ] SSL certificate provisioned
- [ ] Website accessible at https://sabrina.study
- [ ] All features working correctly

---

## Additional Notes

### Free Tier Limitations (Render)
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Limited to 750 hours/month
- Good for testing and low traffic

### Upgrading (Optional)
- **Starter Plan**: $7/month - Always on, faster response
- **Standard Plan**: $25/month - More resources, better performance

### Monitoring
- Check Render dashboard regularly
- Monitor logs for errors
- Set up alerts if needed

---

## Need Help?

- Render Docs: https://render.com/docs
- Render Support: support@render.com
- Porkbun Support: support@porkbun.com
- Check logs in Render dashboard

---

**Congratulations! Your SABRINA mission simulator is now live at sabrina.study! 🚀🌌**

