import re
import string


class Data(object):
    def __init__(self, user='', subtype=None, text='', **kwargs):
        self.text = text
        self.user = user
        self.subtype = subtype
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


class PhtevenPhrases(object):
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


class PhtevenRegex(object):
    thats_something = re.compile(ur"^that(\u2019|\')?s (.*)$", re.IGNORECASE)
    youre_something = re.compile(ur"^.*you(\u2019|\')?re? (\w+)$", re.IGNORECASE)
    myth_busted = re.compile(r"myth (busted|confirmed)", re.IGNORECASE)
    meow_now = re.compile(r'\bnow\b', re.IGNORECASE)

    only_hello = re.compile(r'[^A-Za-z0-9]')
    watdisis = re.compile(r'wh?at.*dis.*is', re.IGNORECASE)
    arentreal = re.compile(ur'aren(\'|\u2019)?t real', re.IGNORECASE)
    baylor = re.compile(r'(\w+(er|or))[%s]*$' % re.escape(string.punctuation), re.IGNORECASE)


class PhtevenLogic(object):
    def __init__(self, data, comparator, output):
        self.data = data
        self.comparator = comparator
        self._output = output
        self.processed = False

    @property
    def output(self):
        return [self.data.channel, self._output()]

    def check_rule(self):
        return self.comparator(self.data)


class PhtevenRules(object):
    def __init__(self, data):
        self.data = data
        self.exclusive = []
        self.inclusive = []

    def add_many_exclusive(self, rules):
        for rule in rules:
            self.add_exclusive(*rule)

    def add_exclusive(self, comparator, output):
        self.exclusive.append(PhtevenLogic(self.data, comparator, output))

    def add_many_inclusive(self, rules):
        for rule in rules:
            self.add_inclusive(*rule)

    def add_inclusive(self, comparator, output):
        self.inclusive.append(PhtevenLogic(self.data, comparator, output))


class PhtevenProcessor(object):
    def __init__(self, rules):
        self.exclusive_rules = rules.exclusive
        self.inclusive_rules = rules.inclusive
        self.outputs = []

    def process(self):
        for rule in self.exclusive_rules:
            if rule.check_rule():
                self.outputs.append(rule.output)
                break
        for rule in self.inclusive_rules:
            if rule.check_rule():
                self.outputs.append(rule.output)
        return self.outputs


class SlackUser(str):
    def __init__(self, user):
        self.user = user

    @property
    def at(self):
        return SlackUser("<@%s>" % self.user)


class SlackUsers(object):
    zeebz = SlackUser(u'U12EQ7BEZ')
    dxm = SlackUser(u'U04JH6A3N')
    phteven = SlackUser(u'U0Y8YJCBU')
    smarx = SlackUser(u'U04TR0MSC')
    stephen = SlackUser(u'U04FX9RJT')
    raymundo = SlackUser(u'U12D20DCP')
    ryan = SlackUser(u'U03TULSM8')
