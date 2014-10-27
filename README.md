
# Download the Datadog GAE module

```
cd $MY_GAE_APPLICATION
git clone https://github.com/DataDog/gae-datadog
```

# app.yaml setup

You need to serve the Datadog requests to the Datadog module, include in your app.yaml:
```yaml
handlers:
# Should probably be at the beginning of the list so it's not clobbered by a catchall route
- url: /datadog
  script: gae-datadog/$framework/datadog.app
```

Depending on the framework you are using, set the `$framework` variable accordingly:
* `flask`
* ...

Set your Datadog token, generated from the [integration settings](https://app.datadoghq.com/account/settings#integrations/google_app_engine)
```yaml
env_variables:
    DATADOG_AUTH_TOKEN: 'CHANGEME'
```
