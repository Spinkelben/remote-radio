from internet_stream_player import InternetStreamPlayer
from request_handler import RequestHandler
from command_server import CommandServer
import time
import logging
import os

def main():
    env_log_level = os.environ["LOGLEVEL"]
    log_level = logging.INFO
    print("Log level: {}".format(env_log_level))
    if env_log_level == "DEBUG":
        log_level = logging.DEBUG
    elif env_log_level == "INFO":
        log_level = logging.INFO
    elif env_log_level == "WARNING":
        log_level = logging.WARNING
    elif env_log_level == "ERROR":
        log_level = logging.ERROR
    logging.basicConfig(level=log_level)
    player = InternetStreamPlayer()
    handler = RequestHandler(player)
    with CommandServer(address='/var/sockets/radio-sock', action=handler.on_message), player:
        while True:
            # Keep the thread alive
            time.sleep(1)


if __name__ == "__main__":
    main()
