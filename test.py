from requests import Response
from typing import Tuple

import requests

def get_content(index : int) -> Response:
    url = f"https://www.kurnik.pl/p/?g=sc{str(index)}.txt"
    return requests.get(url = url)

def is_valid_response(response : Response) -> bool:
    return response.ok and response.content.decode()

def find_valid_range() -> Tuple[int, int]:
    previous_index = 70000000
    index = 70000000

    while True:
        response = get_content(index)
        if (is_valid_response(response)):
            break
        else:
            previous_index = index
            index += 10000
    
    return previous_index, index


def find_first_valid(bottom_index : int, up_index : int) -> int:
    while bottom_index < up_index:
        index = int((bottom_index + up_index)/2)
        response = get_content(index)
        if (is_valid_response(response)): 
            up_index = index
        else:
            bottom_index = index + 1
    return bottom_index

if __name__ == "__main__":

    bottom_index, up_index = find_valid_range()
    index = find_first_valid(bottom_index, up_index)
    
    response_string = get_content(index).content.decode()

    print(response_string.split('\n')[6])

    for s in response_string.split('\n')[12:]:
        print(s)