import os

if os.environ.get('MODE') == 'dev':
    print("Reload True")
    reload = True

print("Test", os.path.dirname(os.path.realpath(__file__)))

bind = '0.0.0.0:80'
