from time import sleep
import random
from cacher import Cacher

from phteven_helper import (
    Data,
    PhtevenProcessor,
    PhtevenRules,
    PhtevenPhrases,
    PhtevenRegex,
    SlackUsers,
)

crontable = []
outputs = []


def say_smarx_and_reset():
    to_say = Cacher.get_smarx_message()
    Cacher.reset_smarx_messages()
    return to_say


def test_smarx(_):
    return len(Cacher.get_smarx_messages()) >= 10


def process_message(data):
    print "process message", data
    data = Data(**data)
    # Be quiet for a while man....
    if SlackUsers.phteven.at in data.text and 'shhh' in data.text.lower():
        print "Shhhhhhhhhh........"
        sleep(5 * 60)
        return
    if SlackUsers.smarx == data.user:
        Cacher.add_smarx_message(data.text)

    # We don't care what Phteven Marquarst says
    if data.user == SlackUsers.phteven:
        return

    rules = PhtevenRules(data)

    rules.add_many_exclusive([

        # If @Phteven gets mentioned
        (
            lambda data: SlackUsers.phteven.at in data.text,
            lambda: "^ %s" % SlackUsers.stephen.at
        ),
        # NO EDITING
        (
            lambda data: data.subtype == u'message_changed',
            lambda: "I SAW THAT.\n\n> %s" % data.previous_message['text']
        ),
        # Copy smarx
        (
            lambda data: random.random() < 0.05 and data.user == "U04TR0MSC",
            lambda: data.text
        ),
        # Smarx has an elipsis
        (
            lambda data: u"\u2026" in data.text and data.user == "U04TR0MSC",
            lambda: "Nice try, Steven J Smarx"
        ),
        # Are we in burgertory?
        (
            lambda data: 'burgertory' in data.text.lower() or 'burgatory' in data.text.lower(),
            lambda: "We're always in burgertory"
        ),
        # Ask Zeebs what he thinks if no one else knows
        (
            lambda data: 'no idea' == data.text.lower(),
            lambda: "<@U04JH6A3N>, what do you think?"
        ),
        # Zeebs trying to be funny
        (
            lambda data: PhtevenRegex.thats_something.search(data.text) and data.user == SlackUsers.dxm,
            lambda: "Shut up, Zeebs"
        ),
        # Am i saying meow?
        (
            lambda data: PhtevenRegex.meow_now.search(data.text),
            lambda: "Right meow?"
        ),
        # That's <blank>
        (
            lambda data: PhtevenRegex.thats_something.search(data.text),
            lambda: "You're %s" % PhtevenRegex.thats_something.search(data.text).group(2)
        ),
        # You're <blank>
        (
            lambda data: PhtevenRegex.youre_something.search(data.text),
            lambda: "No, you're %s!!" % PhtevenRegex.youre_something.search(data.text).group(2)
        ),
        # Childish. References to poop things
        (
            lambda data: any(word in ['poop', 'turd'] for word in data.text.split(' ')),
            lambda: ":poop:"
        ),
        # if someone talks about Seattle
        (
            lambda data: "seattle" in data.text.lower(),
            lambda: ":space-needle: <--- Seattle"
        ),
        # If someone just says hello
        (
            lambda data: 'hello' in data.text.lower() and data.user == 'U12D20DCP',
            lambda: "Traduccion: Hola."
        ),
        # Did someone say snackatizer??
        (
            lambda data: "snack" in data.text,
            lambda: "Mayhaps mean snackatizer???"
        ),
        # Myth busted
        (
            lambda data: PhtevenRegex.myth_busted.search(data.text),
            lambda: random.choice(PhtevenPhrases.myth_busted_phrases)
        ),
        # What dis is?
        (
            lambda data: PhtevenRegex.whatdisis.search(data.text),
            lambda: "YOU KNOW WHAT DIS IS"
        ),
        # If something isn't real
        (
            lambda data: PhtevenRegex.arentreal.search(data.text),
            lambda: "You're not real."
        ),
        # Boom, roasted
        (
            lambda data: data.text.lower() == 'boom',
            lambda: "Roasted"
        ),
    ])

    rules.add_many_inclusive([
        # That's what she said
        (
            lambda data: "harder" in data.text,
            lambda: "That's what she said"
        ),
        # Say what smarx said...but a while ago
        (
            test_smarx,
            say_smarx_and_reset
        ),
        # Party pooper
        (
            lambda data: 'party' in data.text.lower(),
            lambda: "More like party pooper. lawl"
        ),
        # Smarx was president of the juggling club
        (
            lambda data: 'juggl' in data.text.lower(),
            lambda: "Did you know %s was president of his juggling club in school?" % SlackUsers.smarx.at
        ),
        # WAHH
        (
            lambda data: random.random() < 0.02,
            lambda: random.choice(PhtevenPhrases.phteven_phrases)
        ),
        # As it were
        (
            lambda data: 'as it were' in data.text.lower(),
            lambda: "Pindeed"
        ),
        # I hardly knew her
        (
            lambda data: PhtevenRegex.baylor.search(data.text),
            lambda: "%s, I hardly know her" % PhtevenRegex.baylor.search(data.text).group(1)
        ),
        # Be quiet, zeebz
        (
            lambda data: (data.user == u'U04JH6A3N' or data.user == 'U12EQ7BEZ') and random.random() < 0.08,
            lambda: "Shut up, Zeebz"
        ),
        # Raymundo Mascasas
        (
            lambda data: data.user == u'U12D20DCP' and random.random() < 0.09,
            lambda: "QUE??"
        ),
        # Foldable bluetooth keyboard
        (
            lambda data: 'foldable bluetooth keyboard' in data.text.lower(),
            lambda: "You're a foldable bluetooth keyboard"
        ),
        # Giphy
        (
            lambda data: data.text.startswith('/giphy') and random.random() < 0.50,
            lambda: random.choice(PhtevenPhrases.giphy_phrases)
        ),
        # Hello
        (
            lambda data: 'hello' in data.text.lower(),
            lambda: "Oh. Hello."
        ),
    ])

    processor = PhtevenProcessor(rules)
    outputs.extend(processor.process())
