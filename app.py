import os 
import json 
import base64
import uvicorn
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import urllib.parse

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/ws2", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})
@app.get("/fetching", response_class=HTMLResponse)
async def get_fetching(request: Request):
    return templates.TemplateResponse("index3.html", {"request": request})
@app.get("/ws3", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index4.html", {"request": request})
@app.get("/motion_control/{encoded_data}", response_class=HTMLResponse)
async def motion_control(request: Request, encoded_data: str):
    # Decode from URL encoding (%3D -> =, etc)
    encoded_data_clean = urllib.parse.unquote(encoded_data)

    return templates.TemplateResponse("motion_planning_urdf.html", {
        "request": request,
        "shots_data": encoded_data_clean,
        "model_files":"BD3.URDF"
    })
@app.post("/IoT_connect")
async def IoT_control_motion(request: Request):
      reqiot = await request.json()
      print("Request IoT data: ",reqiot)
      #Store the current position of the robot for getting request of the potion of motion 
      return reqiot


'''
@app.get("/motion_control/{encoded_data}", response_class=HTMLResponse)
async def motion_control(request: Request, encoded_data: str):
    try:
        # Decode Base64 to bytes
        decoded_bytes = base64.b64decode(encoded_data)
        # Convert bytes to string
        json_str = decoded_bytes.decode('utf-8')
        # Parse JSON
        data = json.loads(json_str)
    except Exception as e:
        return HTMLResponse(f"<h1>Error decoding: {str(e)}</h1>", status_code=400)

    return templates.TemplateResponse("motion_planning_urdf.html",{
        "request": request,
        "email_data": encoded_data
    })
'''
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # 1. Receive incoming JSON payload
            data = await websocket.receive_text()
            payload = json.loads(data)
            print("Received payload:", payload)

            # 2. Build a feedback response (you can customize this)
            feedback = {
                "status": "ok",
                "received_keys": list(payload.keys()),
                "timestamp": __import__("time").time()
            }

            # 3. Send it back over the WebSocket
            await websocket.send_text(json.dumps(feedback))

        except Exception as e:
            print("WebSocket error:", e)
            break
@app.websocket("/ws2")
async def websocket_endpoint2(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Respond as fast as possible
            feedback = {
                "status": "ok",
                "timestamp": time.time(),
                "keys": list(payload.keys())
            }

            # Send response immediately
            await websocket.send_text(json.dumps(feedback))

    except Exception as e:
        print("WebSocket closed or errored:", e)
        await websocket.close()
#End-point fetching test function 
@app.post("/post_back_end")
async def fetching_back_end(request: Request):
        reqdat = await request.json()
        print("reqdat: ",reqdat)
        return reqdat 
@app.websocket("/optimize")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Process your data here
            print("Received:", payload)

            # Send a response
            await websocket.send_text(json.dumps({
                "status": "ok",
                "message": "Data received successfully"
            }))

            # Explicitly free memory (optional but helps in long sessions)
            del payload
            del data
    except Exception as e:
        print("WebSocket error:", e)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

