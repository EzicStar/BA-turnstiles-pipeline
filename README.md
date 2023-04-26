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

## Results

Here is a dashboard made in Google Looker Studio based on the data model transformed with dbt. You can look it in more detail [here](https://lookerstudio.google.com/reporting/a5163aa8-0e1f-4efb-b330-14ef7f996cc1).

![Dashboard](https://github.com/EzicStar/BA-turnstiles-pipeline/blob/main/Images/Dashboard.jpg)

## Run the Walkthrough Tutorial

Reproducing this project has been tested on an Ubuntu 20.04 LTS VM, in Google Cloud.  This project will require a similar VM, a Google Cloud account, a project on Google Cloud, and a service account with appropriate permissions for the project. Credits to [MikeColemn](https://github.com/mikecolemn) for creating such clear steps for the VM setup!

1) If you need to set up a VM, an account, project, or service account on Google Cloud, see [Setup Readme](https://github.com/EzicStar/BA-turnstiles-pipeline/blob/main/setup/setup_readme.md) for more detailed instructions.

2) On your VM, clone the repo, `git clone https://github.com/EzicStar/BA-turnstiles-pipeline.git`, and then `cd` into the repo folder

3) If you need to install Google Cloud CLI, Anaconda, and Terraform, you can run a bash script with this command, `bash ./setup/setup.sh`, which will perform the following actions:

    * Apply initial updates, and install
    * Install Google Cloud cli application
    * Setup Anaconda and Terraform.

    * (Note) This may take a little time to process and if you see any prompts from updates, you can hit OK on the prompts and `f` for the MORE prompt for the Anaconda setup

4) Setup your conda virtual environment with the following commands:

    * `source ~/.bashrc` - (if you just installed Anaconda above, and haven't restarted your shell session)
    * `conda create -n baturnstiles python=3.9 -y`
    * `conda activate baturnstiles`
    * `pip install -r ./setup/requirements.txt`

5) Save your Google Cloud service account .json file to the ./creds folder.  You can sftp the file from your local computer to that location.  You could even just open the file on your local computer, copy the contents of the file and do `nano ./creds/[filename].json` on the VM and paste in the contents into this new blank file, and then do CTRL + X, and then `Y` and ENTER, to save and exit the file.

6) Set an environment variable for your service account file that you just saved with this command: `export GOOGLE_APPLICATION_CREDENTIALS="<absolute path to the json file in the ./creds folder>"`

7) Update the GOOGLE_APPLICATION_CREDENTIALS environment variable in the ./.env file, using the same absolute path to the .json service account file

8) Run `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS` to authenticate with Google Cloud, with your service account .json file.

9) Run Terraform to deploy your infrastructure to your Google Cloud Project.  Run the following commands:

    * `terraform -chdir="./Terraform" init` - to initialize terraform
    * `terraform -chdir="./Terraform" plan -var="project=<project id here>"`, replacing <project id here> with your Google Project ID.  This will build a deployment plan that you can review.
    * `terraform -chdir="./Terraform" apply -var="project=<project id here>"`, replacing <project id here> with your Google Project ID.  This will apply the deployment plan and deploy the infrastructure

10) Run the following commands to set up a local Prefect profile

    * `prefect profile create baturnstiles`
    * `prefect profile use baturnstiles`
    * `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`

11) Open two new terminal windows and ssh into your VM.  These additional terminals are going to be for launching the Prefect orion server, and to launch a work queue, which will process deployed pipelines

    * Additional window 1:
        * `conda activate baturnstiles`
        * `prefect orion start`

    * Additional window 2:
        * `conda activate baturnstiles`
        * `prefect agent start --work-queue "default"`

12) From your original terminal session, run this command to setup some blocks for your GCP credentials in prefect: `python ./setup/prefect_setup_blocks.py`. If a KeyError raises, you may repeat step 6.

13) Add your project ID in `write_bq()` function from `etl_gcs_to_bq.py`. You can do this running: `nano ./Pipelines etl_gcs_to_bq.py` and changing the string where it says `'your-project-id'`. 

14) From your original terminal session, run the following three commands to deploy the pipeline to Prefect and then run it for all years of data

    * `prefect deployment build Pipelines/parent_flow.py:parent_flow -n "Baturnstiles-ETL"`
    * `prefect deployment apply parent_flow-deployment.yaml`
    * `prefect deployment run parent-flow/Baturnstiles-ETL -p "years=[2018, 2019]"`

    This may take 10-20 minutes to run the full pipeline.  You can switch to the terminal session for the work queue to watch the progress if you like. After this step you can already shut down the VM to avoid costs.

15) In Google Cloud, go to Big Query workspace and create a new query tab. Copy the content from [queries.txt](https://github.com/EzicStar/BA-turnstiles-pipeline/blob/main/setup/queries.txt) and run the first SQL instruction to create a partitioned and clustered table. Below you can see some queries that prove the increase in performance using a partitioned and clustered table.

16) Make high-level transformations of the data using dbt. Create a dbt account [here](https://cloud.getdbt.com).

17) Connect to BigQuery and add a repository following these [instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md). Creating a new repo is recommended.

18) Add the seeds and model in the folder named dbt to your new repo. Then load seeds using `dbt seed`.

19) Run the model using `dbt run`.

 > **Important note: Once you're done evaluating this project, make sure to stop and remove any cloud resources.  If you're using a cloud VM, make sure to stop it in your VM Instances screen in Google Cloud Console, and potentially delete it if you no longer want it.  This way it's not up and running, and using up your credits.  In addition, you can use Terraform to destroy your buckets and datasets, with `terraform -chdir="./terraform" destroy -var="project=<project id here>"`**

## Further steps
- Add tests
- Add a CI/CD Pipeline
- Dockerise prefect orion and agent server
- Adapt ingestion for different CSV formats submitted in BA Open Data

## Special thanks to [DataTalksClub](https://datatalks.club/)!
