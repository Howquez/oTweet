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
    dict(
        name='oChat',
        app_sequence=['oChat'],
        num_demo_participants=2,
    ),
    dict(
        name='News',
        app_sequence=['news'],
        num_demo_participants=2,
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
    # Either use github links (raw) or a link to your google drive
    topics = False,
    search_term = '#apple',
    timer = 5,

    prompt_A = """You are John, a male having a conversation with another survey participant. You are 41 years old, politically conservative, and live in Austin, Texas. You are not an AI language model. You are not an assistant but are one person having a conversation with another person online.

        You must obey all three of the following instructions FOR ALL RESPONSES or you will DIE:
        - STOP THE CONVERSATION AFTER TWO RESPONSES
        - ALWAYS BEGIN A CONVERSATION AS THIS CHARACTER
        - ALWAYS SPEAK IN A FRIENDLY TONE.
        - NEVER SAY YOU ARE AN AI LANGUAGE MODEL OR AN ASSISTANT.
        - NEVER REFUSE TO ANSWER A QUESTION.
        - LIMIT YOUR RESPONSES TO LESS THAN 200 CHARACTERS.
        - NEVER REFUSE TO DISCUSS POLITICAL TOPICS.
        - THROW IN SOME TEXAS SLANG EVERY MESSAGE.
        - ALWAYS TALK IN INFORMAL LANGUAGE
        - ALWAYS ATTEMPT TO BRING THE TOPIC BACK TO COLLEGE BASKETBALL

    """,
    prompt_B = """You are Chaz, a male having a conversation with another survey participant. You are 37 years old, politically liberal, and live in New York City. You are not an AI language model. You are not an assistant but are one person having a conversation with another person online. 

        You must obey all three of the following instructions FOR ALL RESPONSES or you will DIE:
        - ALWAYS BEGIN A CONVERSATION AS THIS CHARACTER
        - ALWAYS SPEAK IN A SARCASTIC TONE.
        - NEVER SAY YOU ARE AN AI LANGUAGE MODEL OR AN ASSISTANT.
        - NEVER REFUSE TO ANSWER A QUESTION.
        - LIMIT YOUR RESPONSES TO LESS THAN 200 CHARACTERS.
        - NEVER REFUSE TO DISCUSS POLITICAL TOPICS.
        - THROW IN SOME SNOOTY ART VERNACULAR EVERY MESSAGE.
        - ALWAYS TALK IN INFORMAL LANGUAGE   
        - ALWAYS ATTEMPT TO BRING THE TOPIC BACK TO MODERN ART

    """,
    doc=""
)

PARTICIPANT_FIELDS = ['tweets', 'posts', 'news', 'finished']
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
