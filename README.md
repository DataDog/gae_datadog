# Use Datadog on Google App Engine

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
  script: gae_datadog.datadog.app
```

Set your API key from the [integration settings](https://app.datadoghq.com/account/settings#integrations/google_app_engine) on Datadog
```yaml
env_variables:
    DATADOG_API_KEY: 'YOURAPIKEY'
```

## Use custom metrics with dogapi

This [gist](https://gist.github.com/LeoCavaille/bb4379d628db2fa6e102) will show you an example of how to use custom metrics in your code.
