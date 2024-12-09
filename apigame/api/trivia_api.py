import requests

class TriviaAPI:
    def __init__(self):
        pass

    token_url = "https://opentdb.com/api_token.php?command=request"
    token_response = requests.get(token_url).json()

    # Extract the token
    token = token_response.get("token")
    print(f"Session Token: {token}")

    # Include the token in your API call
    url_with_token = f"https://opentdb.com/api.php?amount=10&token={token}"
    response = requests.get(url_with_token)
    data = response.json()

    # Handle token exhaustion
    if data.get("response_code") == 4:  # Code 4: Token Empty
        print("Token exhausted. Resetting token...")
        reset_url = f"https://opentdb.com/api_token.php?command=reset&token={token}"
        reset_response = requests.get(reset_url).json()
        print(reset_response)
    else:
        print(data)

    category_url = "https://opentdb.com/api_category.php"
    categories = requests.get(category_url).json()

    # Display all categories
    for category in categories["trivia_categories"]:
        print(f"ID: {category['id']}, Name: {category['name']}")