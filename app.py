import sys

try:
    from flask import (
        Flask,
        request,
        jsonify,
        render_template,
        Response,
        stream_with_context
    )

    from services.gemini_service import get_ai_response_stream

except ValueError as e:
    print(f"[STARTUP ERROR] {e}")
    sys.exit(1)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        message = data.get("message", "")

        if not message or not message.strip():
            return jsonify({
                "error": "message is required and cannot be empty"
            }), 400

        print(f"[USER MESSAGE] {message}")

        def generate():
            for chunk in get_ai_response_stream(message):
                print(chunk, end="", flush=True)
                yield chunk

            print()

        return Response(
            stream_with_context(generate()),
            mimetype="text/plain"
        )

    except Exception as e:

        print(
            f"[CHAT ERROR] {type(e).__name__}: {e}"
        )

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)