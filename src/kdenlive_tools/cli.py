# -*- coding: utf-8 -*-
from __future__ import (
    division, print_function, absolute_import, unicode_literals
)

import logging
import os

import click
from lxml import etree

from __init__ import __version__


log = logging.getLogger(__name__)


class Project(object):
    """ Utility class to interact with Kdenlive projects.

    Project files are XML documents containing description of resources and
    timelines.
    """

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
    """ Tools to fiddle with the PROJECT Kdenlive project file. """
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    click.echo('Parsing project file {!r}...'.format(
        os.path.abspath(project.name)))
    ctx.obj = Project(project)
    ctx.obj.parse()


@cli.command()
@pass_project
def list_producers(project):
    """ List producer IDs and their source files.

    TODO: add options to configure output.
    """
    # Collect mapping of resources
    resource_map = {}
    producers = project.tree.xpath('/mlt/producer')
    for producer in producers:
        resources = producer.xpath('property[@name="resource"]/text()')
        assert len(resources) == 1
        producer_id = producer.get('id')
        resource_map[producer_id] = resources[0]

    # Print mapping
    for producer_id, resource_file in resource_map.items():
        click.echo('{} :> {}.'.format(
            producer_id, resource_file))


@cli.command(short_help="Replace producer's clips in timeline by another.")
@click.argument('source_id')
@click.argument('target_id')
@click.argument('output', type=click.File('wb'))
@pass_project
def replace_producer(project, output, source_id, target_id):
    """ Replace, in all timelines, all occurences of producer's clips by another.

    TODO: add --inplace option.
    TODO: add option to restrict action by timelines.
    """
    click.echo('Replacing producer ID:{!r} by producer ID:{!r}.'.format(
        source_id, target_id))
    source_entries = project.tree.xpath('/mlt/playlist/entry[@producer="{}"]'.format(source_id))
    for entry in source_entries:
        entry.attrib['producer'] = target_id

    click.echo('{} occurences of producer {} replaced by producer {}.'.format(
        len(source_entries), source_id, target_id))

    click.echo('Saving results to file {!r} ...'.format(output))
    output.write(etree.tostring(project.tree.getroot(), xml_declaration=True,
                                pretty_print=True, encoding='UTF-8'))

    click.echo('Done.')
