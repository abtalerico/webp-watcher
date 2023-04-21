#!/usr/bin/env python
from PIL import Image
import inotify.adapters
import inotify.constants
import click
import os


@click.group()
def cli():
    pass


@click.command()
@click.argument("directory")
@click.option("--output-format", help="The output format for converted images. Valid values are 'png' and 'jpg'.",
              default="jpg")
def watch(directory, output_format="jpg"):
    if output_format != "jpg" and output_format != "png":
        raise ValueError("Output format must be 'jpg' or 'png'.")
    i = inotify.adapters.Inotify()
    i.add_watch(directory, inotify.constants.IN_MOVED_TO | inotify.constants.IN_CLOSE_WRITE)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if os.environ.get("DEBUG"):
            print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))
        if filename[-4:] == "webp":
            im = Image.open(path + "/" + filename)
            conv = im.convert("RGB")
            output_filename = directory + "/" + filename.replace("webp", output_format)
            conv.save(output_filename)
            im.close()
            conv.close()


if __name__ == '__main__':
    cli.add_command(watch)
    cli()
