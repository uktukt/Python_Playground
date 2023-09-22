# python -m pip install segno
# python -m pip install pillow qrcode-artistic

import segno
from urllib.request import urlopen

github_qrcode = segno.make_qr('https://github.com/uktukt')
github_gif = urlopen('https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXpkcXV0Zn'
                     'FhNzF4ZXJwMGxmdmxid3VwcDZmZzIxbnhkcXVlNzhlNyZlcD12MV9pbnRlcm5'
                     'hbF9naWZfYnlfaWQmY3Q9Zw/du3J3cXyzhj75IOgvA/giphy.gif')
github_qrcode.to_artistic(
    background=github_gif,
    target='github_qrcode.gif',
    scale=5,
    light='white',
    dark='green'
)

linkedin_qrcode = segno.make_qr('https://www.linkedin.com/in/dovile-meskauskaite-5a0a3967/')
linkedin_gif = urlopen('https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY201ZzIzd2t5d3o1OWUxYTB5dm15azFmenQ2Y2U3YmVxZXlzNWJmMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TJP7EH5i1fB2rKeWbf/giphy.gif')
linkedin_qrcode.to_artistic(
    background=linkedin_gif,
    target='linkedin_qrcode.gif',
    scale=5,
    light='white',
    dark='blue'
)
