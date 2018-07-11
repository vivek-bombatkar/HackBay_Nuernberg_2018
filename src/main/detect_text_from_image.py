"""
Example Usage:
python detect.py text ./resources/wakeupcat.jpg

For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io
import os

from google.cloud import vision
import datetime
import time


def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    file_name = "data_file.csv"
    if os.path.exists(file_name):
        apprnt_or_write = "a"
    else:
        apprnt_or_write = "w"

    data_file = open(file_name,apprnt_or_write)
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    for text in texts:
        text_captured = ""
        for line in text.description.splitlines():
            text_captured += ";" + line

        data_file.write('{}{}\n'.format(current_time,text_captured))
        break



def detect_text_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


def run_local(args):
    if args.command == 'text':
        detect_text(args.path)


def run_uri(args):
    if args.command == 'text-uri':
        detect_text_uri(args.uri)
if __name__ == '__main__':

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\VIVEK\GIT\google_credentials\testProj_1-2aad0580e81d.json"

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    detect_text_parser.add_argument('path')

    text_file_parser = subparsers.add_parser(
        'text-uri', help=detect_text_uri.__doc__)
    text_file_parser.add_argument('uri')

    args = parser.parse_args()

    if 'uri' in args.command:
        run_uri(args)
    else:
        run_local(args)