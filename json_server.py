from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    # JSONデータを取得
    try:
        data = request.get_json()  # ここでJSONを取得
        if not data:
            return "Invalid JSON", 400

        print(f"Received JSON data: {data}")

        # JSONファイルに書き出し
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        return jsonify({"message": "Data received!"})

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="160.16.151.12", port=5000)
