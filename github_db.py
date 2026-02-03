import requests, base64, json, hashlib, datetime, os

TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "GigantGaming/Jdb"
FILE = "data.json"

URL = f"https://api.github.com/repos/{REPO}/contents/{FILE}"
HEADERS = {"Authorization": f"token {TOKEN}"}


def load_data():
    r = requests.get(URL, headers=HEADERS).json()
    content = base64.b64decode(r["content"]).decode()
    return json.loads(content), r["sha"]


def save_data(data, sha, msg):
    encoded = base64.b64encode(
        json.dumps(data, indent=2).encode()
    ).decode()

    payload = {
        "message": msg,
        "content": encoded,
        "sha": sha
    }
    requests.put(URL, headers=HEADERS, json=payload)


def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()


def register_user(username, email, password):
    data, sha = load_data()

    for u in data["classes"]["Users"]:
        if u["email"] == email:
            return False, "❌ Email already exists"

    new_id = data["meta"].get("Users_last_id", 0) + 1
    data["meta"]["Users_last_id"] = new_id

    user = {
        "id": new_id,
        "username": username,
        "email": email,
        "password": hash_password(password),
        "created_at": str(datetime.date.today())
    }

    data["classes"]["Users"].append(user)
    save_data(data, sha, "User registered")

    return True, "✅ Registration successful"


def login_user(email, password):
    data, _ = load_data()
    pwd = hash_password(password)

    for u in data["classes"]["Users"]:
        if u["email"] == email and u["password"] == pwd:
            return True, u

    return False, None
