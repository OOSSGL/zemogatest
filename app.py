from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import BadRequest, NotFound

from decouple import config
import tweepy


auth = tweepy.OAuthHandler(config('TWITTER_API_KEY'),
                           config('TWITTER_SECRET_KEY'))
auth.set_access_token(config('TWITTER_TOKEN'),
                      config('TWITTER_TOKEN_SECRET'))

twitter_api = tweepy.API(auth)

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = config('MYSQL_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Portfolio Class/Model
class Portfolio(db.Model):
    idportfolio = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    twitter_user_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    experience_summary = db.Column(db.String(255))
    last_names = db.Column(db.String(255))
    names = db.Column(db.String(255))
    twitter_user_id = db.Column(db.String(255))

    def __init__(
          self,
          description,
          image_url,
          twitter_user_name,
          title,
          user_id,
          experience_summary,
          last_names,
          names,
          twitter_user_id
    ):
        self.description = description
        self.image_url = image_url
        self.twitter_user_name = twitter_user_name
        self.title = title
        self.user_id = user_id
        self.experience_summary = experience_summary
        self.last_names = last_names
        self.names = names
        self.twitter_user_id = twitter_user_id


# Portfolio Schema
class PortfolioSchema(ma.Schema):
    class Meta:
        fields = (
            'idportfolio',
            'description',
            'image_url',
            'twitter_user_name',
            'title',
            'user_id',
            'experience_summary',
            'last_names',
            'names',
            'twitter_user_id'
        )


# Init schema
portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


# Create a Portfolio
@app.route('/portfolio', methods=['POST'])
def add_portfolio():
    description = None
    image_url = None
    twitter_user_name = None
    title = None
    user_id = None
    experience_summary = None
    last_names = None
    names = None
    twitter_user_id = None

    # Check if each field is given and is not null or empty
    if 'description' not in request.json:
        raise BadRequest('Field description is required')
    if not request.json['description']:
        raise BadRequest('Field description cannot be empty or null')
    if 'image_url' not in request.json:
        raise BadRequest('Field image_url is required')
    if not request.json['image_url']:
        raise BadRequest('Field image_url cannot be empty or null')
    if 'twitter_user_name' not in request.json:
        raise BadRequest('Field twitter_user_name is required')
    if not request.json['twitter_user_name']:
        raise BadRequest('Field twitter_user_name cannot be empty or null')
    if 'title' not in request.json:
        raise BadRequest('Field title is required')
    if not request.json['title']:
        raise BadRequest('Field title cannot be empty or null')

    description = request.json['description']
    image_url = request.json['image_url']
    twitter_user_name = request.json['twitter_user_name']
    title = request.json['title']

    # Those are optional
    if 'user_id' in request.json and request.json['user_id']:
        user_id = request.json['user_id']
    if 'experience_summary' in request.json and request.json['experience_summary']:
        experience_summary = request.json['experience_summary']
    if 'last_names' in request.json and request.json['last_names']:
        last_names = request.json['last_names']
    if 'names' in request.json and request.json['names']:
        names = request.json['names']
    if 'twitter_user_id' in request.json and request.json['twitter_user_id']:
        twitter_user_id = request.json['twitter_user_id']

    new_portfolio = Portfolio(
        description,
        image_url,
        twitter_user_name,
        title,
        user_id,
        experience_summary,
        last_names,
        names,
        twitter_user_id
    )

    db.session.add(new_portfolio)
    db.session.commit()

    return portfolio_schema.jsonify(new_portfolio)


# Get All Portfolios
@app.route('/portfolio', methods=['GET'])
def get_portfolios():
    all_portfolios = Portfolio.query.all()
    result = portfolios_schema.dump(all_portfolios)
    return jsonify(result)


# Get Single Portfolio
@app.route('/portfolio/<id>', methods=['GET'])
def get_portfolio(id):
    portfolio = Portfolio.query.get(id)
    return portfolio_schema.jsonify(portfolio)


# Update a Portfolio
@app.route('/portfolio/<id>', methods=['PUT'])
def update_portfolio(id):
    portfolio = Portfolio.query.get(id)
    if not portfolio:
        raise NotFound

    # Check if each field is given and is not null or empty
    if 'description' in request.json and request.json['description']:
        portfolio.description = request.json['description']
    if 'image_url' in request.json and request.json['image_url']:
        portfolio.image_url = request.json['image_url']
    if 'twitter_user_name' in request.json and request.json['twitter_user_name']:
        portfolio.twitter_user_name = request.json['twitter_user_name']
    if 'title' in request.json and request.json['title']:
        portfolio.title = request.json['title']
    if 'user_id' in request.json and request.json['user_id']:
        portfolio.user_id = request.json['user_id']
    if 'experience_summary' in request.json and request.json['experience_summary']:
        portfolio.experience_summary = request.json['experience_summary']
    if 'last_names' in request.json and request.json['last_names']:
        portfolio.last_names = request.json['last_names']
    if 'names' in request.json and request.json['names']:
        portfolio.names = request.json['names']
    if 'twitter_user_id' in request.json and request.json['twitter_user_id']:
        portfolio.twitter_user_id = request.json['twitter_user_id']

    db.session.commit()

    return portfolio_schema.jsonify(portfolio)


# Delete Portfolio
@app.route('/portfolio/<id>', methods=['DELETE'])
def delete_portfolio(id):
    portfolio = Portfolio.query.get(id)
    if not portfolio:
        raise NotFound

    db.session.delete(portfolio)
    db.session.commit()

    return portfolio_schema.jsonify(portfolio)


# Get Tweets
@app.route('/tweets/<screen_name>', methods=['GET'])
def get_tweets(screen_name):
    try:
        tweets = twitter_api.user_timeline(screen_name=screen_name, count=5)
        res_tweets = []
        for tweet in tweets:
            res_tweet = {
                'date': tweet.created_at,
                'text': tweet.text
            }
            print(tweet.text)
            res_tweets.append(res_tweet)
        response = {
            'tweets': res_tweets
        }
        return response
    except tweepy.error.TweepError as e:
        error = 'Code: ' + str(e.args[0][0]['code']) + ' Message: ' + e.args[0][0]['message']
        raise BadRequest(error)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
