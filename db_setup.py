import argparse

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import ProgrammingError

from db.schema import SCHEMAS
from db.models.base import Base
# The following are the actual tables being made.
# Though apparently unused, the imports are needed so they will be linked to 'Base'
from db.models.notify import Subscription, Constraint
from db.models.security import User, Group, Role, Permission

def create_schemas(engine, schemas):
    # Create schemas
    for schema in schemas:
        try:
            engine.execute(CreateSchema(schema))
        except ProgrammingError as error:
            if not 'schema "%s" already exists' % schema in str(error):
                raise

def get_tables(schemas):
    tables = [
        Base.metadata.tables[table]
        for table in Base.metadata.tables
        if any([table.startswith(schema) for schema in schemas])
    ]
    return tables

def create_tables(engine, schemas):
    Base.metadata.create_all(engine, tables=get_tables(schemas))

def drop_tables(engine, schemas):
    Base.metadata.drop_all(engine, tables=get_tables(schemas))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dburl', required=True)
    parser.add_argument('-s', '--schemas', default=SCHEMAS, choices=SCHEMAS)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-D', '--drop', action='store_true')
    parser.add_argument('-C', '--create', action='store_true')
    args = parser.parse_args()
    
    # Create sqlchemy engine
    engine = create_engine(args.dburl, echo=args.verbose)

    if args.drop:
        drop_tables(engine, args.schemas)
    if args.create:
        create_schemas(engine, args.schemas)
        create_tables(engine, args.schemas)
    

main()