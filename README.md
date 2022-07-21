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

## Run

```
ebike-dl fetch --since 2022-06-15 --out-dir out --login=foo --password=bar
```

where login passwords are from the ebike-connect.com portal.

You'll then get the downloaded files (1per ride) in the folder ./out
(you can also use env variable to provide login, password, ... see --help)

## To GPX

You have the ability to download GPX on Bosch's portal, but those do not contain any additional info like power, cadence or heart_rate.
by using `to-gpx` you can get a gpx with all those things (in gpx extension it might not be supported by the average gpx reader...)

```
ebike-dl to-gpx --file out/myid.json
# output out/myid.pgx
```

Used extensions:

    gpxtpx http://www.garmin.com/xmlschemas/TrackPointExtension/v2
    pwr http://www.garmin.com/xmlschemas/PowerExtension/v1

## To KML 2.2

there is also the ability to transform those to KML (ofc some info will be lost)

```
ebike-dl to-kml --file out/myid.json
# output out/myid.kml
```

## Acknowledgements

- [Cycliste Urbain](https://gitlab.com/cycliste-urbain/resources)

## Authors

- [@eMerzh](https://www.github.com/eMerzh)
