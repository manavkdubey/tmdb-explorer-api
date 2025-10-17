import requests
import time
import json
import sys

def notify_evaluator(evaluation_url, payload_data, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                evaluation_url,
                json=payload_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            if response.status_code == 200:
                print(f"✅ Evaluation notification sent successfully")
                return True
            else:
                print(f"❌ Evaluation failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
        if attempt < max_retries - 1:
            delay = 2 ** attempt
            print(f"⏳ Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"❌ Failed to send evaluation after {max_retries} attempts")
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python notify.py <evaluation_url> <payload.json>")
        sys.exit(1)
    evaluation_url = sys.argv[1]
    payload_file = sys.argv[2]
    try:
        with open(payload_file, 'r') as f:
            payload = json.load(f)
        print(f"📤 Sending evaluation notification to: {evaluation_url}")
        print(f"📋 Payload: {json.dumps(payload, indent=2)}")
        success = notify_evaluator(evaluation_url, payload)
        sys.exit(0 if success else 1)
    except FileNotFoundError:
        print(f"❌ Payload file not found: {payload_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in payload file: {payload_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
