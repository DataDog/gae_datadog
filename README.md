# Use Datadog on GAE

## Download the Datadog GAE module

```
cd $MY_GAE_APPLICATION
git clone https://github.com/DataDog/gae_datadog
```

## app.yaml setup

You need to serve the Datadog requests to the Datadog module, include in your app.yaml:
```yaml
handlers:
# Should probably be at the beginning of the list
# so it's not clobbered by a catchall route
- url: /datadog
  script: gae_datadog/datadog.app
```

Set your token, generated from the [integration settings](https://app.datadoghq.com/account/settings#integrations/google_app_engine) on Datadog
```yaml
env_variables:
    DATADOG_AUTH_TOKEN: 'CHANGEME'
```
