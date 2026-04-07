# Backend Ports Configuration

## Two Backend Services

### 1. mismatch_backend.py - PORT 8001
**File:** `mismatch_backend.py`
**Port:** 8001
**Pages:**
- Dashboard (Executive page)
- Mismatch Engine page

**Endpoints:**
```
/executive/kpis
/executive/risk-radar
/executive/photoshoot-performance
/executive/alerts
/executive/ai-photoshoot-stats
/mismatch/kpis
/mismatch/list
```

**To Run:**
```bash
python mismatch_backend.py
```

---

### 2. unified_main.py - PORT 8000
**File:** `unified_main.py`
**Port:** 8000
**Pages:**
- Color Mismatch page
- Image-to-Text page
- AI Photoshoot page
- SQL Agent page

**Endpoints:**
```
/generate-description
/color/detect-color
/color/match-color
/color/detect-and-match
/color/dataset
/image-to-text/*
```

**To Run:**
```bash
python unified_main.py
```

---

## Environment Variables (.env)

```env
# Backend Ports
PORT=8000              # unified_main.py
MISMATCH_PORT=8001     # mismatch_backend.py

# Frontend API URLs
VITE_EXECUTIVE_API_URL=http://localhost:8001    # Dashboard & Mismatch Engine
VITE_MISMATCH_API_URL=http://localhost:8000     # Color Mismatch & others
```

---

## Frontend Configuration (src/lib/api-config.ts)

```typescript
// Dashboard & Mismatch Engine → Port 8001
export const EXECUTIVE_API_URL = "http://localhost:8001";

// Color Mismatch, Image-to-Text, AI Photoshoot → Port 8000
export const COLOR_MISMATCH_API_URL = "http://localhost:8000";
export const IMAGE_TO_TEXT_API_URL = "http://localhost:8000";
export const PHOTOSHOOT_API_URL = "http://localhost:8000";
```

---

## How to Run Everything

### Step 1: Start mismatch_backend.py (Port 8001)
```bash
python mismatch_backend.py
```
**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### Step 2: Start unified_main.py (Port 8000)
```bash
python unified_main.py
```
**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: Start Frontend
```bash
npm run dev
```
**Expected output:**
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

---

## Verification

### Test mismatch_backend.py (Port 8001)
```bash
# Test Executive KPIs
curl http://localhost:8001/executive/kpis

# Test Mismatch KPIs
curl http://localhost:8001/mismatch/kpis
```

### Test unified_main.py (Port 8000)
```bash
# Test root endpoint
curl http://localhost:8000/

# Test color detection
curl http://localhost:8000/color/health
```

---

## Page → Backend Mapping

| Page | Backend | Port | File |
|------|---------|------|------|
| Dashboard | mismatch_backend.py | 8001 | src/pages/Dashboard.tsx |
| Mismatch Engine | mismatch_backend.py | 8001 | src/pages/MismatchEngine.tsx |
| Color Mismatch | unified_main.py | 8000 | src/pages/ColorMismatch.tsx |
| Image-to-Text | unified_main.py | 8000 | src/pages/ImageToText.tsx |
| AI Photoshoot | unified_main.py | 8000 | src/pages/AIPhotoshoot.tsx |
| SQL Agent | unified_main.py | 8000 | src/pages/SQLAgent.tsx |

---

## Troubleshooting

### Port Already in Use
```bash
# Windows (Git Bash)
netstat -ano | findstr :8001
taskkill /PID <PID> /F

netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Backend Not Responding
1. Check if backend is running: `netstat -ano | findstr :8001`
2. Check terminal for error messages
3. Restart the backend
4. Verify .env file has correct ports

### Frontend Shows Wrong Data
1. Restart frontend: `Ctrl+C` then `npm run dev`
2. Hard refresh browser: `Ctrl + Shift + R`
3. Check browser console for API errors
4. Verify both backends are running

---

## Quick Start Script

Create a file `start_all.sh`:
```bash
#!/bin/bash

# Start mismatch backend
python mismatch_backend.py &
MISMATCH_PID=$!

# Start unified backend
python unified_main.py &
UNIFIED_PID=$!

# Wait a bit for backends to start
sleep 3

# Start frontend
npm run dev

# Cleanup on exit
trap "kill $MISMATCH_PID $UNIFIED_PID" EXIT
```

Make it executable:
```bash
chmod +x start_all.sh
./start_all.sh
```
