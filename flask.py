import asyncio
from flask import Flask, request, jsonify
from nats.aio.client import Client as NATS
import json

app = Flask(__name__)

async def send_request_to_nats(message):
    nc = NATS()
    await nc.connect(servers=["nats://127.0.0.1:4222"])
    await nc.publish("requete", json.dumps(message).encode())
    await nc.close()

@app.route('/api/send-request', methods=['POST'])
async def handle_send_request():
    data = request.json
    message = data.get('message')
    if message:
        await send_request_to_nats({'message': message})
        return jsonify({'status': 'success', 'message': 'Message sent to NATS topic'})
    else:
        return jsonify({'status': 'error', 'message': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
