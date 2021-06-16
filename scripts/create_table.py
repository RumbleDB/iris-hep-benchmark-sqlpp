#!/usr/bin/env python3

import argparse
from os.path import dirname, join
from socket import getfqdn

from argparse_logging import add_log_level_argument

from asterixdb import AsterixDB

parser = argparse.ArgumentParser()
parser.add_argument('-S', '--asterixdb-server', action='store',
                    default=getfqdn() + ':19002',
                    help='URL as <host>:<port> of the AsterixDB REST '
                         'interface.')
parser.add_argument('-C', '--asterixdb-dataverse', action='store',
                    help='Default dataverse to use.')
parser.add_argument('-E', '--external-server',
                    help='URI of the (HDFS) storage server (e.g., '
                         '"hdfs://namenode:8020")')
parser.add_argument('-P', '--external-path',
                    help='Path of the external files on HDFS.')
parser.add_argument('-D', '--dataset-name',
                    help='Name of the dataset that should be created.')
parser.add_argument('-T', '--datatype', default='anyType',
                    help='Name of the data type to use for the table '
                         '("anyType" or "eventType").')
parser.add_argument('-F', '--file-format', default='json',
                    help='Format of the external files ("json" or "parquet").')
parser.add_argument('-L', '--storage-location', default='external',
                    help='Storage location of the date ("internal" or'
                         '"external"), i.e., whether or not to load the data')
add_log_level_argument(parser)
args = parser.parse_args()

conf = {
    'external_server': args.external_server,
    'external_path': args.external_path,
    'dataset_name': args.dataset_name,
    'type_name': args.datatype,
}

# Assemble paths to SQL files
base_dir = dirname(__file__)

create_table_file = \
    join(base_dir, 'create_{}_table_{}.sqlpp'
                   .format(args.storage_location, args.file_format))

type_prefix = args.datatype[:-len('Type')]
create_type_file = \
    join(base_dir, 'create_{}_type.sqlpp'.format(type_prefix))

# Set up client
asterixdb = AsterixDB(args.asterixdb_server, args.asterixdb_dataverse)

# Create type
with open(create_type_file, 'r') as f:
    query = f.read()
query = query % conf
asterixdb.run(query)

# Create new table
with open(create_table_file, 'r') as f:
    query = f.read()
query = query % conf
asterixdb.run(query)
