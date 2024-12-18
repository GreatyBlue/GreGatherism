import requests
import instaloader
from googleapiclient.discovery import build
import discord
import asyncio

# Instagram Info Gathering
def get_instagram_info(username):
    loader = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        print(f"Instagram Username: {profile.username}")
        print(f"Name: {profile.full_name}")
        print(f"Followers: {profile.followers}")
        print(f"Following: {profile.followees}")
        print(f"Bio: {profile.biography}")
        print(f"Posts: {profile.mediacount}")
    except Exception as e:
        print(f"Error fetching Instagram info for {username}: {e}")

# Facebook Info Gathering (Requires Access Token)
def get_facebook_info(page_id, access_token):
    url = f"https://graph.facebook.com/{page_id}?fields=id,name,followers_count,posts&access_token={access_token}"
    try:
        response = requests.get(url)
        data = response.json()
        print(f"Facebook Page Name: {data['name']}")
        print(f"Followers: {data['followers_count']}")
        print(f"Recent Posts: {data['posts']['data'][:3]}")  # Display 3 recent posts
    except Exception as e:
        print(f"Error fetching Facebook info for {page_id}: {e}")

# YouTube Info Gathering (Requires API Key)
def get_youtube_info(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_id)
        response = request.execute()
        channel = response['items'][0]
        print(f"YouTube Channel Name: {channel['snippet']['title']}")
        print(f"Subscribers: {channel['statistics']['subscriberCount']}")
        print(f"Videos: {channel['statistics']['videoCount']}")
    except Exception as e:
        print(f"Error fetching YouTube info for {channel_id}: {e}")

# Discord Info Gathering (Requires Bot Token and Guild ID)
async def get_discord_info(token, guild_id):
    client = discord.Client()

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            print(f"Discord Guild Name: {guild.name}")
            print(f"Total Members: {guild.member_count}")
            print(f"Channels: {[channel.name for channel in guild.channels]}")
        else:
            print("Guild not found.")
        await client.close()

    client.run(token)

# Main function to gather info from selected platform
def main():
    platform = input("Enter platform (Instagram, Facebook, YouTube, Discord): ").lower()

    if platform == "instagram":
        username = input("Enter Instagram username: ")
        get_instagram_info(username)
    
    elif platform == "facebook":
        page_id = input("Enter Facebook page ID: ")
        access_token = input("Enter your Facebook access token: ")
        get_facebook_info(page_id, access_token)
    
    elif platform == "youtube":
        api_key = input("Enter YouTube API key: ")
        channel_id = input("Enter YouTube channel ID: ")
        get_youtube_info(api_key, channel_id)
    
    elif platform == "discord":
        token = input("Enter Discord bot token: ")
        guild_id = int(input("Enter Discord guild ID (server ID): "))
        asyncio.run(get_discord_info(token, guild_id))
    
    else:
        print("Platform not supported!")

if __name__ == "__main__":
    main()
