# viboo-challenge


![Architecture Diagram](/viboo.png "Architecture")


1. run terraform
    1. cd terraform
    2. terraform init
    3. terraform plan -out myplan
    4. terraform apply myplan
2. create the rest api
    1. gcloud builds submit --region=europe-west6 --project=<project-id> --config=cloud-build.yaml --substitutions="SHORT_SHA=v0.0.1" \
         --gcs-source-staging-dir=gs://viboo-challenge/source .
3. Load the test data
    1. curl http://127.0.0.1:8080/api/generate_example_data
4. Test the APIs:
    1. curl -X POST -H "Content-Type: application/json" -d "@data.json" http://127.0.0.1:8080/api/data
    2. curl http://127.0.0.1:8080/api/average_temperature