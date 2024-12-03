from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/neovero-receiver', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)