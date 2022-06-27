import requests

if __name__ == "__main__":

    previous_index = 70000000
    index = 70000000

    while True:
        print('index: ' + str(index))
        url = 'https://www.kurnik.pl/p/?g=sc' + str(index) +'.txt'
        r = requests.get(url = url)
        if (not r.ok or len(r.content.decode()) == 0):
            previous_index = index
            index += 10000
        else:
            break

    bottom_index = previous_index
    up_index = index

    while bottom_index != up_index:
        index = int((bottom_index + up_index)/2)
        print('index: ' + str(index))
        url = 'https://www.kurnik.pl/p/?g=sc' + str(index) +'.txt'
        r = requests.get(url = url)
        if (not r.ok or len(r.content.decode()) == 0):
            bottom_index = index + 1
        else:
            up_index = index




    URL = 'https://www.kurnik.pl/p/?g=sc' + str(index) + '.txt'

    rs = requests.get(url = URL)
    r = rs.content.decode()

    print(r.split('\n')[6])

    for s in r.split('\n')[12:]:
        print(s)

    print(len(r))
