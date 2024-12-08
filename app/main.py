from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)

@app.on_event("startup")
async def print_routes():
    for route in app.router.routes:
        if hasattr(route, 'methods'):
            print(f"Path: {route.path} | Methods: {route.methods}")
        else:
            print(f"Path: {route.path}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
