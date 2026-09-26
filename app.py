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

@app.route("/api/get-seasons-by-date", methods=["GET"])
def get_seasons_by_date():
    target_date = request.args.get("date", "").strip()

    if not target_date:
        return jsonify({"message": "Дата не может быть пустой!"}), 400

    if not os.path.exists(FILE_PATH):
        return jsonify({"message": "Файл data.txt ещё не найден."}), 200

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        seasons_found = []
        for line in lines:
            if not line.strip():
                continue
            if target_date in line and "Время года:" in line:
                parts = line.split("Время года:")
                if len(parts) > 1:
                    seasons_found.append(parts[1].strip())

        if not seasons_found:
            return jsonify({"message": f"За дату {target_date} записей не найдено."}), 200

        return jsonify({"message": "\n".join(seasons_found)}), 200

    except IOError as e:
        return jsonify({"message": f"Ошибка при чтении файла: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
