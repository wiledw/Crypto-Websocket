import asyncio
import json
import websockets
from websockets.server import serve
from market_data import get_market_data, format_market_data
from config import assets
import redis.asyncio as redis

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to get cached market data from Redis
async def get_cached_market_data():
    data = await redis_client.get("market_data")
    if data:
        return json.loads(data)  # Convert the JSON string back to a Python object
    return None

# Function to set cached market data to Redis
async def set_cached_market_data(data):
    await redis_client.set("market_data", json.dumps(data))  # Store as JSON string

# List to store active WebSocket connections
active_connections = []

async def market_websocket_handler(websocket):
    try:
        # Add new WebSocket connection to the list
        active_connections.append(websocket)
        print("New client connected.")

        async for message in websocket:
            data = json.loads(message)
            # Handle subscription message
            if data.get("event") == "subscribe" and data.get("channel") == "rates":
                print("Client subscribed to rates channel.")
            
                # Immediately send cached data to the new client
                cached_data = await get_cached_market_data()
                for asset, asset_data in cached_data.items():
                    response = {
                        "channel": "rates",
                        "event": "data",
                        "data": format_market_data(asset, asset_data)
                    }
                    await websocket.send(json.dumps(response))


    except websockets.ConnectionClosed:
        print("Client disconnected.")
    except Exception as e:
        print(f"Error handling WebSocket connection: {e}")
    finally:
        # Remove WebSocket from active connections if disconnected
        if websocket in active_connections:
            active_connections.remove(websocket)

# Function to fetch market data and broadcast to all connected clients
async def broadcast_market_data():
    while True:
        try:
            # Fetch the market data once for all clients
            market_data = get_market_data(assets)
            
            # Handle empty market_data response (possible api is currently unavailable)
            # Users still use the old data fetch or redis data (both are the same data)
            if not market_data:
                print("Market data is empty. Retrying after 60 seconds.")
                await asyncio.sleep(60)  # Wait before retrying
                continue 

            print(active_connections)
            await set_cached_market_data(market_data)  # Update the cache
            print("Broadcasting new market data to clients.")
            # Loop through all active WebSocket connections
            for websocket in active_connections:
                try:
                    # Send the market data to each client
                    for asset, asset_data in market_data.items():
                        response = {
                            "channel": "rates",
                            "event": "data",
                            "data": format_market_data(asset, asset_data)
                        }
                        await websocket.send(json.dumps(response))
                except websockets.ConnectionClosed:
                    # Handle disconnected client
                    print("A client has disconnected.")
                    active_connections.remove(websocket)
                except Exception as e:
                    print(f"Error sending data to client: {e}")

        except Exception as e:
            print(f"Error fetching market data: {e}")

        # Wait 60 seconds before fetching again
        await asyncio.sleep(60)

# Start the WebSocket server
async def start_server():
    # The serve function in start_server accepts new WebSocket connections.
    # After the connection is established, control is handed over to market_websocket_handler
    async with serve(market_websocket_handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765/markets/ws")

        # Run both the WebSocket server and the market data broadcaster concurrently
        # Only happen once when the WebSocket server starts running.
        await asyncio.gather(
            asyncio.Future(),  # Keep server running
            broadcast_market_data()  # Broadcast market data to all clients
        )

# Run the server
if __name__ == "__main__":
    asyncio.run(start_server())
