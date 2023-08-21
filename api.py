import httpx
from datetime import datetime, timedelta
import os
# import eda_key

from flask import Flask, jsonify, request

# Replace these with your own values
# page_access_token = eda_key.access_token
page_access_token = os.environ.get("ACCESS_TOKEN")

app = Flask(__name__)

# Dictionary to store rate limit usage
rate_limit_usage = {}

@app.route('/')
def main():
    return "Welcome to the FB GROUP API!"

@app.route('/latest_post/<group_id>')
def latest_post(group_id):
    with httpx.Client() as client:
        client_ip = request.remote_addr
        now = datetime.now()

        # print("rate_limit_usage =", rate_limit_usage)

        if client_ip in rate_limit_usage:
            last_call_time, call_count = rate_limit_usage[client_ip]
            if last_call_time is not None:
                time_since_last_call = now - last_call_time
            else:
                time_since_last_call = timedelta(seconds=0)
        else:
            time_since_last_call = timedelta(seconds=0)
            call_count = 0

        # print("time_since_last_call =", time_since_last_call)
        # print("call_count =", call_count)
        # print("time_since_last_call.total_seconds() =", time_since_last_call.total_seconds())

        # Check if rate limit is reached max call = 3 , time_since_last_call < 100 seconds
        # if true ,then return 429 error code
        if call_count >= 150 and time_since_last_call.total_seconds() < 1800:
            reset_time = last_call_time + timedelta(hours=1)
            # print("reset_time =", reset_time)
            return jsonify({"error": "Rate limit reached. Try again after reset.",
                            "reset_time": reset_time.strftime("%Y-%m-%d %H:%M:%S")}), 429
        
        if time_since_last_call.total_seconds() >= 100:
            rate_limit_usage[client_ip] = (now, 0)

        limit = 1
        fields = "id,message,created_time"
        url = f"https://graph.facebook.com/v17.0/{group_id}/feed?fields={fields}&limit={limit}&access_token={page_access_token}"

        try:
            response = client.get(url)

            if response.status_code == 200:
                rate_limit_usage[client_ip] = (now, call_count + 1)
                
                posts = response.json()["data"]
                for post in posts:
                    created_time_str = post["created_time"]
                    created_time = datetime.strptime(created_time_str, "%Y-%m-%dT%H:%M:%S%z")
                    formatted_time = (created_time + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")

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
