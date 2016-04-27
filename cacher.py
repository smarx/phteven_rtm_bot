import datetime
import json
import os

from phteven_helper import SlackUsers

'''
This is a lazy way to save state. This should be made **way** better in the future.
I just wanted to get this out the door and have a way to keep track of what we've seen.
'''

now = datetime.datetime.now()


class Cacher(object):
    STATE_FILE = os.path.join(os.path.dirname(__file__), 'cacher.json')

    @staticmethod
    def load_state():
        if not os.path.exists(Cacher.STATE_FILE):
            return {}
        try:
            f = open(Cacher.STATE_FILE, 'r')
            state = json.load(f)
            f.close()
            return state
        except ValueError:
            return {}

    @classmethod
    def add_smarx_message(cls, message):
        print "adding message to smarx sayings"
        state = cls.load_state()
        if str(SlackUsers.smarx) not in state:
            state[str(SlackUsers.smarx)] = []
        state[str(SlackUsers.smarx)].append(message)
        cls.save_state(state)

    @classmethod
    def reset_smarx_messages(cls):
        print "resetting smarx messages"
        state = cls.load_state()
        if str(SlackUsers.smarx) in state:
            state[str(SlackUsers.smarx)] = []
            cls.save_state(state)

    @classmethod
    def get_smarx_messages(cls):
        print "getting smarx messages"
        state = cls.load_state()
        if str(SlackUsers.smarx) not in state:
            state[str(SlackUsers.smarx)] = []
        cls.save_state(state)
        return cls.load_state()[str(SlackUsers.smarx)]

    @staticmethod
    def save_state(state):
        f = open(Cacher.STATE_FILE, 'w')
        json.dump(state, f, indent=4)
        f.close()
