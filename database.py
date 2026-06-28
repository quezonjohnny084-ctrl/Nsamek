import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    referrals INTEGER DEFAULT 0,
    referred_by INTEGER DEFAULT NULL,
    last_claim REAL DEFAULT 0
)
""")
conn.commit()


def add_user(uid, username):
    c.execute("""
        INSERT OR IGNORE INTO users (user_id, username, referrals, referred_by, last_claim)
        VALUES (?, ?, 0, NULL, 0)
    """, (uid, username))
    conn.commit()


def get(uid):
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    return c.fetchone()


def set_referral(new_user, ref_user):
    if new_user == ref_user:
        return None

    c.execute("SELECT referred_by FROM users WHERE user_id=?", (new_user,))
    row = c.fetchone()

    if row and row[0] is None:
        c.execute("""
            UPDATE users
            SET referred_by=?, referrals = referrals + 1
            WHERE user_id=?
        """, (ref_user, ref_user))
        conn.commit()
        return ref_user

    return None


def update_time(uid, t):
    c.execute("UPDATE users SET last_claim=? WHERE user_id=?", (t, uid))
    conn.commit()


def top():
    c.execute("""
        SELECT username, referrals
        FROM users
        ORDER BY referrals DESC
        LIMIT 10
    """)
    return c.fetchall()