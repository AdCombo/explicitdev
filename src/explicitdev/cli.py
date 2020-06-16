import logging

import click

from explicitdev.config import Config
from explicitdev.fetch.jira import FetchJiraData
from explicitdev.storage.model.base import Base
from explicitdev.storage.update import UpdateJira
from explicitdev.storage.update.holiday import UpdateHolidayCSV


def drop_and_create_all():
    logging.warning('Going to drop DB')
    Base.metadata.drop_all(bind=Config.engine)
    logging.warning('DB dropped')
    logging.warning('Going to create tables.')
    Base.metadata.create_all(bind=Config.engine)
    logging.warning('Tables successfully created.')


@click.group('CLI for working with jira_analyze')
def main():
    pass


@main.command()
def dump():
    fetcher = FetchJiraData(Config)
    data = fetcher.fetch_data()
    fetcher.dump_data(data)


@main.command()
@click.option('--drop_db', is_flag=True)
def load(drop_db):
    if drop_db:
        # todo drop only needed tables not all
        drop_and_create_all()
    fetcher = FetchJiraData(Config)
    data = fetcher.load_data()
    UpdateJira(Config).add_new_issues(data)


@main.command()
@click.option('--drop_db', is_flag=True)
def sync(drop_db):
    # todo delete copypaste and merge it with load
    if drop_db:
        drop_and_create_all()
    UpdateJira(Config).sync()

@main.command()
@click.option('--drop_db', is_flag=True)
def sync_holiday(drop_db):
    updater = UpdateHolidayCSV(Config)
    # todo delete copypaste and merge it with load
    if drop_db:
        updater.drop_create_tables()
    updater.sync()


def _analyze():
    analyzer = Config.JiraAnalyzer(Config)


@main.command()
def analyze():
    _analyze()


if __name__ == "__main__":
    main()
    logging.info('See ya!')
