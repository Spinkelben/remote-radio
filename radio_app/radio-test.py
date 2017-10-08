from internet_stream_player import InternetStreamPlayer
from request_handler import RequestHandler
from command_server import CommandServer
import time
import logging
import argparse

def main(args):
    log_level = logging.WARNING
    if args.log_level:
        if args.log_level == "DEBUG":
            log_level = logging.DEBUG
        elif args.log_level == "INFO":
            log_level = logging.INFO
        elif args.log_level == "WARNING":
            log_level = logging.WARNING
        elif args.log_level == "ERROR":
            log_level = logging.ERROR

    logging.basicConfig(level=log_level)

    #our stream to play
    #music_stream_uri = 'http://live-icy.gss.dr.dk/A/A29L.mp3'
    music_stream_uri = 'http://live-icy.gss.dr.dk/A/A29H.mp3'
    all_stations = [
        ('Radio-Klassisk-900-', 'http://onair.100fmlive.dk/klassisk_live.mp3'),
        ('Radio-Odsherred-1079-', 'https://stream.radiotime.com/listen.stream?streamId=9170729&rti=dEZzGgYzfxg4dhE2AxFRSGgyQE5RdicUC1cCEwQcSAwTRkR0%7e%7e%7e&render=json&qs=eQQxTw9daF0GURF5RA%3d%3d%7e%7e%7e'),
        ('Retro-Radio-Millennium-', 'http://tx-2.retro-radio.dk/TX-2'),
        ('Radio-Alborz--Persian-', 'http://live.indvandrerradio.dk:8000'),
        ('Retro-radio-jul-', 'http://isstream.kanalplus.fm/TX-1'),
        ('Radio-Vesterbro-989-', 'http://185.80.220.12:8006/live'),
        ('DR-Ramasjang-Ultra-', 'http://live-icy.gss.dr.dk:8000/A/A24H.mp3'),
        ('DR-P3-939-', 'https://stream.radiotime.com/listen.stream?streamId=40690612&rti=dEZzGgYzfxg4dhE2AxFRSGgyQE5RdicUC1cCEwQcSAwTRkR0%7e%7e%7e&render=json&qs='),
        ('Radio-Halsns-1053-', 'http://45.32.238.225:80'),
        ('Yes2day-Radio-889-', 'rtmp://krykeypremium1.com/RadioDispatcher/53905/dj1'),
        ('Radio-Projekti-21-1029-', 'http://64.150.176.42:8178/'),
        ('myROCK-927-', 'http://stream.myrock.fm/myrock128'),
        ('Radioti-929-', 'http://radioti.serverroom.us:6906'),
        ('CopenhagenFM-1059-', 'http://stream.wlmm.dk/copenhagenfm'),
        ('Global-FM-982-', 'http://stream.radiosolutions.dk:60040/global'),
        ('Radio-Ballerup-902-', 'http://stream.vibestream.dk:8010/stream'),
        ('Radio-Humleborg-1043-', 'http://media.wlmm.dk/humleborg'),
        ('Rockkanalen-', 'http://stream.kanalplus.fm/kp128'),
        ('Radio-Kultur-977-', 'https://stream.radiotime.com/listen.stream?streamId=74968802&rti=dEZzGgYzfxg4dhE2AxFRSGgyQE5RdicUC1cCEwQcSAwTRkR0%7e%7e%7e&render=json&qs='),
        ('Radio-Nord-FM-986-', 'https://stream.radiotime.com/listen.stream?streamId=61461135&rti=dEZzGgYzfxg4dhE2AxFRSGgyQE5RdicUC1cCEwQcSAwTRkR0%7e%7e%7e&render=json&qs=')]
    player = InternetStreamPlayer(music_stream_uri)
    handler = RequestHandler(player)


    with CommandServer(address='/tmp/radio-sock', action=handler.on_message), player:
        try:
            while True:
                choice = input('(S)top, (P)lay, P(a)use, (C)hange Station and (Q)uit')
                choice = str(choice)
                if choice.lower() == 's':
                    player.stop()
                elif choice.lower() == 'p':
                    player.play()
                elif choice.lower() == 'a':
                    player.pause()
                elif choice.lower() == 'c':
                    print("Select station by pressing the number")
                    for idx, station in enumerate(all_stations):
                        print("Press {} for {}".format(idx, station[0]))
                    number = input("Select station by pressing the number: ")
                    url = None
                    try:
                        number = int(number)
                        url = all_stations[number][1]
                    except Exception as e:
                        print("Did not understand number. Error '{}'".format(e))
                    if url is not None:
                        player.stop()
                        player.set_url(url)
                        player.play()
                elif choice.lower() == 'q':
                    exit(0)
                else:
                    print("Did not understand command {}".format(choice))
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], required=False)
    args = parser.parse_args()
    main(args)
