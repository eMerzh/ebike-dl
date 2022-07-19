[![PyPI version](https://badge.fury.io/py/ebike-dl.svg)](https://badge.fury.io/py/ebike-dl)

# ebike-downloader

Bosch eBike Connect Activity Downloader (https://www.ebike-connect.com/dashboard)
Fetch activities by dates and download a copy of the rides.

## Install

ebike-downloader uses [poetry](https://python-poetry.org/).

You can easily run it using

```bash
pipx install ebike-dl
```

might be published on pypi later.

## Run

```
ebike-dl fetch --since 2022-06-15 --out-dir out --login=foo --password=bar
```

where login passwords are from the ebike-connect.com portal.

You'll then get the downloaded files (1per ride) in the folder ./out
(you can also use env variable to provide login, password, ... see --help)

there is also the ability to transform those to KML (ofc some info will be lost)

```
ebike-dl to-kml --file out/myid.json
# output out/myid.kml
```

## Acknowledgements

- [Cycliste Urbain](https://gitlab.com/cycliste-urbain/resources)

## Authors

- [@eMerzh](https://www.github.com/eMerzh)
