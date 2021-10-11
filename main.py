import discord
import requests

client = discord.Client()
# TODO Remove api key
googleUrl = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=YOUR API KEY"  # Google LookUp API Key


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    urls = message.content
    urls = urls[urls.find("http"):]
    author = str(message.author)
    if urls.find(" ") != -1:
        urls = urls[0: urls.find(" ")]

    check_url_resp = check_url(urls)

    if urls.find("http") != -1 and urls.find("!SafeLinkBot") == -1:
        if check_url_resp != "Safe":
            await message.channel.send("The following link " + urls + " posted by, " + author + ", is considered "
                                       "to unsafe because Google's LookUp API labels it as, " + check_url_resp + ".")

    if message.content.lower().startswith("!safelinkbot"):
        check_url_resp = check_url(urls)
        if check_url_resp == "Safe":
            await message.channel.send("The following link " + urls + " posted by, " + author + " is considered to be "
                                        "safe by Google's LookUp API.")
        else:
            await message.channel.send("The following link " + urls + " posted by, " + author + ", is considered "
                                       "to unsafe because Google's LookUp API labels it as, " + check_url_resp + ".")


# TODO remove api keys
def check_url(url):
    api_key = ""  # Google LookUp API Key
    payload = {'client': {'clientId': "SafeLinkBot", 'clientVersion': "0.1"},
               'threatInfo': {'threatTypes': ["SOCIAL_ENGINEERING", "MALWARE"],
                              'platformTypes': ["ANY_PLATFORM"],
                              'threatEntryTypes': ["URL"],
                              'threatEntries': [{'url': url}]}}
    params = {'key': api_key}
    r = requests.post(googleUrl, params=params, json=payload)
    if len(r.text) < 5:
        return "Safe"
    else:
        return r.json()["matches"][0]["threatType"]


client.run('')  # Discord Bot Token
