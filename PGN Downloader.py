import asyncio
from chessdotcom.aio import get_player_games_by_month, get_player_game_archives, Client
Client.aio = True
async def gather_cors(cors):
    responses = await asyncio.gather(*cors)
    return responses
def PGNcreator(response, username, file_path):
    response_data = response.json
    games = response_data['games']
    for game in games:
        pgn = game['pgn']
        with open(file_path, 'a') as file:
            file.write(pgn + "\n\n")  # Add newline between games
async def main(usernames, file_path):
    cors = [get_player_game_archives(username) for username in usernames]
    responses = await gather_cors(cors)
    for response, username in zip(responses, usernames):
        archives_urls = response.json['archives']
        for link in archives_urls:
            year = link[-7:-3]
            month = link[-2:]
            cors = [get_player_games_by_month(username, year, month)]
            monthly_responses = await gather_cors(cors)
            for monthly_response in monthly_responses:
                PGNcreator(monthly_response, username, file_path)
def usernamesGetting():
    usernames = []
    print("How do you want to give the usernames?")
    numberOfUsername = input("[1] Input into cmd\n[2] Give file\n")
    if (numberOfUsername == "1"):
        amountOfUsernames = int(input("How many usernames do you want to give?\n"))
        for x in range(amountOfUsernames):
            usernames.append(input(f"Username {x+1}:"))
        return usernames
    elif (numberOfUsername == '2'):
        location = input("What is the location of the text file?\n")
        seperator = input("What character seperates the usernames?\n")
        with open(location.strip("'\""), 'r') as file:
            accounts = file.readlines()
        for account in accounts:
            acount_data = account.strip().split(seperator)
            usernames.extend(acount_data)
        return usernames
if __name__ == "__main__":
    usernames = usernamesGetting()
    output_file_path = "games.pgn"
    with open(output_file_path, 'w') as file:
        file.write("")  # Initialize the file
    asyncio.run(main(usernames, output_file_path))
