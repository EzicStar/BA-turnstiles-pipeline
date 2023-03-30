# Buenos Aires Subway Turnstiles Data Pipeline
## Overview

Buenos Aires subway, also known as "Subte", was the first underground metro system in Latin America and the Southern Hemisphere. The goal of this project is to apply Data Engineering concepts to extract, process and visualize passengers distribution from 2018 and 2019 recorded by the turnstiles of the stations. 
The steps required for acomplishing this goal are the following:

 - Upload all source data into a Data Lake.
 - Format data and upload it into a Data Warehouse.
 - Make a model with high-level transformations.
 - Visualize data.
 
![Solution Overview](https://github.com/EzicStar/BA-turnstiles-pipeline/blob/main/Images/SolutionOverview.jpeg)

## Dataset
The dataset is obtained from [Buenos Aires Goverment Data Site](https://data.buenosaires.gob.ar/dataset/subte-viajes-molinetes/resource/51f7cdcf-04dd-40c0-b0b1-32b016d3ab6b). The site provides CSV files with records of the turnstiles. Each record contains information about the turnstile and the amount of passengers that passed through it in a 15 minute range. 

Data from 2018 and 2019 were used for this project because datasets from the following years vary their structure significantly.

## Technologies

 -  Cloud: Google Cloud Platform (GCP)
-   Infrastructure as code (IaC): Terraform
-   Workflow orchestration: Prefect
-   Data Warehouse: BigQuery
-   Batch processing: dbt
- Data Visualization: Google Looker Studio
