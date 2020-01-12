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

def reset_screen(display):
    logging.info('Reset Screen.') 
    display.clear()

def display_gradient(display):
    print('Displaying gradient...')

    # set frame buffer to gradient
    for i in range(16):
        color = i*0x10
        box = (
            i*display.width//16,      # xmin
            0,                        # ymin
            (i+1)*display.width//16,  # xmax
            display.height            # ymax
        )
        
        display.frame_buf.paste(color, box=box)

    # update display
    display.draw_full(constants.DisplayModes.GC16)

async def create_screenshot(file_path):
    global display_width
    global display_height
    global wait_to_load
    global wait_after_load
    global url
    logging.debug('Creating screenshot')
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--headless', '--disable-gpu', '--disable-dev-shm-usage'], executablePath='/usr/bin/chromium-browser')
    page = await browser.newPage()
    await page.setViewport({
        "width": display_width,
        "height": display_height
    })
    await page.goto(url, timeout=wait_to_load * 1000)
    await page.waitFor(wait_after_load * 1000)
    await page.screenshot({'path': file_path})
    await browser.close()
    logging.debug('Finished creating screenshot')


async def refresh(display, dims):
    logging.info('Starting refresh.')

    with tempfile.NamedTemporaryFile(suffix='.png') as tmp_file:
        logging.debug('Created temporary file at {tmp_file.name}.')
        await create_screenshot(tmp_file.name)
        logging.debug('Opening screenshot.')
        image = Image.open(tmp_file)

        # Rotate the image by 90
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

    from IT8951.display import AutoEPDDisplay
    logging.info('Init Display.')
    display = AutoEPDDisplay(vcom=-2.06)
    dims = (display.width, display.height)

    reset_screen(display)
    sleep(1)
    display_gradient(display)
    sleep(1)
    reset_screen(display)
    sleep(1)
    refresh(display, dims)


if __name__ == '__main__':
    main()
