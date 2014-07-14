import logging
from lxml import etree

import kdenlive_tools

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

    log.debug('Goodbye %s!' % name)import lxml


FILE = './project.kdenlive'

DEST_FILE = FILE + '-replaced'


tree = etree.parse(FILE)

def list_resources():

    resource_mapping = {}

    producers = tree.xpath('/mlt/producer')

    for producer in producers:
        resources = producer.xpath('property[@name="resource"]/text()')
        assert len(resources) == 1
        producer_id = producer.get('id')
        resource_mapping[producer_id] = resources[0]

    return resource_mapping


for resource_id, file_path in list_resources().items():
    print "%s => %s" % (resource_id, file_path)


def replace(source_id, target_id):
    """ Replaces in the timeline all occurences of the source producer by the tager producer.
    """
    source_entries = tree.xpath('/mlt/playlist/entry[@producer="{}"]'.format(source_id))

    for entry in source_entries:
        entry.attrib['producer'] = target_id


#with open(DEST_FILE, 'w') as f:
#    f.write(etree.tostring(tree.getroot(), xml_declaration=True, pretty_print=True, encoding='UTF-8'))
