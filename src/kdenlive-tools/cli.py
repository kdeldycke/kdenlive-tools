import logging

import kdenlive-tools

log = logging.getLogger(__name__)


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
@click.option('--debug', default=False, help='Debug mode.')
def main(count, name, debug):
    """Simple program that greets NAME for a total of COUNT times."""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    for x in range(count):
        click.echo('Hello %s!' % name)

    log.debug('Goodbye %s!' % name)