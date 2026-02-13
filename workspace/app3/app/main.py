# workspace/app3/main.py 
# 
# minimal FastAPI app
#
# What it does
# Provides a simple endpoint you can test quickly:
# GET http://localhost:8000/health
#
# version B.1 - 260212


from fastapi import FastAPI

app = FastAPI(title="app3")

@app.get("/health")
def health():
    return {"app": "app3", "ok": True}
