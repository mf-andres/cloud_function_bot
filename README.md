# Create or deploy cloud function

```
gcloud functions deploy chuinibot ^
--region=europe-west6 ^
--runtime=python39 ^
--source=. ^
--entry-point=manage ^
--trigger-http
```

# Create a service account such as chuinitbot-service-account@proyectos-personales-393909.iam.gserviceaccount.com

# Set invoke permissions

```
gcloud functions add-iam-policy-binding chuinibot ^
--region=europe-west6 ^
--member=chuinitbot-service-account@proyectos-personales-393909.iam.gserviceaccount.com \
--role="roles/cloudfunctions.invoker"
```

# Deploy scheduler

```
gcloud scheduler jobs create http my_job ^
--region=europe-west6 ^
--schedule="45 9 \* \* \*" ^
--uri="https://europe-west6-proyectos-personales-393909.cloudfunctions.net/chuinibot" ^
--http-method=POST ^
--oidc-service-account-email="chuinitbot-service-account@proyectos-personales-393909.iam.gserviceaccount.com" ^
--oidc-token-audience="https://europe-west6-proyectos-personales-393909.cloudfunctions.net/chuinibot" ^
```

# Now each day the bot should be run
