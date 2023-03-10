import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from pathlib import Path


@task(log_prints=True)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read turnstiles data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)

    # Some of the files uses ; as a delimiter, so by this way we check if  
    # the df has the correct amount of columns
    if len(df.columns) < 2:
        df = pd.read_csv(dataset_url, delimiter=';')
    
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop unnecesary columns and translate the others"""

    # Remove columns that aren't well described in the dataset documentation
    df = df.drop(columns=['pax_pagos', 'pax_pases_pagos', 'pax_franq',
                          'periodo'])

    df.rename(
    columns={"fecha": "Date", "desde": "StartTime", "linea": "Line",
             "hasta": "EndTime", "molinete": "TurnstileID",
             "estacion": "Station", "total": "PaxAmount" }, inplace=True)

    return df


@task(log_prints=True)
def format_date(df: pd.DataFrame) -> pd.DataFrame:
    """Fix datetime type issues"""

    # Create new columns with date and time joined, and make it datetime type
    df['StartDateTime'] = pd.to_datetime(df['Date'] + df['StartTime'],
    format='%Y-%m-%d%H:%M:%S')
    df['EndDateTime'] = pd.to_datetime(df['Date'] + df['EndTime'],
    format='%Y-%m-%d%H:%M:%S')
    
    df = df.drop(columns=['Date', 'StartTime', 'EndTime'])

    return df


@task()
def write_local(df : pd.DataFrame, dataset_file : str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"tempData/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    # Remember to create your own gcs bucket prefect block
    gcs_block = GcsBucket.load("your-gcs-block-name")
    gcs_block.upload_from_path(from_path=f"{path}")


@flow()
def turnstiles_web_to_gcs(year: int) -> None:
    dataset_file = f'molinetes-{year}'
    dataset_url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets' \
    f'/sbase/subte-viajes-molinetes/molinetes-{year}.zip'
    
    df = fetch(dataset_url)
    df = clean(df)
    df = format_date(df)
    path = write_local(df, dataset_file)
    write_gcs(path)

if __name__ == '__main__':
    turnstiles_web_to_gcs(2019)
