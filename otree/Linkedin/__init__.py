from otree.api import *
import pandas as pd
import numpy as np

import itertools

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Linkedin'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    COL_RIGHT_TEMPLATE = "Linkedin/T_Col_Right.html"
    COL_LEFT_TEMPLATE = "Linkedin/T_Col_Left.html"
    NAVBAR_TEMPLATE = "Linkedin/T_Navbar.html"
    FEED_TEMPLATE = "Linkedin/T_Feed.html"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(doc="The participant's name")
    treatment = models.StringField(doc="The participant's treatment status.")
    PIN = models.StringField(doc="The participant's name")



# FUNCTIONS -----
def creating_session(subsession):
    shuffle = itertools.cycle(['control', 'treatment'])
    for player in subsession.get_players():
        player.treatment = next(shuffle)


# PAGES

class Intro(Page):
    form_model = 'player'
    form_fields = ['name']

    @staticmethod
    def before_next_page(player, timeout_happened):
        # read data
        posts = pd.read_csv('Linkedin/static/posts_12.csv', sep=',')

        # subset
        posts = posts[posts["group"] == player.treatment]

        # highlight hashtags, cashtags, mentions, etc.
        posts['text'] = posts['text'].str.replace(r'\B(\#[a-zA-Z0-9_]+\b)',
                                                      r'<span class="text-primary">\g<0></span>', regex=True)
        posts['text'] = posts['text'].str.replace(r'\B(\$[a-zA-Z0-9_\.]+\b)',
                                                      r'<span class="text-primary">\g<0></span>', regex=True)
        posts['text'] = posts['text'].str.replace(r'\B(\@[a-zA-Z0-9_]+\b)',
                                                      r'<span class="text-primary">\g<0></span>', regex=True)

        # make numeric information integers and fill NAs with 0
        posts['likes_count'] = posts['likes_count'].fillna(0).astype(int)
        posts['comments_count'] = posts['comments_count'].fillna(0).astype(int)

        # pics
        posts['pic_available'] = np.where(posts['media'].isnull(), False, True)
        posts['profile_pic_available'] = np.where(posts['user_image'].isnull(), False, True)

        print( posts['pic_available'])
        
        # index
        posts['index'] = range(1, len(posts) + 1)

        #print((posts))

        # participant vars
        player.participant.posts = posts

class PIN(Page):
    form_model = 'player'
    form_fields = ['PIN']


class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            posts=player.participant.posts.to_dict('index'),
            pic="https://cdn-icons-png.flaticon.com/512/727/727399.png?w=1380&t=st=1682605622~exp=1682606222~hmac=7dae0d644fca039ecd3c0366eb7b39c11d38a49bcaf75a5f9675e4310956fd7e"
        )


page_sequence = [Intro, MyPage]
