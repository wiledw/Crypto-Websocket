# Crypto-Websocket

Here you can clone and do the following:
recreate the virtual environment using requirements.txt:

python3 -m venv venv
source venv/bin/activate  # On Linux/macOS

or

venv\Scripts\activate  # On Windows

pip install -r requirements.txt

// Run the server
py server.py

or

py server2.py

2 Approaches:
Server.py:
Per-Client API Fetch (First Approach)

Each client that connects to the WebSocket initiates its own API call to fetch market data. Every client fetches the data independently, and each has its own separate loop to request and send data back to the frontend.

Pros:
Simple to implement due to each WebSocket connection works independently. You don’t have to maintain a shared state or worry about synchronizing data between clients.
Isolated operations for each client,where a failure in a client does not affect other clients.

Cons:
Increase Load on API, every connected client makes separate API calls
Leads to redundant fetching


Server2.py:
Shared API Fetch (Optimization Better approach)

When a client subscribes, their connection is stored in an array. The backend fetches crypto prices in a single API call, then broadcasts the data to all connected WebSocket clients. Uses redis to fetch last updated data from the last api call for new connected clients that connect before or after the fetching and sending all websocket instances happens.

Pros:
Efficient API usage, only single API call is made for all clients
Consistent Data Across Clients
Easier to scale to a large number of clients since the number of API calls doesn’t increase with each new client.
Better resource management: less cpu and memory usage overall
Fast in memory cache using redis to fetch latest data, all websocket can pull data from redis, ensuring synchronization and fast access.

Why I decided to use this new approach after submission:
Single API call for all clients listening to the websocket, more efficient overall
Using redis to fetch last cached updated data, faster retrieval
Scalability of WebSocket Connections: Horizontal scaling using multiple WebSocket server instances helps distribute load and manage more clients without overburdening a single server. This improves reliability during high traffic scenarios.

# Implement kubernetes, kafka, docker containers with the websocket flow:
Fetch Data: Only one of the WebSocket server instances (containers) calls the external API to fetch market data.

Publish Data: This server (container) publishes the data to a kafka topic (e.g., market_updates).

Other Servers Listen: All other server instances (running in their own containers) that are subscribed to the "market_updates" topic, receive this message.

Broadcast to Clients: Each of these instances then broadcasts the market data to their respective connected clients. The broadcast to clients is through websocket between client frontend and backend server 

Kubernetes can dynamically manage the scaling of WebSocket server instances based on the load, automatically adjusting the number of running containers to handle varying traffic throughout the day.

Difference on using Kafka topics and Redis pub/sub in this scenario:

Kafka Topics:
Pros:
  High Scalability: can handle massive volumes of messages
  Message Persistence: If a WebSocket server instance is down, the data is still available, and missed messages can be replayed when the instance comes back up.
Cons:
  Higher latency: since its in disk, its slower compared to redis
  Higher storage: Kafka is resource-intensive and might cost more to run, especially for smaller projects that don’t need Kafka’s level of scalability.

Redis Pub/sub: 
Pros:
  Lower latency: since its in memory, faster compared to kafka
  Lightweight: Redis consumes fewer resources than Kafka, making it a cost-effective solution for small to medium-scale applications.
Cons:
  Limited Scalability: can’t handle massive volumes of messages
  No Message Persistence: If a WebSocket server instance is down, it misses the message since it only travels through memory once.


You need to clone the frontend dashboard to display the crypto data from the server:
https://github.com/wiledw/Crypto-Dashboard