import argparse
import logging
import time

from simulation_components.main_actor import MainActor


def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-t', '--time', type=int, default=10, required=False)
    return parser.parse_args()


def app():
    logger = logging.getLogger('app')

    import sys
    print(sys.path)
    logger.info('starting simulation...')
    args = parse()
    MainActor.start(args.file).proxy()
    logger.info('started simulation')
    time.sleep(args.time)
    logger.info('stopping simulation...')
    MainActor.get_instance_proxy().stop()
    logger.info('simulation stopped')


if __name__ == '__main__':
    app()
