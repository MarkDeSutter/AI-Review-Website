"""
AI Tool Reviewer - A Yelp-style platform for reviewing AI tools.
Built with Python Bottle + PostgreSQL (Neon) for a databases course final project.
"""

import hashlib
import time
from functools import wraps

import psycopg2
import psycopg2.extras          # gives us RealDictCursor (rows as plain dicts)

from bottle import (
    Bottle, run, template, request, response,
    redirect, static_file, HTTPError
)

app = Bottle()

# ---------------------------------------------------------------------------
# !! PUT YOUR NEON CONNECTION STRING HERE !!
#
# Find it in your Neon dashboard:
#   Project → Connection Details → Connection string
#
# It looks like:
#   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
# ---------------------------------------------------------------------------
DATABASE_URL = "postgresql://neondb_owner:npg_7pWUxzyt2eAY@ep-proud-darkness-appjb0ti-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    """
    Open a new connection to the Neon PostgreSQL database.
    RealDictCursor makes every row behave like a regular Python dict,
    so row["columnName"] works the same way it did with sqlite3.Row.
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def query(sql, params=(), one=False):
    """
    Run a SELECT and return one row (dict) or a list of rows.
    PostgreSQL uses %s placeholders instead of SQLite's ?.
    """
    conn = get_db()
    cur  = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows


def execute(sql, params=()):
    """
    Run an INSERT / UPDATE / DELETE.
    Uses RETURNING to get back the id of an inserted row (PostgreSQL's
    equivalent of sqlite3's lastrowid).
    Returns the first column of the first returned row, or None.
    """
    conn = get_db()
    cur  = conn.cursor()
    cur.execute(sql, params)
    conn.commit()

    result = None
    try:
        row = cur.fetchone()
        if row:
            result = list(row.values())[0]
    except psycopg2.ProgrammingError:
        pass   # No RETURNING clause — that's fine

    conn.close()
    return result


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def get_session_user():
    """Return the logged-in user row (dict), or None."""
    uid = request.get_cookie("uid", secret="SUPER_SECRET_KEY")
    if uid:
        return query('SELECT * FROM users WHERE "user_ID" = %s', (uid,), one=True)
    return None


