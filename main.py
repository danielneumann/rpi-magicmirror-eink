#!/usr/bin/env python3
import asyncio
import logging
import tempfile
import argparse
import sys
from time import sleep
import numpy as np
from aiocron import crontab
from pyppeteer import launch
from PIL import Image
from IT8951 import constants
from IT8951.display import AutoEPDDisplay



# TODO fix ignored KeyboardInterrupt when running in the the event loop (run_forever)
# TODO implement proper reset and shutdown of the screen when the systemd service is stopped or the raspberry pi is shut down
# TODO maybe a "last updated" time (just a clock module with a different header)

# Import the waveshare folder (containing the waveshare display drivers) without refactoring it to a module
# TODO maybe switch to a git submodule here and upgrade to the latest version:
# https://github.com/waveshare/e-Paper/blob/master/RaspberryPi%26JetsonNano/python/lib/waveshare_epd/epd7in5bc.py
#sys.path.insert(0, './waveshare')
sys.path.insert(0, './IT8951')
# import epd7in5b
#import epd9in7


# Global config
display_width = 1200		# Width of the display
display_height = 825		# Height of the display
is_portrait = False		# True of the display should be in landscape mode (make sure to adjust the width and height accordingly)
wait_to_load = 60		# Page load timeout
wait_after_load = 18		# Time to evaluate the JS afte the page load (f.e. to lazy-load the calendar data)
url = 'http://localhost:8080'	# URL to create the screenshot of

def reset_screen():
    logging.info('Reset Screen.')
    display = AutoEPDDisplay(vcom=-2.06)
    display.clear()

@asyncio.coroutine
def create_screenshot(file_path):
    global display_width
    global display_height
    global wait_to_load
    global wait_after_load
    global url
    logging.debug('Creating screenshot')
    browser = yield launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--headless', '--disable-gpu', '--disable-dev-shm-usage'], executablePath='/usr/bin/chromium-browser')
    page = yield browser.newPage()
    yield page.setViewport({
        "width": display_width,
        "height": display_height
    })
    yield page.goto(url, timeout=wait_to_load * 1000)
    yield page.waitFor(wait_after_load * 1000)
    yield page.screenshot({'path': file_path})
    yield browser.close()
    logging.debug('Finished creating screenshot')

@asyncio.coroutine
def refresh():
    logging.info('Starting refresh.')

    logging.info('Init Display.')
    display = AutoEPDDisplay(vcom=-2.06)
    dims = (display.width, display.height)

    with tempfile.NamedTemporaryFile(suffix='.png') as tmp_file:
        logging.debug('Created temporary file at {tmp_file.name}.')
        yield create_screenshot(tmp_file.name)
        logging.debug('Opening screenshot.')
        image = Image.open(tmp_file)

        # Rotate the image by 90°
        if is_portrait:
           logging.debug('Rotating image (portrait mode).')
           image = image.rotate(90)
        logging.debug('Sending image to screen.')

        image.thumbnail(dims)
        paste_coords = [dims[i] - image.size[i] for i in (0,1)]  # align image with bottom of display
        display.frame_buf.paste(image, paste_coords)
        display.draw_full(constants.DisplayModes.GC16)

    logging.info('Refresh finished.')


def main():

    try:
        parser = argparse.ArgumentParser(description='Python EInk MagicMirror')
        parser.add_argument('-d', '--debug', action='store_true', dest='debug',
                            help='Enable debug logs.', default=False)
        parser.add_argument('-c', '--cron', action='store', dest='cron',
                            help='Sets a schedule using cron syntax')
        parser.add_argument('-r', '--reset', action='store_true', dest='reset',
                            help='Ignore all other settings and just reset the screen.', default=False)
        args = parser.parse_args()
        level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(level=level, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        if not args.reset:
            if args.cron:
                logging.info('Scheduling the refresh using the schedule "{args.cron}".')
                crontab(args.cron, func=refresh)
                # Initially refresh the display before relying on the schedule
                asyncio.get_event_loop().run_until_complete(refresh())
                asyncio.get_event_loop().run_forever()
            else:
                logging.info('Only running the refresh once.')
                asyncio.get_event_loop().run_until_complete(refresh())
    except KeyboardInterrupt:
        logging.info('Shutting down after receiving a keyboard interrupt.')
    finally:
        logging.info('Resetting screen.')
        reset_screen()


if __name__ == '__main__':
    main()
