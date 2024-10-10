
import discord, requests, logging
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
UID = int(os.getenv('UID'))
CLIENT_ID = os.getenv('CLIENT_ID')
HA_TOKEN = os.getenv('HA_TOKEN')
HA_URL = os.getenv('HA_URL')
ENTITY_ID = os.getenv('ENTITY_ID')
DC_BOT_TOKEN = os.getenv('DC_BOT_TOKEN')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('info'):
        await message.channel.send('Hello!')

def send_request(action, data):

    url = f'{HA_URL}/api/services/light/{action}'
    headers = {
        'Authorization': f'Bearer {HA_TOKEN}',
        'content-type': 'application/json',
    }
    data['entity_id'] = ENTITY_ID

    response = requests.post(url, headers=headers, json=data)
    return response

def mic_on_indicator():
    data = {
        'brightness': 50,
        "xy_color": [
            0.2656,
            0.6282
        ],
    }
    response = send_request('turn_on', data)
    if response.status_code != 200:
        raise Exception('Failed to turn on light')
    return

def mic_off_indicator():
    data = {
        'brightness': 50,
        "xy_color": [
            0.674,
            0.320
        ],
    }
    response = send_request('turn_on', data)
    if response.status_code != 200:
        raise Exception('Failed to turn on light')
    return

def turn_off_indicator():
    response = send_request('turn_off', {})
    if response.status_code != 200:
        raise Exception('Failed to turn off light')
    return

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

    logger.debug(member)
    logger.debug(after)
    if member.id != UID:
        return

    if after.channel is None:
        turn_off_indicator()
    else:
        if after.self_mute:
            mic_off_indicator()
        else:
            mic_on_indicator()

logger = logging.getLogger('discord')

permission = discord.Permissions(permissions=33554432)
url = discord.utils.oauth_url(client_id=CLIENT_ID, permissions=permission)
print(url)
client.run(DC_BOT_TOKEN)
