from collections import defaultdict

EMOJI_MAPPING = {
    '+1': '👍',
    '-1': '👎',
    'coeur': '🧡',
    'rire': '😂'
}

VALID_REACTIONS = {'+1', '-1', 'coeur', 'rire'}

class ReactionsManager(object):
    def __init__(self):
        # self.reactions = {
        #   123: {
        #     '+1': ['flo', 'quentin']
        #   }
        #   124: {
        #     '-1': ['flo', 'quentin'],
        #     'coeur': ['flo']
        #   }
        # }
        self.reactions = defaultdict(lambda: defaultdict(list))
    
    def add_reaction(self, msg_id, emetteur, reaction):
        if reaction not in VALID_REACTIONS:
            raise Exception("La reaction '%s' n'existe pas. Veuillez utiliser '%s'" % (reaction, str(VALID_REACTIONS)))
        current_authors_for_emoji_and_msg = self.reactions[msg_id][reaction]

        if emetteur not in current_authors_for_emoji_and_msg:
            current_authors_for_emoji_and_msg.append(emetteur)
    
    def get_reactions(self, msg_id):
        return self.reactions[msg_id]