from box import Box
from tassi.telegram_bot.bot import parser

class Update:

    def __init__(self, message, update=False):

        self.message = None
        self.edited_message = None

        if not update:
            self.message = Box(message)
        else:
            self.edited_message = Box(message)

fake_data = [
    {'message_id': 38, 'date': 1601223659, 'chat': {'id': 941270, 'type': 'private', 'username': 'Yabir', 'first_name': 'Yabir', 'last_name': 'Garcia'}, 'edit_date': 1601223699, 'entities': [], 'caption_entities': [], 'photo': [], 'location': {'longitude': -3.607837, 'latitude': 37.220822}, 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 941270, 'first_name': 'Yabir', 'is_bot': False, 'last_name': 'Garcia', 'username': 'Yabir', 'language_code': 'en'}},
    {'message_id': 38, 'date': 1601223659, 'chat': {'id': 941270, 'type': 'private', 'username': 'Yabir', 'first_name': 'Yabir', 'last_name': 'Garcia'}, 'edit_date': 1601223671, 'entities': [], 'caption_entities': [], 'photo': [], 'location': {'longitude': -3.607756, 'latitude': 37.220848}, 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 941270, 'first_name': 'Yabir', 'is_bot': False, 'last_name': 'Garcia', 'username': 'Yabir', 'language_code': 'en'}},
    # Not updates
    {'message_id': 38, 'date': 1601223659, 'chat': {'id': 941270, 'type': 'private', 'username': 'Yabir', 'first_name': 'Yabir', 'last_name': 'Garcia'}, 'entities': [], 'caption_entities': [], 'photo': [], 'location': {'longitude': -3.60784, 'latitude': 37.220865}, 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 941270, 'first_name': 'Yabir', 'is_bot': False, 'last_name': 'Garcia', 'username': 'Yabir', 'language_code': 'en'}}
]

def test_mock_update():

    update = Update(fake_data[0], True)

    result = parser(update.edited_message)

    assert(result[0] == 38)
    assert(result[1] == 941270)
    assert sorted(result[2].items()) == sorted({'longitude': -3.607837, 'latitude': 37.220822, 'datetime': 1601223699}.items())

def test_mock_first_message():
    
    update = Update(fake_data[2], False)

    result = parser(update.message)

    assert(result[0] == 38)
    assert(result[1] == 941270)
    assert sorted(result[2].items()) == sorted({'longitude': -3.60784, 'latitude': 37.220865, 'datetime': 1601223659}.items())
    