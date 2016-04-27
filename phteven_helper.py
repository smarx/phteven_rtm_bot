class Data(object):
    def __init__(self, user='', subtype=None, text='', **kwargs):
        self.text = text
        self.user = user
        self.subtype = subtype
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


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
        self._complete = False
        self.outputs = []

    def is_complete(self):
        return self._is_complete

    def process(self):
        for rule in self.exclusive_rules:
            if rule.check_rule():
                self.outputs.append(rule.output)
                break
        for rule in self.inclusive_rules:
            if rule.check_rule():
                self.outputs.append(rule.output)
        return self.outputs


#subclass string not object
class SlackUser(object):
    def __init__(self, user):
        self.user = user

    @property
    def at(self):
        return SlackUser("<@%s>" % self.user)

    def is_in(self, s):
        return self.user in s

    def __repr__(self):
        return self.user

    def __str__(self):
        return self.user

    def __eq__(self, cmp):
        return self.user == cmp

    def __contains__(self, cmp):
        return cmp in self.user


class SlackUsers:
    zeebz = SlackUser('U12EQ7BEZ')
    dxm = SlackUser('U04JH6A3N')
    phteven = SlackUser('U0Y8YJCBU')
    smarx = SlackUser('U04TR0MSC')
    stephen = SlackUser('U04FX9RJT')
    raymundo = SlackUser('U12D20DCP')
    ryan = SlackUser('U03TULSM8')

