from otree.api import *
import datetime
import pandas as pd
import numpy as np
import itertools
import re


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'feed'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    RULES_TEMPLATE = "feed/T_Rules.html"
    PRIVACY_TEMPLATE = "feed/T_Privacy.html"
    TWEET_TEMPLATE = "feed/T_Tweet.html"
    ATTENTION_TEMPLATE = "feed/T_Attention_Check.html"
    TOPICS_TEMPLATE = "feed/T_Trending_Topics.html"

    FEED_LENGTH = list(range(*{'start':0,'stop':41,'step':1}.values()))
    TWEET_LENGTH = list(range(*{'start':0,'stop':41,'step':1}.values()))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField(doc='indicates the treatment a player is randomly assigned to')
    privacy_time = models.FloatField(doc="counts the number of seconds the privacy statement was opened.", blank=True)

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
    shuffle = itertools.cycle(['clean', 'polluted'])
    for player in subsession.get_players():
        player.treatment = next(shuffle)


# PAGES
class A_Intro(Page):
    form_model = "player"
    form_fields = ["privacy_time"]


class B_Instructions(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        # read data and shuffle
        tweets = pd.read_csv('feed/static/tweets/sample_tweets.csv', sep=';')
        tweets = tweets.sample(frac=1)
        tweets['index'] = range(1, len(tweets) + 1)

        # reformat date
        tweets['datetime'] = pd.to_datetime(tweets['datetime'], errors='coerce')
        tweets['date'] = tweets['datetime'].dt.strftime('%d %b').str.replace(' ', '. ')
        tweets['date'] = tweets['date'].str.replace('^0', '', regex=True)

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
        tweets['profile_pic_available'] = np.where(tweets['user_image'].isnull(), False, True)

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

        # create row ID
        tweets['row'] = range(1, len(tweets) + 1)

        # store data on participant level
        player.participant.tweets = tweets


class C_Feed(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        items = player.participant.tweets['doc_id'].values.tolist()
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
