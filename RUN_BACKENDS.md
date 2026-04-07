# Running Multiple Backends

This project now uses two separate backend services:

## Backend Services

### 1. Mismatch Backend (Port 8001)
**File:** `mismatch_backend.py`
**Port:** 8001
**Used by:**
- Dashboard (Executive KPIs, Risk Radar, Photoshoot Performance)
- Mismatch Engine page

**Endpoints:**
- `/executive/kpis`
- `/executive/risk-radar`
- `/executive/photoshoot-performance`
- `/executive/alerts`
- `/executive/ai-photoshoot-stats`
- `/mismatch/kpis`
- `/mismatch/list`

**To run:**
```bash
python mismatch_backend.py
```

### 2. Unified Backend (Port 8000)
**File:** `unified_main.py`
**Port:** 8000
**Used by:**
- Color Mismatch page (Color detection, matching, image description)
- Image-to-Text page
- AI Photoshoot page

**Endpoints:**
- `/generate-description`
- `/color/detect-color`
- `/color/match-color`
- `/color/detect-and-match`
- `/image-to-text/*`

**To run:**
```bash
python unified_main.py
```

## Running Both Backends

You need to run BOTH backends simultaneously for the full application to work.

### Option 1: Two Terminal Windows

**Terminal 1 - Mismatch Backend:**
```bash
cd ~/Desktop/projects/company/e-commerce-backend
python mismatch_backend.py
```

**Terminal 2 - Unified Backend:**
```bash
cd ~/Desktop/projects/company/e-commerce-backend
python unified_main.py
```

**Terminal 3 - Frontend:**
```bash
cd ~/Desktop/projects/company/e-commerce-backend
npm run dev
```

### Option 2: Using Background Processes (Git Bash)

```bash
# Start mismatch backend in background
python mismatch_backend.py &

# Start unified backend in background
python unified_main.py &

# Start frontend
npm run dev
```

To stop background processes:
```bash
# Find process IDs
ps aux | grep python

# Kill processes
kill <PID>
```

## Verification

After starting both backends, verify they're running:

```bash
# Check mismatch backend (port 8001)
curl http://localhost:8001/executive/kpis

# Check unified backend (port 8000)
curl http://localhost:8000/
```

## Environment Variables

The `.env` file configures which backend each feature uses:

```env
# Executive Dashboard and Mismatch Engine → port 8001
VITE_EXECUTIVE_API_URL=http://localhost:8001

# Color Mismatch and other features → port 8000
VITE_MISMATCH_API_URL=http://localhost:8000

# Backend ports
PORT=8000              # Unified backend
MISMATCH_PORT=8001     # Mismatch backend
```

## Troubleshooting

### Port Already in Use

If you get "Address already in use" error:

**Windows (Git Bash):**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Same for port 8001
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```


