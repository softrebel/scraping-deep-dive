url='https://host1.rj-mw1.com/media/{url}.mp3'

import requests

while True:
    inp=input('enter url: ')

    x=requests.get(url.format(url=inp))
    name=inp.split('/')[-1]
    with open(f'music/{name}.mp3','wb') as f:
        f.write(x.content)
    print('done')