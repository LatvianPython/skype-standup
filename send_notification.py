from skpy import Skype
from skpy import SkypeAuthException
from getpass import getpass
import json
import keyring

service_name = 'skype-standup'

# see conf_example.json
with open('conf.json', mode='r', encoding='utf-8') as file:
    config = json.loads(file.read())
    username = config['username']

# todo: implement check on if during script execution we are connected to the internal network

password = keyring.get_password(service_name, username)

if password is None:  # if script is run the first time for specific username then you must register password
    keyring.set_password(service_name, username, getpass('Input Skype password for {}: '.format(username)))
    password = keyring.get_password(service_name, username)

token_file = '{}.token'.format(username)

sk = Skype(connect=False)
sk.conn.setTokenFile(token_file)
try:
    sk.conn.readToken()
except SkypeAuthException as e:
    # Old token, log into skype to obtain fresh one
    sk.conn.setUserPwd(username, password)
    sk.conn.getSkypeToken()

chat = sk.chats[config['target_chat']]

chat.sendMsg(config['message_text'])
