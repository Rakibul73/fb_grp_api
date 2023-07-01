import httpx
from datetime import datetime, timedelta
import os

from flask import Flask, jsonify

# Replace these with your own values
# page_access_token = eda_key.access_token
page_access_token = os.environ.get("ACCESS_TOKEN")

app = Flask(__name__)

@app.route('/')
def main():
    return "Welcome to the FB GROUP API!"

@app.route('/latest_post/<group_id>')
def latest_post(group_id):
    with httpx.Client() as client:
        # Add a limit parameter to the URL and request specific fields
        limit = 1  # Set the number of posts per request
        fields = "id,message,created_time"
        url = f"https://graph.facebook.com/v17.0/{group_id}/feed?fields={fields}&limit={limit}&access_token={page_access_token}"

        try:
            response = client.get(url)

            if response.status_code == 200:
                posts = response.json()["data"]
                for post in posts:
                    created_time_str = post["created_time"]
                    created_time = datetime.strptime(created_time_str, "%Y-%m-%dT%H:%M:%S%z")
                    formatted_time = (created_time + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")

                    # Format post data and return as JSON
                    post_data = {
                        "message": post["message"],
                        "timestamp": formatted_time,
                        "post_id": post["id"],
                    }
                    return jsonify(post_data)
            else:
                print("Error:", response.status_code, response.text)
                print("URL:", url)
                print("Response:", response)
                return jsonify({"error": "Failed to fetch posts",
                                "response_status_code": response.status_code,
                                "response_text": response.text})
        except Exception as e:
            print("Exception:", e)
            print("URL:", url)
            return jsonify({"error": "An exception occurred",
                            "exception": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
