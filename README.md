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

Reproducing this project has been tested on an Ubuntu 20.04 LTS VM, in both Google Cloud and a Proxmox homelab.  This project will require a similar VM, a Google Cloud account, a project on Google Cloud, and a service account with appropriate permissions for the project.

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

    * `terraform -chdir="./terraform" init` - to initialize terraform
    * `terraform -chdir="./terraform" plan -var="project=<project id here>"`, replacing <project id here> with your Google Project ID.  This will build a deployment plan that you can review.
    * `terraform -chdir="./terraform" apply -var="project=<project id here>"`, replacing <project id here> with your Google Project ID.  This will apply the deployment plan and deploy the infrastructure
