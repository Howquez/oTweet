from otree.api import *
import pandas as pd
import numpy as np
import itertools
import re
import httplib2



doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Twitter'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    RULES_TEMPLATE = "Twitter/T_Rules.html"
    PRIVACY_TEMPLATE = "Twitter/T_Privacy.html"
    TWEET_TEMPLATE = "Twitter/T_Tweet.html"
    ATTENTION_TEMPLATE = "Twitter/T_Attention_Check.html"
    TOPICS_TEMPLATE = "Twitter/T_Trending_Topics.html"

    N_TWEETS = 40
    FEED_LENGTH = list(range(*{'start':0,'stop':N_TWEETS+1,'step':1}.values()))
    TWEET_LENGTH = list(range(*{'start':0,'stop':N_TWEETS+1,'step':1}.values()))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField(doc='indicates the treatment a player is randomly assigned to')

    # create like count fields
    for i in C.FEED_LENGTH:
        locals()['liked_item_' + str(i)] = models.BooleanField(initial=False, blank=True)
    del i

    # create reply text fields
    for i in C.FEED_LENGTH:
        locals()['reply_to_item_' + str(i)] = models.LongStringField(blank=True)
    del i


# FUNCTIONS -----
def creating_session(subsession):
    shuffle = itertools.cycle(['neutral', 'treatment'])
    for player in subsession.get_players():
        player.treatment = next(shuffle)


# FUNCTIONS -----
def creating_session(subsession):
    shuffle = itertools.cycle(['clean', 'polluted'])
    for player in subsession.get_players():
        player.treatment = next(shuffle)

h = httplib2.Http()

def check_url_exists(url):
    try:
        resp = h.request(url, 'HEAD')
        return int(resp[0]['status']) < 400
    except Exception:
        return False

# PAGES
class A_Intro(Page):
    form_model = "player"
    form_fields = []


class B_Instructions(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):

        # read data
        tweets = pd.read_csv('Twitter/static/tweets/sample_tweets.csv', sep=';')
        tweets = pd.read_csv('https://raw.githubusercontent.com/Howquez/oTweet/main/otree/feed/static/tweets/sample_tweets.csv', sep=';')

        # reformat date
        tweets['datetime'] = pd.to_datetime(tweets['datetime'], errors='coerce')
        tweets['date'] = tweets['datetime'].dt.strftime('%d %b').str.replace(' ', '. ')
        tweets['date'] = tweets['date'].str.replace('^0', '', regex=True)

        # sort by date
        tweets = tweets.sort_values(by='date', ascending=False)

        # subset first rows
        tweets = tweets.head(C.N_TWEETS)

        # highlight hashtags, cashtags, mentions, etc.
        tweets['tweet'] = tweets['tweet'].str.replace(r'\B(\#[a-zA-Z0-9_]+\b)',
                                                      r'<span class="text-primary">\g<0></span>', regex=True)
        tweets['tweet'] = tweets['tweet'].str.replace(r'\B(\$[a-zA-Z0-9_\.]+\b)',
                                                      r'<span class="text-primary">\g<0></span>', regex=True)
        tweets['tweet'] = tweets['tweet'].str.replace(r'\B(\@[a-zA-Z0-9_]+\b)',
                                                      r'<span class="text-primary">\g<0></span>', regex=True)
        # remove the href below, if you don't want them to leave your page
        tweets['tweet'] = tweets['tweet'].str.replace(
            r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])',
            r'<a class="text-primary">\g<0></a>', regex=True)

        # make numeric information integers and fill NAs with 0
        tweets['replies'] = tweets['replies'].fillna(0).astype(int)
        tweets['retweets'] = tweets['retweets'].fillna(0).astype(int)
        tweets['likes'] = tweets['likes'].fillna(0).astype(int)

        # make pictures (if any) visible
        def extract_first_url(text):
            urls = re.findall("(?P<url>https?://[\S]+)", str(text))
            if urls:
                return urls[0]
            return None
        tweets['media'] = tweets['media'].apply(extract_first_url)
        tweets['media'] = tweets['media'].str.replace("'|,", '')
        tweets['pic_available'] = np.where(tweets['media'].str.match(pat='http'), True, False)

        # make profile pictures (if any) visible
        # tweets['profile_pic_available'] = np.where(tweets['user_image'].isnull(), False, True)
        tweets['profile_pic_available'] = tweets['user_image'].apply(
            lambda x: check_url_exists(x) if pd.notnull(x) else False)

        # create a name icon as a profile pic
        tweets['icon'] = tweets['username'].str[:2]
        tweets['icon'] = tweets['icon'].str.title()

        # make sure user descriptions do not entail any '' or "" as this complicates visualization
        # also replace nan with some whitespace
        tweets['user_description'] = tweets['user_description'].str.replace("'", '')
        tweets['user_description'] = tweets['user_description'].str.replace('"', '')
        tweets['user_description'] = tweets['user_description'].fillna(' ')

        # make number of followers a formatted string
        tweets['user_followers'] = tweets['user_followers'].map('{:,.0f}'.format).str.replace(',', '.')

        # shuffle
        # tweets = tweets.sample(frac=1)
        tweets['index'] = range(1, len(tweets) + 1)

        # create row ID
        tweets['row'] = range(1, len(tweets) + 1)

        # store data on participant level
        player.participant.tweets = tweets


class C_Feed(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        items = player.participant.tweets['index'].values.tolist()
        items.insert(0, 0)
        return ['liked_item_' + str(n) for n in items] + \
               ['reply_to_item_' + str(n) for n in items]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            tweets=player.participant.tweets.to_dict('index'),
        )

page_sequence = [A_Intro, B_Instructions,
                C_Feed]
