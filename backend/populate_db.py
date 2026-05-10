import random
import time

from app import app
from extensions import db
from models import Users, Reviews, Review_Votes, AI_Tools, Topical_Reviews, Tags, Bookmarks

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

now = int(time.time())

with app.app_context():

    # --- Clear existing data (children before parents) ---
    Topical_Reviews.query.delete()
    Review_Votes.query.delete()
    Tags.query.delete()
    Bookmarks.query.delete()
    Reviews.query.delete()
    AI_Tools.query.delete()
    Users.query.delete()
    db.session.commit()

    # --- Users ---
    users_data = [
        (1, 'techreviewer',  'pass1', 'tech@mail.com'),
        (2, 'aiexplorer',    'pass2', 'ai@mail.com'),
        (3, 'codewizard',    'pass3', 'code@mail.com'),
        (4, 'mlgeek',        'pass4', 'ml@mail.com'),
        (5, 'devninja',      'pass5', 'dev@mail.com'),
        (6, 'promptmaster',  'pass6', 'prompt@mail.com'),
    ]
    for uid, username, password, email in users_data:
        db.session.add(Users(user_ID=uid, username=username, password=password,
                             date_Created=now - random.randint(100000, 10000000), email=email))
    db.session.commit()

    # --- AI Tools ---
    tools_data = [
        (1, 'ChatGPT',        'OpenAI',      4.5, 20.0, 'Language Model'),
        (2, 'Claude',         'Anthropic',   4.7, 20.0, 'Language Model'),
        (3, 'Gemini',         'Google',      4.2,  0.0, 'Language Model'),
        (4, 'GitHub Copilot', 'Microsoft',   4.3, 10.0, 'Code Assistant'),
        (5, 'Midjourney',     'Midjourney',  4.6, 10.0, 'Image Generation'),
    ]
    for aid, name, company, rating, price, category in tools_data:
        db.session.add(AI_Tools(ai_ID=aid, name=name, company=company, rating=rating,
                                price=price, category=category,
                                date=now - random.randint(1000000, 50000000)))
    db.session.commit()

    # --- Reviews ---
    # Each review_ID is one review thread — version tracks edits
    reviews_data = [
        (1, 1, 1, 1, 4.5, 'ChatGPT is great for coding help!'),
        (1, 2, 1, 1, 4.7, 'Updated: even better with new features.'),
        (2, 1, 1, 2, 3.8, 'Decent but sometimes hallucinates.'),
        (2, 2, 1, 2, 4.0, 'Improved with recent updates.'),
        (3, 1, 2, 3, 5.0, 'Claude is the most thoughtful AI I have used.'),
        (3, 2, 2, 3, 4.9, 'Still excellent, minor quirks.'),
        (4, 1, 2, 4, 4.6, 'Great for long documents and summarization.'),
        (4, 2, 2, 4, 4.8, 'Context handling is top notch.'),
        (5, 1, 3, 5, 4.0, 'Gemini is solid for everyday tasks.'),
        (5, 2, 3, 5, 4.2, 'Google integration is a nice bonus.'),
        (6, 1, 4, 1, 4.4, 'Copilot saves me hours every week.'),
        (6, 2, 4, 1, 4.5, 'Still the best code assistant out there.'),
        (7, 1, 5, 6, 4.8, 'Midjourney outputs are stunning.'),
        (7, 2, 5, 6, 4.9, 'Version 6 is a massive improvement.'),
    ]
    for rid, version, aid, uid, rating, text in reviews_data:
        db.session.add(Reviews(review_ID=rid, version=version, ai_ID=aid, user_ID=uid,
                               rating=rating, written_Review=text,
                               date=now - random.randint(10000, 5000000)))
    db.session.commit()

    # --- Topical Reviews ---
    # PK is (review_ID, version) — one topical entry per review version
    topicals_data = [
        (1, 1, 'Accuracy',  4.5),
        (1, 2, 'Accuracy',  4.8),
        (2, 1, 'Speed',     4.0),
        (2, 2, 'Speed',     4.2),
        (3, 1, 'Usability', 5.0),
        (3, 2, 'Usability', 4.9),
        (4, 1, 'Value',     4.6),
        (4, 2, 'Value',     4.7),
        (5, 1, 'Features',  4.0),
        (5, 2, 'Features',  4.3),
        (6, 1, 'Accuracy',  4.4),
        (6, 2, 'Accuracy',  4.5),
        (7, 1, 'Usability', 4.8),
        (7, 2, 'Usability', 4.9),
    ]
    for rid, version, ttype, rating in topicals_data:
        db.session.add(Topical_Reviews(review_ID=rid, version=version, types=ttype, rating=rating))
    db.session.commit()

    # --- Review Votes ---
    # PK is (user_ID, review_ID, version)
    votes_data = [
        (2, 1, 1,  1),
        (3, 1, 1,  1),
        (4, 1, 2, -1),
        (1, 2, 1,  1),
        (5, 2, 1, -1),
        (6, 3, 1,  1),
        (1, 3, 2,  1),
        (2, 4, 1,  1),
        (6, 4, 2, -1),
        (1, 5, 1,  1),
        (2, 5, 2,  1),
        (3, 6, 1,  1),
        (4, 6, 2, -1),
        (1, 7, 1,  1),
        (2, 7, 2,  1),
    ]
    for uid, rid, version, vote in votes_data:
        db.session.add(Review_Votes(user_ID=uid, review_ID=rid, version=version, vote=vote))
    db.session.commit()

    # --- Tags ---
    # PK is (ai_ID, user_ID)
    tags_data = [
        (1, 1, 'coding'),
        (1, 2, 'writing'),
        (2, 3, 'research'),
        (2, 4, 'productivity'),
        (3, 5, 'free'),
        (3, 1, 'writing'),
        (4, 2, 'coding'),
        (4, 6, 'automation'),
        (5, 3, 'creative'),
        (5, 4, 'premium'),
    ]
    for aid, uid, tag in tags_data:
        db.session.add(Tags(ai_ID=aid, user_ID=uid, tag=tag))
    db.session.commit()

    # --- Bookmarks ---
    # PK is (ai_ID, user_ID)
    bookmarks_data = [
        (1, 1), (1, 3), (2, 2), (2, 4),
        (3, 5), (3, 6), (4, 1), (4, 2),
        (5, 3), (5, 5),
    ]
    for aid, uid in bookmarks_data:
        db.session.add(Bookmarks(ai_ID=aid, user_ID=uid))
    db.session.commit()

    print("Database populated successfully!\n")

    # --- Print all data ---
    print("Users:")
    for u in Users.query.all():
        print(f"  ID: {u.user_ID}, Username: {u.username}, Email: {u.email}")

    print("\nAI Tools:")
    for t in AI_Tools.query.all():
        print(f"  ID: {t.ai_ID}, Name: {t.name}, Company: {t.company}, Category: {t.category}, Rating: {t.rating}")

    print("\nReviews:")
    for r in Reviews.query.all():
        print(f"  Review ID: {r.review_ID}, Version: {r.version}, AI: {r.ai_ID}, User: {r.user_ID}, Rating: {r.rating}")

    print("\nTopical Reviews:")
    for tr in Topical_Reviews.query.all():
        print(f"  Review ID: {tr.review_ID}, Version: {tr.version}, Type: {tr.types}, Rating: {tr.rating}")

    print("\nReview Votes:")
    for v in Review_Votes.query.all():
        print(f"  User: {v.user_ID}, Review: {v.review_ID}, Version: {v.version}, Vote: {v.vote}")

    print("\nTags:")
    for tag in Tags.query.all():
        print(f"  AI: {tag.ai_ID}, User: {tag.user_ID}, Tag: {tag.tag}")

    print("\nBookmarks:")
    for bm in Bookmarks.query.all():
        print(f"  AI: {bm.ai_ID}, User: {bm.user_ID}")