def login_required(fn):
    """Decorator: redirect to /login if not authenticated."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not get_session_user():
            redirect("/login")
        return fn(*args, **kwargs)
    return wrapper


def next_id(table, id_col):
    """
    Get the next ID for a table by finding the current maximum.
    Keeps the same manual-ID approach as the original schema.
    """
    row = query(f'SELECT MAX("{id_col}") AS m FROM "{table}"', one=True)
    return (row["m"] or 0) + 1


# ---------------------------------------------------------------------------
# Routes - Static files
# ---------------------------------------------------------------------------

@app.route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root="static")


# ---------------------------------------------------------------------------
# Routes - Home / Search
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    user       = get_session_user()
    top_tools  = query('SELECT * FROM ai_tools ORDER BY rating DESC LIMIT 6')
    categories = query('SELECT DISTINCT category FROM ai_tools ORDER BY category')
    return template("index", user=user, top_tools=top_tools, categories=categories)


@app.route("/search")
def search():
    user      = get_session_user()
    q         = request.query.get("q", "").strip()
    category  = request.query.get("category", "").strip()
    sort      = request.query.get("sort", "rating")

    sql        = 'SELECT DISTINCT t.* FROM ai_tools t'
    conditions = []
    params     = []

    if q:
        # ILIKE is PostgreSQL's case-insensitive LIKE (replaces SQLite's LIKE)
        conditions.append('(t."name" ILIKE %s OR t."company" ILIKE %s)')
        params.extend([f"%{q}%", f"%{q}%"])

    if category:
        conditions.append('t."category" = %s')
        params.append(category)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sort_map = {
        "rating": 't."rating" DESC',
        "name":   't."name" ASC',
        "price":  't."price" ASC',
    }
    sql += f' ORDER BY {sort_map.get(sort, "t.\"rating\" DESC")}'

    tools      = query(sql, params)
    categories = query('SELECT DISTINCT category FROM ai_tools ORDER BY category')

    return template("search", user=user, tools=tools, categories=categories,
                    q=q, selected_category=category, sort=sort)


# ---------------------------------------------------------------------------
# Routes - AI Tool Detail
# ---------------------------------------------------------------------------

@app.route("/tool/<aiid:int>")
def tool_detail(aiid):
    user = get_session_user()
    tool = query('SELECT * FROM ai_tools WHERE "ai_ID" = %s', (aiid,), one=True)
    if not tool:
        raise HTTPError(404, "Tool not found")

    reviews = query("""
        SELECT r.*, u."username",
               (SELECT COUNT(*) FROM review_votes rv WHERE rv."review_ID" = r."review_ID" AND rv.vote = 1)  AS upvotes,
               (SELECT COUNT(*) FROM review_votes rv WHERE rv."review_ID" = r."review_ID" AND rv.vote = -1) AS downvotes
        FROM reviews r
        JOIN users u ON r."user_ID" = u."user_ID"
        WHERE r."ai_ID" = %s
          AND r."version" = (
              SELECT MAX(r2."version") FROM reviews r2 WHERE r2."review_ID" = r."review_ID"
          )
        ORDER BY r."date" DESC
    """, (aiid,))

    topical = {}
    for rev in reviews:
        topical[rev["review_ID"]] = query(
            'SELECT "types", "rating" FROM topical_reviews WHERE "review_ID" = %s AND "version" = %s',
            (rev["review_ID"], rev["version"])
        )

    tags = query("""
        SELECT "tag", COUNT(*) AS count
        FROM tags WHERE "ai_ID" = %s
        GROUP BY "tag" ORDER BY count DESC
    """, (aiid,))

    bookmarked  = False
    user_review = None
    if user:
        bm = query('SELECT 1 FROM bookmarks WHERE "ai_ID"=%s AND "user_ID"=%s',
                   (aiid, user["user_ID"]), one=True)
        bookmarked = bm is not None
        user_review = query("""
            SELECT * FROM reviews WHERE "ai_ID"=%s AND "user_ID"=%s
            AND "version" = (
                SELECT MAX("version") FROM reviews WHERE "ai_ID"=%s AND "user_ID"=%s
            )
        """, (aiid, user["user_ID"], aiid, user["user_ID"]), one=True)

    avg_topical = query("""
        SELECT tr."types", ROUND(AVG(tr."rating")::numeric, 1) AS avg_rating
        FROM topical_reviews tr
        JOIN reviews r ON tr."review_ID" = r."review_ID" AND tr."version" = r."version"
        WHERE r."ai_ID" = %s
        GROUP BY tr."types"
    """, (aiid,))

    return template("tool_detail", user=user, tool=tool, reviews=reviews,
                    topical=topical, tags=tags, bookmarked=bookmarked,
                    user_review=user_review, avg_topical=avg_topical)


# ---------------------------------------------------------------------------
# Routes - Review submit / edit
# ---------------------------------------------------------------------------

@app.route("/tool/<aiid:int>/review", method="POST")
@login_required
def submit_review(aiid):
    user = get_session_user()
    tool = query('SELECT * FROM ai_tools WHERE "ai_ID"=%s', (aiid,), one=True)
    if not tool:
        raise HTTPError(404)

    overall = float(request.forms.get("rating", 3))
    text    = request.forms.get("written_review", "").strip()

    topical_types   = ["ease_of_use", "accuracy", "value", "creativity", "support"]
    topical_ratings = {}
    for t in topical_types:
        val = request.forms.get(f"topical_{t}", "")
        if val:
            topical_ratings[t] = float(val)

    now = int(time.time())

    existing = query("""
        SELECT "review_ID", MAX("version") AS max_ver
        FROM reviews WHERE "ai_ID"=%s AND "user_ID"=%s
        GROUP BY "review_ID"
    """, (aiid, user["user_ID"]), one=True)

    if existing:
        rid     = existing["review_ID"]
        new_ver = existing["max_ver"] + 1
    else:
        rid     = next_id("reviews", "review_ID")
        new_ver = 1

    execute("""
        INSERT INTO reviews ("ai_ID","user_ID","review_ID","rating","written_Review","date","version")
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (aiid, user["user_ID"], rid, overall, text, now, new_ver))

    for ttype, trating in topical_ratings.items():
        execute("""
            INSERT INTO topical_reviews ("review_ID","version","types","rating")
            VALUES (%s,%s,%s,%s)
        """, (rid, new_ver, ttype, trating))

    avg = query("""
        SELECT ROUND(AVG(r."rating")::numeric, 1) AS avg FROM reviews r
        WHERE r."ai_ID" = %s
          AND r."version" = (SELECT MAX(r2."version") FROM reviews r2 WHERE r2."review_ID" = r."review_ID")
    """, (aiid,), one=True)
    execute('UPDATE ai_tools SET "rating"=%s WHERE "ai_ID"=%s', (avg["avg"] or 0, aiid))

    redirect(f"/tool/{aiid}")

