import random
import time

from app import app
from extensions import db
from models import Users, Reviews, Review_Votes, AI_Tools, Topical_Reviews, Tags, Bookmarks
from sqlalchemy import func

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
        (1, 'ChatGPT',        'OpenAI',      4.5, 20.0, 'Language Model', 'https://chat.openai.com',   '/static/img/chat_gpt.jpg'),
        (2, 'Claude',         'Anthropic',   4.7, 20.0, 'Language Model', 'https://claude.ai',         '/static/img/claude_logo.jpg'),
        (3, 'Gemini',         'Google',      4.2,  0.0, 'Language Model', 'https://gemini.google.com', '/static/img/gemini.png'),
        (4, 'GitHub Copilot', 'Microsoft',   4.3, 10.0, 'Code Assistant', 'https://github.com/features/copilot', '/static/img/copilot.png'),
        (5, 'Midjourney',     'Midjourney',  4.6, 10.0, 'Image Generation','https://midjourney.com',   '/static/img/midjourney.jpg'),
    ]
    for aid, name, company, rating, price, category, website_url, img_url in tools_data:
        db.session.add(AI_Tools(ai_ID=aid, name=name, company=company, rating=rating,
                                price=price, category=category, website_url=website_url,
                                img_url=img_url, date=now - random.randint(1000000, 50000000)))
    db.session.commit()

    # --- Reviews ---
    # (review_ID, version, ai_ID, user_ID, rating, text)
    reviews_data = [
        # ChatGPT (ai_ID=1)
        (1,  1, 1, 1, 4.7, 'ChatGPT impresses with its coding suggestions and broad knowledge. The plugin ecosystem makes it incredibly versatile for day-to-day tasks.'),
        (1,  2, 1, 1, 4.8, 'After months of daily use, ChatGPT remains my go-to for everything from drafting emails to debugging code. GPT-4 is a significant upgrade.'),
        (2,  1, 1, 2, 3.5, 'Good for general questions but unreliable for anything requiring up-to-date information. Hallucinations are frustrating when doing serious research.'),
        (3,  1, 1, 4, 2.5, 'Confidently states wrong facts too often. I double-check everything it produces now. Not suitable for anything high-stakes.'),
        # Claude (ai_ID=2)
        (4,  1, 2, 3, 5.0, 'Claude is in a league of its own for nuanced, thoughtful responses. It handles complex tasks with a level of depth that other models cannot match.'),
        (4,  2, 2, 3, 5.0, 'Still my number one after extensive testing. The long context window is a game changer for reading and summarizing full documents.'),
        (5,  1, 2, 5, 4.3, 'Impressed by how Claude handles ambiguity — it asks clarifying questions instead of assuming. That alone saves a lot of unnecessary back and forth.'),
        (6,  1, 2, 1, 3.8, 'Solid model, but the lack of image generation and third-party integrations makes it feel limited compared to the competition.'),
        # Gemini (ai_ID=3)
        (7,  1, 3, 5, 4.2, 'Gemini really shines when used alongside Google products. The integration with Docs and Gmail makes it a natural fit for everyday productivity.'),
        (7,  2, 3, 5, 4.3, 'The multimodal capabilities are genuinely impressive — being able to analyze images alongside text sets it apart from most competitors.'),
        (8,  1, 3, 6, 3.0, 'Feels like Google is playing catch-up. Decent but lacks the polish of ChatGPT or Claude. Hopefully future updates improve the reasoning quality.'),
        (9,  1, 3, 2, 4.0, 'Free tier is generous and performance is solid for most use cases. A great entry point for anyone new to AI tools who does not want to pay upfront.'),
        # GitHub Copilot (ai_ID=4)
        (10, 1, 4, 1, 4.8, 'Copilot has transformed how I write code. It anticipates what I need almost every time and the VS Code integration is completely seamless.'),
        (10, 2, 4, 1, 4.9, 'The new chat feature makes it even better. It is like having a senior developer pair programming with you around the clock.'),
        (11, 1, 4, 3, 4.0, 'Solid tool but it occasionally suggests outdated patterns or insecure code snippets. Always review what it generates before committing to production.'),
        (12, 1, 4, 6, 3.2, 'The subscription price is hard to justify for solo developers. Great for teams but the individual plan feels overpriced for what you actually get.'),
        # Midjourney (ai_ID=5)
        (13, 1, 5, 6, 4.9, 'Midjourney consistently produces the most beautiful AI-generated imagery I have seen. Version 6 raised the bar — outputs are nearly indistinguishable from real photos.'),
        (14, 1, 5, 4, 4.4, 'The quality is undeniable but the Discord-only interface is a major friction point. A proper web app would easily make this a perfect five stars.'),
        (14, 2, 5, 4, 4.5, 'They have been improving the web interface steadily. Still not fully there yet, but it is getting significantly better with each update.'),
        (15, 1, 5, 2, 3.6, 'Stunning results when you know how to prompt well, but the learning curve for getting consistent outputs is steep. Definitely not beginner-friendly.'),
    ]
    for rid, version, aid, uid, rating, text in reviews_data:
        db.session.add(Reviews(review_ID=rid, version=version, ai_ID=aid, user_ID=uid,
                               rating=rating, written_Review=text,
                               date=now - random.randint(10000, 5000000)))
    db.session.commit()

    # --- Recalculate tool ratings from latest review versions ---
    for tool in AI_Tools.query.all():
        subq = (db.session.query(Reviews.review_ID, func.max(Reviews.version).label('max_v'))
                .filter_by(ai_ID=tool.ai_ID)
                .group_by(Reviews.review_ID)
                .subquery())
        avg = (db.session.query(func.avg(Reviews.rating))
               .join(subq, (Reviews.review_ID == subq.c.review_ID) &
                           (Reviews.version == subq.c.max_v))
               .scalar())
        tool.rating = round(float(avg), 1) if avg else None
    db.session.commit()

    # --- Topical Reviews ---
    # PK is (review_ID, version, types)
    topicals_data = [
        (1,  2, 'Accuracy',   4.8),
        (1,  2, 'Value',      4.5),
        (2,  1, 'Accuracy',   3.0),
        (3,  1, 'Accuracy',   2.5),
        (4,  2, 'Usability',  5.0),
        (4,  2, 'Value',      4.8),
        (5,  1, 'Usability',  4.5),
        (6,  1, 'Value',      3.5),
        (7,  2, 'Features',   4.5),
        (7,  2, 'Usability',  4.3),
        (8,  1, 'Accuracy',   3.0),
        (9,  1, 'Value',      4.5),
        (10, 2, 'ease_of_use',5.0),
        (10, 2, 'Accuracy',   4.8),
        (11, 1, 'Accuracy',   4.0),
        (12, 1, 'Value',      3.0),
        (13, 1, 'creativity', 5.0),
        (14, 2, 'Usability',  4.0),
        (14, 2, 'creativity', 4.5),
        (15, 1, 'creativity', 3.5),
    ]
    for rid, version, ttype, rating in topicals_data:
        db.session.add(Topical_Reviews(review_ID=rid, version=version, types=ttype, rating=rating))
    db.session.commit()

    # --- Review Votes ---
    # PK is (user_ID, review_ID, version)
    votes_data = [
        (2,  1,  2,  1),
        (3,  1,  2,  1),
        (5,  2,  1,  1),
        (1,  3,  1, -1),
        (2,  3,  1,  1),
        (4,  4,  2,  1),
        (1,  4,  2,  1),
        (6,  5,  1,  1),
        (2,  7,  2,  1),
        (4,  8,  1, -1),
        (1,  8,  1, -1),
        (3,  10, 2,  1),
        (5,  10, 2,  1),
        (2,  13, 1,  1),
        (1,  13, 1,  1),
        (3,  14, 2,  1),
        (5,  15, 1, -1),
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
