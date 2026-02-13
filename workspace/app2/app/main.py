# workspace/app2/main.py 
# 
# minimal FastAPI app
#
# What it does
# Provides a simple endpoint you can test quickly:
# GET http://localhost:8000/health
#
# version B.1 - 260212


from fastapi import FastAPI

app = FastAPI(title="app2")

@app.get("/health")
def health():
    return {"app": "app2", "ok": True}
