from etl_gcs_to_bq import parent_etl_gcs_to_bq
from etl_web_to_gcs import parent_web_to_gcs
from prefect import flow


@flow()
def parent_flow(years: list[int]) -> None:
    parent_web_to_gcs(years)
    parent_etl_gcs_to_bq(years)


if __name__ == '__main__':
    parent_flow([2018, 2019])