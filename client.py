import websocket
import json

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket connection closed.")

def on_open(ws):
    print("WebSocket connection opened.")
    subscribe_message = json.dumps({
        "event": "subscribe",
        "channel": "rates"
    })
    ws.send(subscribe_message)

# Run the WebSocket client
if __name__ == "__main__":
    websocket_url = "ws://localhost:8765/markets/ws"  # URL of your server
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.on_open = on_open
    ws.run_forever()
