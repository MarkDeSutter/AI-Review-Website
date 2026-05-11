from extensions import db


class Users(db.Model):
    __tablename__ = 'users'

    user_ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_Created = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Relationships
    reviews = db.relationship('Reviews', backref='user', lazy=True)
    votes = db.relationship('Review_Votes', backref='user', lazy=True)
    tags = db.relationship('Tags', backref='user', lazy=True)
    bookmarks = db.relationship('Bookmarks', backref='user', lazy=True)


class Reviews(db.Model):
    __tablename__ = 'reviews'

    review_ID = db.Column(db.Integer(), primary_key=True)
    ai_ID = db.Column(db.Integer(), db.ForeignKey('ai_tools.ai_ID'), nullable=False)
    user_ID = db.Column(db.Integer(), db.ForeignKey('users.user_ID'), nullable=False)
    rating = db.Column(db.Float(), nullable=True)
    written_Review = db.Column(db.String(700), nullable=True)
    date = db.Column(db.Integer(), nullable=False)
    version = db.Column(db.Integer(), primary_key=True, nullable=False)

    # Relationships
    topical_reviews = db.relationship('Topical_Reviews', backref='review', lazy=True)
    votes = db.relationship('Review_Votes', backref='review', lazy=True)


class Review_Votes(db.Model):
    __tablename__ = 'review_votes'

    user_ID = db.Column(db.Integer, db.ForeignKey('users.user_ID'), primary_key=True)
    review_ID = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['review_ID', 'version'],
            ['reviews.review_ID', 'reviews.version']
        ),
    )

    # Relationships


class AI_Tools(db.Model):
    __tablename__ = 'ai_tools'

    ai_ID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    company = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Float(), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    category = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Integer(), nullable=False)
    website_url = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)

    # Relationships
    reviews = db.relationship('Reviews', backref='ai_tool', lazy=True)
    tags = db.relationship('Tags', backref='ai_tool', lazy=True)
    bookmarks = db.relationship('Bookmarks', backref='ai_tool', lazy=True)


class Topical_Reviews(db.Model):
    __tablename__ = 'topical_reviews'

    review_ID = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer(), primary_key=True)
    types = db.Column(db.Text(), nullable=True)
    rating = db.Column(db.Float(), nullable=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['review_ID', 'version'],
            ['reviews.review_ID', 'reviews.version']
        ),
    )



class Tags(db.Model):
    __tablename__ = 'tags'

    ai_ID = db.Column(db.Integer(), db.ForeignKey('ai_tools.ai_ID'), primary_key=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('users.user_ID'), primary_key=True)
    tag = db.Column(db.Text(), nullable=False)



class Bookmarks(db.Model):
    __tablename__ = 'bookmarks'

    ai_ID = db.Column(db.Integer(), db.ForeignKey('ai_tools.ai_ID'), primary_key=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('users.user_ID'), primary_key=True)

