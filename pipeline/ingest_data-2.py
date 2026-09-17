from asyncio import sleep

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

@click.command()
@click.option('--pg-user', default="root", help='PostgreSQL username')
@click.option('--pg-pass', default="root", help='PostgreSQL password')
@click.option('--pg-host', default="localhost", help='PostgreSQL host')
@click.option('--pg-port', default="5432", help='PostgreSQL port')
@click.option('--pg-db', default="ny_taxi", help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-table', default="taxi_zone_lookup", help='Target table name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize,target_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc'
    url = f'{prefix}/taxi_zone_lookup.csv'

    df_iter= pd.read_csv(
        url,
        iterator=True,
        chunksize=chunksize,
        )
    first=True
    
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first=False
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append')


if __name__=='__main__':
    run()




