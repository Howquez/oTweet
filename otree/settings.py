from os import environ

SESSION_CONFIGS = [
    dict(
        name='Twitter',
        app_sequence=['Twitter'],
        num_demo_participants=4,
    ),
    dict(
        name='Linkedin',
        app_sequence=['Linkedin'],
        num_demo_participants=4,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=2.10,
    tweets_url = 'https://raw.githubusercontent.com/Howquez/oTweet/main/otree/Twitter/static/tweets/sample_tweets.csv',
    # Either use github links (raw) or a link to your google drive following this pattern: https://drive.google.com/uc?export=download&id=FILE_ID
    # see how to retrieve that ID here: https://stackoverflow.com/a/62698638
    doc=""
)

PARTICIPANT_FIELDS = ['tweets', 'posts', 'finished']
SESSION_FIELDS = ['prolific_completion_url']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8744261096089'
