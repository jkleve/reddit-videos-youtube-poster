Add the following to `crontab -e`

```sh
@hourly cd <project_dir> && exec runner.sh
```
