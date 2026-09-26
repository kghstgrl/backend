import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FILE_PATH = "data.txt"


@app.route("/api/send-season", methods=["POST"])
def receive_season():
    data = request.get_json()
    season = data.get("season", "").strip()

    if not season:
        return jsonify({"message": "Ошибка: время года не должно быть пустым!"}), 400

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line_to_save = f"[{current_time}] Время года: {season}\n"

    try:
        with open(FILE_PATH, "a", encoding="utf-8") as f:
            f.write(line_to_save)
        return jsonify({"message": f"Время года '{season}' успешно сохранено!"}), 200
    except IOError as e:
        return jsonify({"message": f"Ошибка при записи файла: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
