crontable = []
outputs = []
from time import sleep
import re
import string
import random

from phteven_helper import (
    PhtevenRules,
    PhtevenProcessor,
    SlackUsers,
    Data
)
from cacher import Cacher

thats_something = re.compile(ur"^that(\u2019|\')?s (.*)$", re.IGNORECASE)
youre_something = re.compile(ur"^.*you(\u2019|\')?re? (\w+)$", re.IGNORECASE)
myth_busted = re.compile(r"myth (busted|confirmed)", re.IGNORECASE)
meow_now = re.compile(r'\bnow\b', re.IGNORECASE)
myth_busted_phrases = ['Mythterious',
                       'Mythinterpreted',
                       'You\'re mythtaken',
                       'Yes. Myth confirmed',
                       'Pindeed. Myth busted',
                       "That's mythguided",
                       "Hmm...you may have mythjudged that one",
                       "That's being mythused"
                       ]
giphy_phrases = ["hmmmm...that one kinda sucked",
                 "/giphy NOICE", "NOICE",
                 "wat",
                 "uhhhh nope",
                 "ya ya ya!"
                 ]
phteven_phrases = [
    "WAH?",
    "mayhaps...",
    "yeah...but can that be real if science isn't real?",
    "yeah...but can that be real if ghosts aren't real?",
    "I think I've hit the Phteven peak",
    "hmmmMMMMmmmMmmmMMmmMmmmmm",
    "Great success!",
]
only_hello = re.compile(r'[^A-Za-z0-9]')
watdisis = re.compile(r'wh?at.*dis.*is', re.IGNORECASE)
arentreal = re.compile(ur'aren(\'|\u2019)?t real', re.IGNORECASE)
baylor = re.compile(r'(\w+(er|or))[%s]*$' % re.escape(string.punctuation), re.IGNORECASE)


def translate(t):
    from translate import Translator
    translator = Translator(to_lang="en", from_lang="es")
    return translator.translate(t)


def say_smarx_and_reset():
    to_say = Cacher.get_smarx_messages()[0]
    Cacher.reset_smarx_messages()
    return to_say

def test_smarx(_):
    print "test smarx", Cacher.get_smarx_messages()
    return len(Cacher.get_smarx_messages()) >= 10
    
def process_message(data):
    print "process message", data
    data = Data(**data)
    # Be quiet for a while man....
    if SlackUsers.phteven.at.is_in(data.text) and 'shhh' in data.text.lower():
        print "Shhhhhhhhhh........"
        sleep(5 * 60)
        return
    if str(SlackUsers.smarx) == data.user:
        Cacher.add_smarx_message(data.text)
        print "Smarx length", len(Cacher.get_smarx_messages())
    # We don't care what Phteven Marquarst says
    if data.user == u'U0Y8YJCBU':
        return

    rules = PhtevenRules(data)

    rules.add_many_exclusive([

        # If @Phteven gets mentioned
        (lambda data: SlackUsers.phteven.at.is_in(data.text), lambda: "^ %s" % SlackUsers.stephen.at),
        # NO EDITING
        (lambda data: data.subtype == u'message_changed', lambda: "I SAW THAT.\n\n> %s" % data.previous_message['text']),
        # Copy smarx
        (lambda data: random.random() < 0.05 and data.user == "U04TR0MSC", lambda: data.text),
        # Smarx has an elipsis
        (lambda data: u"\u2026" in data.text and data.user == "U04TR0MSC", lambda: "Nice try, Steven J Smarx"),
        # Are we in burgertory?
        (lambda data: 'burgertory' in data.text.lower() or 'burgatory' in data.text.lower(), lambda: "We're always in burgertory"),
        # Ask Zeebs what he thinks if no one else knows
        (lambda data: 'no idea' == data.text.lower(), lambda: "<@U04JH6A3N>, what do you think?"),
        # Zeebs trying to be funny
        (lambda data: thats_something.search(data.text) and data.user == u'U04JH6A3N', lambda: "Shut up, Zeebs"),
        # Am i saying meow?
        (lambda data: meow_now.search(data.text), lambda: "Right meow?"),
        # That's <blank>
        (lambda data: thats_something.search(data.text), lambda: "You're %s" % thats_something.search(data.text).group(2)),
        # You're <blank>
        (lambda data: youre_something.search(data.text), lambda: "No, you're %s!!" % youre_something.search(data.text).group(2)),
        # Childish. References to poop things
        (lambda data: any(word in ['poop', 'turd'] for word in data.text.split(' ')), lambda: ":poop:"),
        # if someone talks about Seattle
        (lambda data: "seattle" in data.text.lower(), lambda: ":space-needle: <--- Seattle"),
        # If someone just says hello
        (lambda data: 'hello' in data.text.lower() and data.user == 'U12D20DCP', lambda: "Traduccion: Hola."),
        # Did someone say snackatizer??
        (lambda data: "snack" in data.text, lambda: "Mayhaps mean snackatizer???"),
        # Myth busted
        (lambda data: myth_busted.search(data.text), lambda: random.choice(myth_busted_phrases)),
        # Wat dis is?
        (lambda data: watdisis.search(data.text), lambda: "YOU KNOW WAT DIS IS"),
        # If something isn't real
        (lambda data: arentreal.search(data.text), lambda: "You're not real."),
        # Boom, roasted
        (lambda data: data.text.lower() == 'boom', lambda: "Roasted"),
    ])

    rules.add_many_inclusive([
        (test_smarx, say_smarx_and_reset),
        # Translate Raymuno mas casas
        # (lambda data: data.user == SlackUsers.raymundo and not SlackUsers.ryan.at.is_in(data.text), lambda: "Translation: %s" % translate(data.text)),
        # Party pooper
        (lambda data: 'party' in data.text.lower(), lambda: "More like party pooper. lawl"),
        # Smarx was president of the juggling club
        (lambda data: 'juggl' in data.text.lower(), lambda: "Did you know %s was president of his juggling club in school?" % SlackUsers.smarx.at),
        # WAHH
        (lambda data: random.random() < 0.02, lambda: random.choice(phteven_phrases)),
        # As it were
        (lambda data: 'as it were' in data.text.lower(), lambda: "Pindeed"),
        # I hardly knew her
        (lambda data: baylor.search(data.text), lambda: "%s, I hardly know her" % baylor.search(data.text).group(1)),
        # Be quiet, zeebz
        (lambda data: (data.user == u'U04JH6A3N' or data.user == 'U12EQ7BEZ') and random.random() < 0.08, lambda: "Shut up, Zeebz"),
        # Raymundo Mascasas
        (lambda data: data.user == u'U12D20DCP' and random.random() < 0.09, lambda: "QUE??"),
        # Foldable bluetooth keyboard
        (lambda data: 'foldable bluetooth keyboard' in data.text.lower(), lambda: "You're a foldable bluetooth keyboard"),
        # Giphy
        (lambda data: data.text.startswith('/giphy') and random.random() < 0.50, lambda: random.choice(giphy_phrases)),
        # Hello
        (lambda data: 'hello' in data.text.lower() ,lambda: "Oh. Hello."),
    ])

    processor = PhtevenProcessor(rules)
    outputs.extend(processor.process())
