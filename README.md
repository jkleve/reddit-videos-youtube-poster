Add the following to `crontab -e`

```sh
@hourly cd <project_dir> && exec runner.sh
```

## Sqlite

#### Install

Ubuntu/Debian

```sh
sudo apt install -y sqlite3
```

#### Usage

```sh
$ sqlite3 -column -header
> .open posts.db
> .tables
> SELECT * FROM top_of_rvideos;
> SELECT * FROM top_of_rvideos_new;
> .exit
```
