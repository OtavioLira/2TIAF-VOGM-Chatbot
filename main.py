from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return "OK", 200


@app.route("/dialogflow", methods=["POST"])
def dialogflow():
    data = request.get_json()
    print(data)

    return jsonify(
        {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": ["This is a sample response from webhook"],
                            "redactedText": ["This is a sample response from webhook"]
                        },
                        "responseType": "HANDLER_PROMPT",
                        "source": "VIRTUAL_AGENT"
                    }
                ]
            }
        }
    )


if __name__ == "__main__":

    app.run(debug=True)
