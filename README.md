# Use Datadog on Google App Engine

## Download the Datadog GAE module

```
cd $MY_GAE_APPLICATION
git clone https://github.com/DataDog/gae_datadog
```

## app.yaml setup

You need to serve the Datadog requests to the Datadog module, include in your `app.yaml`:

```yaml
handlers:
# Should probably be at the beginning of the list
# so it's not clobbered by a catchall route
- url: /datadog
  script: gae_datadog.datadog.app
```

Then set your `<DATADOG_API_KEY>` key from the [integration settings](https://app.datadoghq.com/account/settings#api) on Datadog in your `app.yaml`:

```yaml
env_variables:
    DATADOG_API_KEY: '<DATADOG_API_KEY>'
```


**Note**: To send custom metrics to Datadog, see the [Datadog Libraries documentation page](https://docs.datadoghq.com/libraries) for a list of all official and community-contributed API and DogStatsD client libraries.
