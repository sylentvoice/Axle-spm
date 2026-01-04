from instagrapi import Client
import time
import random
import os
import threading

# ============================
# 🔹 Instagram Client Setup
# ============================
cl = Client()

SESSIONID = os.getenv("IG_SESSIONID")
if not SESSIONID:
    raise Exception("❌ IG_SESSIONID not set")

cl.login_by_sessionid(SESSIONID)

me_id = cl.user_id
print(f"🤖 Logged in as @{cl.username}")

# ============================
# 🔹 Reply templates
# ============================
reply_templates_master = [
    """ARJUN TRY M4AA R4xNDY🤎___/




ARJUN TRY M4AA R4xNDY💛___/




ARJUN TRY M4AA R4xNDY💚___/




ARJUN TRY M4AA R4xNDY❤️‍🩹___/




ARJUN TRY M4AA R4xNDY❤️___/




ARJUN TRY M4AA R4xNDY💙___/




ARJUN TRY M4AA R4xNDY💜___/"""
]

last_msg_id_by_user = {}
user_reply_history = {}

def get_next_reply(history):
    possible = [r for r in reply_templates_master if r not in history]
    if not possible:
        history.clear()
        possible = reply_templates_master.copy()
    reply = random.choice(possible)
    history.add(reply)
    return reply

# ============================
# 🔹 Auto-reply loop
# ============================
def auto_reply():
    while True:
        try:
            threads = cl.direct_threads(amount=5)

            for thread in threads:
                if not thread.messages:
                    continue

                msg = thread.messages[0]

                # Skip own messages
                if msg.user_id == me_id:
                    continue

                user_id = msg.user_id
                username = thread.users[0].username

                if last_msg_id_by_user.get(user_id) == msg.id:
                    continue

                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                reply = get_next_reply(user_reply_history[user_id])
                cl.direct_answer(thread.id, reply)

                print(f"✔️ Replied to @{username}")
                last_msg_id_by_user[user_id] = msg.id

                time.sleep(15)

            time.sleep(15)

        except Exception as e:
            print("🚨 Error:", e)
            time.sleep(30)

# ============================
# Start bot safely (NON-BLOCKING)
# ============================
bot_thread = threading.Thread(target=auto_reply, daemon=True)
bot_thread.start()

# Keep the script alive
while True:
    time.sleep(20)
