from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task()
def extract_from_gcs(year: int) -> Path:
    """Download turnstiles data from GCS"""
    gcs_path = f"molinetes-{year}.parquet"
    #Remember to put your prefect gcs block
    gcs_block = GcsBucket.load('your-gcs-block')
    gcs_block.download_object_to_path(from_path=gcs_path, 
    to_path=f'./tempData/molinetes-{year}.parquet')

    return Path.joinpath(Path(f"tempData"), gcs_path)


@task(log_prints=True)
def transform(path: Path) -> pd.DataFrame:
    """Fill pax amount NaN values with 0, and drop rows containing NaN in other 
    columns"""
    df = pd.read_parquet(path)

    df["PaxAmount"].fillna(0, inplace=True)
    df.dropna(inplace=True)

    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write Dataframe to BigQuery"""
    # Remember to change it to your prefect gcs block
    gcs_creds_block = GcpCredentials.load('your-gcp-creds')
    df.to_gbq(
        # Remember to change it to your project ID
        destination_table='turnstiles_data.turnstiles',
        project_id='your-project-id',
        credentials=gcs_creds_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )


@flow()
def etl_gcs_to_bq(year):
    """Main ETL flow to load data into Big Query"""  
    path = extract_from_gcs(year)
    df = transform(path)
    write_bq(df)
    return len(df)


@flow(log_prints=True)
def parent_etl_gcs_to_bq(years: list[int] = [2018, 2019]) -> None:
    rows = 0
    for year in years:
        rows += etl_gcs_to_bq(year)
    print("Processed rows:", str(rows))


if __name__ == '__main__':
    parent_etl_gcs_to_bq()
