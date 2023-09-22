# python -m pip install segno
# python -m pip install pillow qrcode-artistic

import segno
from urllib.request import urlopen

github_qrcode = segno.make_qr('https://github.com/uktukt')
github_gif = urlopen('https://media4.giphy.com/media/dxn6fRlTIShoeBr69N/giphy.gif?cid'
                     '=ecf05e47497lbmz9qmicifcn6vx44uu05jicqehx5ia4x4n4&ep=v1_gifs_search'
                     '&rid=giphy.gif&ct=g')
github_qrcode.to_artistic(
    background=github_gif,
    target='github_qrcode2.gif',
    scale=5,
    light='white',
    dark='darkgreen'
)

linkedin_qrcode = segno.make_qr('https://www.linkedin.com/in/dovile-meskauskaite-5a0a3967/')
linkedin_gif = urlopen('https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY201ZzIzd2t5d3o1OWU'
                       'xYTB5dm15azFmenQ2Y2U3YmVxZXlzNWJmMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQm'
                       'Y3Q9Zw/TJP7EH5i1fB2rKeWbf/giphy.gif')
linkedin_qrcode.to_artistic(
    background=linkedin_gif,
    target='linkedin_qrcode.gif',
    scale=5,
    light='white',
    dark='blue'
)
