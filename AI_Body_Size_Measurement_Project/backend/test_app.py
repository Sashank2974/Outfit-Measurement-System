"""
Simple test script to verify backend structure
This runs without database dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Simple FastAPI app for testing
app = FastAPI(
    title="AI Body Measurement API - Test",
    description="Test version without database",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Body Measurement System API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Body Measurement API"
    }

@app.get("/api/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "Backend is working correctly!",
        "features": [
            "Gender-specific measurements",
            "AI-powered pose detection",
            "Size recommendations",
            "Measurement history"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting AI Body Measurement API (Test Mode)...")
    print("Server running at: http://localhost:8000")
    print("API Docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