# ---------------------------------------------------------------------------
# Routes - Review delete
# ---------------------------------------------------------------------------

@app.route("/review/<rid:int>/delete", method="POST")
def delete_review(rid):
    user = get_session_user()

    # get review
    review = query("""
        SELECT * FROM reviews
        WHERE "review_ID"=%s
        LIMIT 1
    """, (rid,), one=True)

    if not review:
        raise HTTPError(404)

    # ownership check
    if review["user_ID"] != user["user_ID"]:
        raise HTTPError(403)

    aiid = review["ai_ID"]

    # delete topical ratings first
    execute("""
        DELETE FROM topical_reviews
        WHERE "review_ID"=%s
    """, (rid,))

    # delete review versions
    execute("""
        DELETE FROM reviews
        WHERE "review_ID"=%s
    """, (rid,))

    # recalculate tool average
    avg = query("""
        SELECT ROUND(AVG(r."rating")::numeric, 1) AS avg
        FROM reviews r
        WHERE r."ai_ID" = %s
          AND r."version" = (
              SELECT MAX(r2."version")
              FROM reviews r2
              WHERE r2."review_ID" = r."review_ID"
          )
    """, (aiid,), one=True)

    execute("""
        UPDATE ai_tools
        SET "rating"=%s
        WHERE "ai_ID"=%s
    """, (avg["avg"] or 0, aiid))

    redirect(f"/tool/{aiid}")


# ---------------------------------------------------------------------------
# Routes - Vote on review
# ---------------------------------------------------------------------------

@app.route("/review/<reviewid:int>/vote", method="POST")
@login_required
def vote_review(reviewid):
    user = dict(get_session_user())
    print(user)
    vote = int(request.forms.get("vote", 1))
    if vote not in (1, -1):
        redirect(request.environ.get("HTTP_REFERER", "/"))

    existing = query('SELECT "vote" FROM review_votes WHERE "user_ID"=%s AND "review_ID"=%s',
                     (user["user_ID"], reviewid), one=True)
    version = query('SELECT MAX(version) FROM reviews WHERE "review_ID" = %s', (reviewid,), one=True)['max']
    print(version)
    
    if existing:
        if existing["vote"] == vote:
            execute('DELETE FROM review_votes WHERE "user_ID"=%s AND "review_ID"=%s',
                    (user["user_ID"], reviewid))
        else:
            execute('UPDATE review_votes SET "vote"=%s WHERE "user_ID"=%s AND "review_ID"=%s',
                    (vote, user["user_ID"], reviewid))
    else:
        execute('INSERT INTO review_votes ("user_ID","review_ID","version","vote") VALUES (%s,%s,%s,%s)',
                (int(user["user_ID"]), reviewid, version, vote,))

    redirect(request.environ.get("HTTP_REFERER", "/"))


# ---------------------------------------------------------------------------
# Routes - Bookmark
# ---------------------------------------------------------------------------

@app.route("/tool/<aiid:int>/bookmark", method="POST")
@login_required
def toggle_bookmark(aiid):
    user = get_session_user()
    existing = query('SELECT 1 FROM bookmarks WHERE "ai_ID"=%s AND "user_ID"=%s',
                     (aiid, user["user_ID"]), one=True)
    if existing:
        execute('DELETE FROM bookmarks WHERE "ai_ID"=%s AND "user_ID"=%s', (aiid, user["user_ID"]))
    else:
        execute('INSERT INTO bookmarks ("ai_ID","user_ID") VALUES (%s,%s)', (aiid, user["user_ID"]))
    redirect(request.environ.get("HTTP_REFERER", f"/tool/{aiid}"))


# ---------------------------------------------------------------------------
# Routes - User profile
# ---------------------------------------------------------------------------

