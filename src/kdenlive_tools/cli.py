# -*- coding: utf-8 -*-
from __future__ import (
    division, print_function, absolute_import, unicode_literals
)

import tempfile
import logging
import os
from operator import itemgetter

import click
from lxml import etree

from __init__ import __version__


log = logging.getLogger(__name__)


class Project(object):
    """ Utility class to interact with Kdenlive projects.

    Project files are XML documents containing description of resources and
    timelines.
    """

    # List of MLT services consumming file-based resources.
    FILE_BASED_SERVICES = ('avformat', 'pixbuf')

    def __init__(self, project_file):
        self.project_file = project_file
        self.tree = None

    def parse(self):
        """ Parse project XML. """
        self.tree = etree.parse(self.project_file)

    def __repr__(self):
        return '<Project {!r}>'.format(self.project_file)


# Decorator to pass Project instance to all sub-commands.
pass_project = click.make_pass_decorator(Project)


@click.group()
@click.version_option(__version__)
@click.argument('project', type=click.File('rb'))
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print much more debug statements.')
@click.pass_context
def cli(ctx, project, verbose):
    """ Tool to fiddle with the Kdenlive PROJECT file. """
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    click.echo('Parsing project file {} ...'.format(
        os.path.abspath(project.name)))
    ctx.obj = Project(project)
    ctx.obj.parse()


@cli.command()
@click.option('--full-path/--file-name', default=False,
              help='Print full resource file path or only its file name.')
@pass_project
def list_producers(project, full_path):
    """ List producer IDs, type and resource.

    TODO: add options to configure output.
    """
    # Collect mapping of resources
    resource_map = {}
    producers = project.tree.xpath('/mlt/producer')
    for producer in producers:
        # Fetch ID
        producer_id = producer.get('id')
        # Fetch type
        producer_types = producer.xpath('property[@name="mlt_service"]/text()')
        assert len(producer_types) == 1
        producer_type = producer_types.pop()
        # Fetch resource
        resources = producer.xpath('property[@name="resource"]/text()')
        assert len(resources) == 1
        resource = resources.pop()
        if not full_path and producer_type in Project.FILE_BASED_SERVICES:
            resource = os.path.basename(resource)
        # Assemble producer properties
        resource_map[producer_id] = {
            'resource': resource,
            'type': producer_type}

    # Prepare the table of results, sorted by producer IDs
    print_table = sorted(resource_map.items(), key=itemgetter(0))
    # Add header
    print_table.insert(0, ('Producer ID',
                           {'resource': 'Resource file', 'type': 'Resource type'}))

    # Print a formatted table
    max_id_lenght = max([len(row[0]) for row in print_table])
    max_type_lenght = max([len(row[1]['type']) for row in print_table])
    for producer_id, properties in print_table:
        click.echo('{:>{}} | {type:>{}} | {resource}'.format(
            producer_id, max_id_lenght, max_type_lenght, **properties))


@cli.command(short_help="Replace producer's clips in timeline by another.")
@click.argument('source_id')
@click.argument('target_id')
@click.argument('output', type=click.File('wb'), required=False, default=None)
@click.option('--inplace', is_flag=True, default=False,
              help='Save results in source project.')
@pass_project
def replace_producer(project, output, source_id, target_id, inplace):
    """ Replace, in all timelines, all occurences of producer's clips by another.

    TODO: add option to restrict action by timelines.
    """
    click.echo('Replacing producer {} by producer {}:'.format(
        source_id, target_id))
    source_entries = project.tree.xpath('/mlt/playlist/entry[@producer="{}"]'.format(source_id))
    with click.progressbar(source_entries) as entries:
        for entry in entries:
            entry.attrib['producer'] = target_id

    click.echo('{} occurences replaced.'.format(
        len(source_entries), source_id, target_id))

    if inplace:
        # Reopen file for writting.
        project.project_file.close()
        output = open(project.project_file.name, 'wb')
    elif not output:
        # Create a sibling file along the original one for writting
        output_folder, output_filename = os.path.split(project.project_file.name)
        _, output_path = tempfile.mkstemp(
            '.kdenlive', os.path.splitext(output_filename)[0] + '-', output_folder)
        output = open(output_path, 'wb')

    click.echo('Saving results to file {} ...'.format(os.path.abspath(output.name)))
    output.write(etree.tostring(project.tree.getroot(), xml_declaration=True,
                                pretty_print=True, encoding='UTF-8'))

    click.echo('Done.')
