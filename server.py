import asyncio
import json
import websockets
from websockets.server import serve
from market_data import get_market_data, format_market_data
from config import assets

async def market_websocket_handler(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            # print(f"Received message: {data}")  # Log the received message
            
            # Handle subscription message
            if data.get("event") == "subscribe" and data.get("channel") == "rates":
                print("Client subscribed to rates channel.")
                
                # Loop to send market data periodically
                while True:
                    market_data = get_market_data(assets)
                    # print("this is marketData", market_data)

                    for asset, asset_data in market_data.items():
                        response = {
                            "channel": "rates",
                            "event": "data",
                            "data": format_market_data(asset, asset_data)
                        }
                        await websocket.send(json.dumps(response))
                        # print(f"Sent response: {response}")  # Log the sent response
                    
                    await asyncio.sleep(60)
    except websockets.ConnectionClosed:
        print("Client disconnected.")
    except Exception as e:
        print(f"Error handling WebSocket connection: {e}")

# Start the WebSocket server
async def start_server():
    # The serve function in start_server accepts new WebSocket connections.
    # After the connection is established, control is handed over to market_websocket_handler
    async with serve(market_websocket_handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765/markets/ws")
        
        # Only happen once when the WebSocket server starts running.
        await asyncio.Future()  # Run forever

# Run the server
if __name__ == "__main__":
    asyncio.run(start_server())



