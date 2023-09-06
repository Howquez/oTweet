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
    NAME_IN_URL = 'News'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    RULES_TEMPLATE = "Twitter/T_Rules.html"
    PRIVACY_TEMPLATE = "Twitter/T_Privacy.html"
    NEWS_TEMPLATE = "news/News_Template.html"
    ATTENTION_TEMPLATE = "Twitter/T_Attention_Check.html"
    TOPICS_TEMPLATE = "Twitter/T_Trending_Topics.html"
    BANNER_TEMPLATE = "Twitter/T_Banner_Ads.html"

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

def creating_session(subsession):
    shuffle = itertools.cycle(['clean', 'polluted'])
    for player in subsession.get_players():
        player.treatment = next(shuffle)
        print(player.session.config['tweets_url'])

h = httplib2.Http()

def check_url_exists(url):
    try:
        resp = h.request(url, 'HEAD')
        return int(resp[0]['status']) < 400
    except Exception:
        return False

# PAGES
class B_Instructions(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        # read data
        news = pd.read_csv('News/static/news.csv', sep=';')

        # index
        news['index'] = range(1, len(news) + 1)

        # print((posts))

        # participant vars
        player.participant.news = news

class C_Feed(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        items = player.participant.news['index'].values.tolist()
        items.insert(0, 0)
        return ['liked_item_' + str(n) for n in items] + \
               ['reply_to_item_' + str(n) for n in items]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            tweets=player.participant.news.to_dict('index'),
            topics=player.session.config['topics'],
            search_term=player.session.config['search_term']
        )

page_sequence = [B_Instructions,
                C_Feed]
