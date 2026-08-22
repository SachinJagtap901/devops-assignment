from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
@app.route("/horoscope")
def home():
    return {
        "application": "Vedic Horoscope API",
        "status": "running"
    }


@app.route("/health")
@app.route("/horoscope/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/horoscope", methods=["POST"])
def horoscope():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    date_of_birth = data.get("date_of_birth")
    time_of_birth = data.get("time_of_birth")
    place_of_birth = data.get("place_of_birth")

    if not all([name, date_of_birth, time_of_birth, place_of_birth]):
        return jsonify({
            "error": "name, date_of_birth, time_of_birth and place_of_birth are required"
        }), 400

    # Placeholder interpretation for the first version.
    # Accurate Vedic calculations will be added separately.
    return jsonify({
        "name": name,
        "birth_details": {
            "date": date_of_birth,
            "time": time_of_birth,
            "place": place_of_birth
        },
        "horoscope": {
            "personality": "You are encouraged to develop your natural strengths and maintain consistency.",
            "career": "Focus on disciplined growth and long-term professional goals.",
            "relationships": "Clear communication and patience can strengthen relationships.",
            "general": "Use this reading as entertainment and general reflection rather than a deterministic prediction."
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)