@app.route("/profile/<uid:int>")
def profile(uid):
    current_user = get_session_user()
    profile_user = query('SELECT * FROM users WHERE "user_ID"=%s', (uid,), one=True)
    if not profile_user:
        raise HTTPError(404, "User not found")

    reviews = query("""
        SELECT r.*, t."name" AS tool_name, t."ai_ID"
        FROM reviews r
        JOIN ai_tools t ON r."ai_ID" = t."ai_ID"
        WHERE r."user_ID" = %s
          AND r."version" = (SELECT MAX(r2."version") FROM reviews r2 WHERE r2."review_ID" = r."review_ID")
        ORDER BY r."date" DESC
    """, (uid,))

    bookmarks = query("""
        SELECT t.* FROM ai_tools t
        JOIN bookmarks b ON t."ai_ID" = b."ai_ID"
        WHERE b."user_ID" = %s
        ORDER BY t."name"
    """, (uid,)) if (current_user and current_user["user_ID"] == uid) else []

    return template("profile", current_user=current_user, profile_user=profile_user,
                    reviews=reviews, bookmarks=bookmarks)


# ---------------------------------------------------------------------------
# Routes - Auth
# ---------------------------------------------------------------------------

@app.route("/register", method=["GET", "POST"])
def register():
    if get_session_user():
        redirect("/")

    error = None
    if request.method == "POST":
        username  = request.forms.get("username", "").strip()
        email     = request.forms.get("email", "").strip()
        password  = request.forms.get("password", "").strip()

        if not username or not email or not password:
            error = "All fields are required."
        elif query('SELECT 1 FROM users WHERE "username"=%s', (username,), one=True):
            error = "Username already taken."
        elif query('SELECT 1 FROM users WHERE "email"=%s', (email,), one=True):
            error = "Email already registered."
        else:
            uid = next_id("users", "user_ID")
            execute("""
                INSERT INTO users ("user_ID","username","password","date_Created","email")
                VALUES (%s,%s,%s,%s,%s)
            """, (uid, username, password, int(time.time()), email))
            response.set_cookie("uid", str(uid), secret="SUPER_SECRET_KEY",
                                path="/", max_age=60*60*24*30)
            redirect("/")

    return template("register", error=error)


@app.route("/login", method=["GET", "POST"])
def login():
    if get_session_user():
        redirect("/")

    error = None
    if request.method == "POST":
        username = request.forms.get("username", "").strip()
        password = request.forms.get("password", "").strip()

        user = query('SELECT * FROM users WHERE "username"=%s AND "password"=%s',
                     (username, password), one=True)
        if user:
            response.set_cookie("uid", str(user["user_ID"]), secret="SUPER_SECRET_KEY",
                                path="/", max_age=60*60*24*30)
            redirect("/")
        else:
            error = "Invalid username or password."

    return template("login", error=error)


@app.route("/logout")
def logout():
    response.delete_cookie("uid", path="/")
    redirect("/")


# ---------------------------------------------------------------------------
# Routes - Add tool
# ---------------------------------------------------------------------------

@app.route("/add-tool", method=["GET", "POST"])
@login_required
def add_tool():
    user  = get_session_user()
    error = None
    if request.method == "POST":
        name        = request.forms.get("name", "").strip()
        company     = request.forms.get("company", "").strip()
        category    = request.forms.get("category", "").strip()
        price       = request.forms.get("price", "0").strip()

        if not name or not company or not category:
            error = "Name, company, and category are required."
        else:
            try:
                price = float(price)
            except ValueError:
                price = 0.0
            aiid = next_id("ai_tools", "ai_ID")
            execute("""
                INSERT INTO ai_tools ("ai_ID","name","company","rating","price","category","date")
                VALUES (%s,%s,%s,0,%s,%s,%s)
            """, (aiid, name, company, price, category, int(time.time())))
            redirect(f"/tool/{aiid}")

    categories = ["Chatbot", "Code Assistant", "Image Gen", "Writing Aid",
                  "Search", "Productivity", "Audio", "Video", "Other"]
    return template("add_tool", user=user, error=error, categories=categories)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("✓ Connected to Neon PostgreSQL")
    print("✓ Starting AI Tool Reviewer on http://localhost:8080")
    run(app, host="localhost", port=8080, debug=True, reloader=True)