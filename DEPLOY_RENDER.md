# Parenting Capacity Assessor — Cloud Deployment Guide

## Deploy on Render

### Prerequisites
- GitHub account (repo already connected)
- OpenAI API key (get at https://platform.openai.com/api-keys)

### Step-by-Step Deployment

#### 1. Go to Render Dashboard
- Visit https://dashboard.render.com
- Sign up or log in with GitHub

#### 2. Create New Web Service
- Click **"New +"** → select **"Web Service"**
- Connect your GitHub account if prompted
- Search for and select `parenting-capacity-assessor` repo
- Click **"Connect"**

#### 3. Configure Deployment
Fill in the form:
- **Name:** `parenting-capacity-assessor` (or your choice)
- **Environment:** `Python 3.11`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- **Instance Type:** `Standard` (free tier available)

#### 4. Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `LLM_PROVIDER` | `openai` |
| `OPENAI_API_KEY` | Your OpenAI API key from https://platform.openai.com/api-keys |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `DATA_DIR` | `/app/data` |
| `KNOWLEDGE_DIR` | `/app/data/knowledge` |
| `REPORTS_DIR` | `/app/data/reports` |
| `SKILL_DOC_DIR` | `/app/data/skill_doc` |
| `UPLOADS_DIR` | `/app/uploads` |

#### 5. Add Persistent Disk (for uploads & reports)
Under **"Disks"** → **"Add Disk"**:
- **Name:** `data`
- **Mount Path:** `/app/data`
- **Size:** `1 GB` (minimum)

Add second disk:
- **Name:** `uploads`
- **Mount Path:** `/app/uploads`
- **Size:** `1 GB`

#### 6. Deploy
- Click **"Create Web Service"**
- Render will build and deploy automatically
- Wait for status to show **"Live"** (5-10 minutes)
- Your URL will be: `https://<service-name>.onrender.com`

### Post-Deployment Checklist

✅ **App loads**
- Visit your Render URL
- Should see Streamlit sidebar with "⚖️ Parenting Capacity Assessor"

✅ **LLM connected**
- Check the sidebar status indicator
- Should show green "✓ Connected — gpt-4o-mini"

✅ **File uploads work**
- Upload a test PDF or TXT file
- Should process and show in "Indexed" list

✅ **Report generation**
- Complete intake tab
- Go to "Generate Report" tab
- Click "🚀 Generate full report"
- Should draft all 11 sections

### Troubleshooting

**"✗ Not connected" error in sidebar**
- Check that `OPENAI_API_KEY` is set correctly in Environment Variables
- Verify key has API credits: https://platform.openai.com/account/billing/overview

**App crashes on startup**
- Check Render logs: click service → "Logs"
- Common issue: missing env vars
- Re-verify all 8 env vars are set

**File uploads fail**
- Verify disk is mounted at `/app/uploads`
- Check disk has available space

**App is very slow**
- gpt-4o-mini is slower than larger models
- First run downloads embedding model (5+ min) — wait for "Live" status
- Chat/report generation takes 30-60 seconds per section

### Local Testing (before deploying)

```bash
# Test with OpenAI locally first
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-4o-mini

streamlit run app.py
```

### Scaling Up

If you need:
- **Faster responses:** upgrade to `gpt-4o` or `gpt-4-turbo`
- **More storage:** increase disk size in Render dashboard
- **Better performance:** upgrade Instance Type from Standard to Pro

### Keep Local Ollama Option

To run locally with Ollama instead:

```bash
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b

ollama serve  # in another terminal
streamlit run app.py
```

---

**Live URL after deploy:** `https://<your-service-name>.onrender.com`

Questions? Check Render docs: https://render.com/docs
