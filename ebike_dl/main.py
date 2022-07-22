from __future__ import annotations

import dataclasses
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterator, List, Tuple

import requests
from typer import Exit, Option, Typer

app = Typer()

USER_DATE_FORMAT = "%Y/%m/%d %H:%M"


@dataclass
class ECRideHeader:
    id: str
    start_time: datetime
    end_time: datetime
    driving_time: timedelta
    type: str
    status: int
    total_distance: float
    title: str
    calories: float
    avg_speed: float
    max_speed: float
    header_rides_ids: List[str]

    @staticmethod
    def from_dict(obj: dict[str, Any]) -> ECRideHeader:
        return ECRideHeader(
            id=str(obj["id"]),
            start_time=datetime.fromtimestamp(int(obj["start_time"]) / 1000),
            end_time=datetime.fromtimestamp(int(obj["end_time"]) / 1000),
            driving_time=timedelta(seconds=int(obj["driving_time"])),
            type=str(obj["type"]),
            status=int(obj["status"]),
            total_distance=float(obj["total_distance"]),
            title=str(obj["title"]),
            calories=float(obj["calories"]),
            avg_speed=float(obj["avg_speed"]),
            max_speed=float(obj["max_speed"]),
            header_rides_ids=obj["header_rides_ids"],
        )


@dataclass
class ECActivity:
    id: str
    start_time: datetime
    end_time: datetime
    driving_time: timedelta
    type: str
    status: int
    total_distance: float
    header_rides_ids: List[str]
    ride_headers: List[ECRideHeader]

    @staticmethod
    def from_dict(obj: dict[str, Any]) -> ECActivity:
        return ECActivity(
            id=str(obj["id"]),
            start_time=datetime.fromtimestamp(int(obj["start_time"]) / 1000),
            end_time=datetime.fromtimestamp(int(obj["end_time"]) / 1000),
            driving_time=timedelta(seconds=int(obj["driving_time"])),
            type=str(obj["type"]),
            status=int(obj["status"]),
            total_distance=float(obj["total_distance"]),
            header_rides_ids=obj["header_rides_ids"],
            ride_headers=[ECRideHeader.from_dict(y) for y in obj["ride_headers"]],
        )


@dataclass
class ECRide:
    id: str
    start_time: datetime
    end_time: datetime
    driving_time: timedelta
    type: str
    status: int
    total_distance: float
    title: str
    operation_time: str
    header_type: str
    calories: float
    avg_speed: float
    avg_heart_rate: float
    avg_cadence: float
    avg_altitude: float
    max_speed: float
    max_heart_rate: int
    max_cadence: int
    max_altitude: float
    cadence: List[List[int]]
    heart_rate: List[List[object]]
    speed: List[List[float]]
    coordinates: List[List[List[float]]]
    portal_altitudes: List[List[float]]
    training_effect: int
    training_load_peak: int
    speed_weight: int
    cadence_weight: int
    driver_power_weight: int
    significant: int
    elevation_gain: float
    elevation_loss: float
    total_driver_power: int
    total_driver_consumption_percentage: float
    total_battery_consumption_percentage: float
    bui_decoded_serial_number: str
    bui_decoded_part_number: str
    drive_unit_decoded_serial_number: str
    drive_unit_decoded_part_number: str
    average_driver_power: float
    power_output: List[List[int]]
    significant_assistance_level_percentages: List[SignificantAssistanceLevelPercentage]
    drive_unit_serial: str

    @staticmethod
    def from_dict(obj: Any) -> ECRide:
        return ECRide(
            id=str(obj.get("id")),
            start_time=datetime.fromtimestamp(int(obj["start_time"]) / 1000),
            end_time=datetime.fromtimestamp(int(obj["end_time"]) / 1000),
            driving_time=timedelta(seconds=int(obj["driving_time"])),
            type=str(obj.get("type")),
            status=int(obj.get("status")),
            total_distance=float(obj.get("total_distance")),
            title=str(obj.get("title")),
            operation_time=str(obj.get("operation_time")),
            header_type=str(obj.get("header_type")),
            calories=float(obj.get("calories")),
            avg_speed=float(obj.get("avg_speed")),
            avg_heart_rate=float(obj.get("avg_heart_rate")),
            avg_cadence=float(obj.get("avg_cadence")),
            avg_altitude=float(obj.get("avg_altitude")),
            max_speed=float(obj.get("max_speed")),
            max_heart_rate=int(obj.get("max_heart_rate")),
            max_cadence=int(obj.get("max_cadence")),
            max_altitude=float(obj.get("max_altitude")),
            cadence=obj.get("cadence"),
            heart_rate=obj.get("heart_rate"),
            speed=obj.get("speed"),
            coordinates=obj.get("coordinates"),
            portal_altitudes=obj.get("portal_altitudes"),
            training_effect=int(obj.get("training_effect")),
            training_load_peak=int(obj.get("training_load_peak")),
            speed_weight=int(obj.get("speed_weight")),
            cadence_weight=int(obj.get("cadence_weight")),
            driver_power_weight=int(obj.get("driver_power_weight")),
            significant=int(obj.get("significant")),
            elevation_gain=float(obj.get("elevation_gain")),
            elevation_loss=float(obj.get("elevation_loss")),
            total_driver_power=int(obj.get("total_driver_power")),
            total_driver_consumption_percentage=float(obj.get("total_driver_consumption_percentage")),
            total_battery_consumption_percentage=float(obj.get("total_battery_consumption_percentage")),
            bui_decoded_serial_number=str(obj.get("bui_decoded_serial_number")),
            bui_decoded_part_number=str(obj.get("bui_decoded_part_number")),
            drive_unit_decoded_serial_number=str(obj.get("drive_unit_decoded_serial_number")),
            drive_unit_decoded_part_number=str(obj.get("drive_unit_decoded_part_number")),
            average_driver_power=float(obj.get("average_driver_power")),
            power_output=obj.get("power_output"),
            significant_assistance_level_percentages=[
                SignificantAssistanceLevelPercentage(int(y.get("level")), float(y.get("value")))
                for y in obj.get("significant_assistance_level_percentages")
            ],
            drive_unit_serial=str(obj.get("drive_unit_serial")),
        )


class datetime_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int(round((obj.timestamp()) * 1000))
        if isinstance(obj, timedelta):
            return obj.seconds
        return json.JSONEncoder.default(self, obj)


@dataclass
class SignificantAssistanceLevelPercentage:
    level: int
    value: float


class ClientError(Exception):
    message: str


class EConnectFDownloader:
    cookie_data: str
    user_info: Any

    BASE_URL = "https://www.ebike-connect.com/ebikeconnect/api"

    activities: list[ECActivity] = []

    def __init__(self, cookie: str):
        self.cookie_data = cookie

    @classmethod
    def from_login(cls, login: str, password: str) -> EConnectFDownloader:

        response = requests.post(
            EConnectFDownloader.BASE_URL + "/portal/login/public",
            json={"username": login, "password": password, "rememberme": True},
        )
        if not response.ok:
            raise Exception(f"Login error {response.text}")
        if error := response.json().get("errors"):
            raise Exception(f"Login error {error[0].get('message')}")
        obj = cls(response.cookies["REMEMBER"])
        obj.user_info = response.json()

        return obj

    def get_activities_ids(self, since: datetime, to: datetime | None = None) -> list[str]:
        to = datetime.now() if to is None else to

        print(f"Downloading ride list from {since.strftime(USER_DATE_FORMAT)} to {to.strftime(USER_DATE_FORMAT)}")

        end_time = int(to.timestamp() * 1000)
        maxtrips = 2

        response = self._request("/portal/activities/trip/headers", {"max": maxtrips, "offset": end_time})
        ride_ids = []
        for item in response:
            activity = ECActivity.from_dict(item)
            self.activities.append(activity)
            for ride in activity.ride_headers:
                if since <= ride.start_time <= to:
                    ride_ids.append(ride.id)

        return ride_ids

    def get_activity(self, id: str) -> ECRide:
        response = self._request(f"/activities/ride/details/{id}")
        print(f" ...Downloading Ride : {id}")

        return ECRide.from_dict(response)

    def _request(self, url, query_params: dict[str, Any] | None = None) -> Any:
        # referer = "https://www.ebike-connect.com/activities/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
            # "Accept": "application/vnd.ebike-connect.com.v4+json, application/json",
            "Protect-from": "CSRF",
        }
        response = requests.get(
            self.BASE_URL + url,
            headers=headers,
            cookies={"REMEMBER": self.cookie_data},
            params=query_params,
        )

        return response.json()


def init_dir(out_dir: Path):
    if not out_dir.exists():
        try:
            os.makedirs(out_dir)
        except:
            print(f"Error: Unable to create output dir")
            Exit(1)


@app.command()
def fetch(
    login: str = Option(..., help="Login Email on the Portal", envvar="LOGIN"),
    password: str = Option(..., help="Password on the Portal", envvar="PASSWORD"),
    out_dir: Path = Option(
        ...,
        help="Output path of the downloaded files",
        writable=True,
        dir_okay=True,
        file_okay=False,
        envvar="OUT_DIR",
    ),
    since: datetime = Option(datetime.now() - timedelta(days=7), envvar="SINCE"),  # TODO: make this an interval or smth
):
    """
    Download Bike Activities form Bosch eBike Connect portal
    """

    init_dir(out_dir)

    try:
        client = EConnectFDownloader.from_login(login, password)
        ids = client.get_activities_ids(since)
        for idx, id in enumerate(ids):
            print(f"## Ride {idx+1} on {len(ids)}")

            activity = client.get_activity(id)

            print(f" ...Writing {activity.id}.json")
            with open(os.path.join(out_dir, f"{activity.id}.json"), "w") as write_file:
                json.dump(dataclasses.asdict(activity), write_file, cls=datetime_encoder)

    except ClientError as e:
        print(f"Error: {e.message}")
        Exit(1)


def load_trips(input: Path) -> Iterator[Tuple[ECRide, Path]]:
    files = []
    if input.is_dir():
        for file in os.listdir(input):
            if file.endswith(".json"):
                files.append(Path(os.path.join(input, file)))
    else:
        files = [input]
    for file in files:
        ride_file = open(file)
        trip_raw = json.load(ride_file)
        yield ECRide.from_dict(trip_raw), file


def write_export(file: Path, extension: str, content: str):
    filename = file.stem
    new_file = os.path.join(file.parent, f"{filename}.{extension}")
    print(f"Write to {new_file}")
    with open(new_file, "w") as write_file:
        write_file.write(content)


def trip_to_gpx(trip: ECRide) -> str:
    count_item = len(trip.coordinates[0])
    interval = trip.end_time - trip.start_time
    total_points = interval / count_item

    segments = []
    for idx, coord in enumerate(trip.coordinates[0]):
        alt = trip.portal_altitudes[0][idx]
        point_when = trip.start_time + (total_points * idx)

        segments.append(
            f"""<trkpt lat="{coord[0] or ''}" lon="{coord[1] or ''}">
                <ele>{alt}</ele>
                <time>{point_when.isoformat()}</time>
                <extensions>
                <gpxtpx:TrackPointExtension>
                    <gpxtpx:speed>{trip.speed[0][idx] or ''}</gpxtpx:speed>
                    <gpxtpx:hr>{trip.heart_rate[0][idx] or ''}</gpxtpx:hr>
                    <gpxtpx:cad>{trip.cadence[0][idx] or ''}</gpxtpx:cad>
                    <pwr:PowerInWatts>{trip.power_output[0][idx] or ''}</pwr:PowerInWatts>
                </gpxtpx:TrackPointExtension>
                </extensions>
            </trkpt>
        """
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
        <gpx xmlns="http://www.topografix.com/GPX/1/1"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            creator="ebik-dl" version="1.1"
            xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"
            xmlns:pwr="http://www.garmin.com/xmlschemas/PowerExtension/v1"
            xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd  http://www.garmin.com/xmlschemas/TrackPointExtension/v2 http://www.garmin.com/xmlschemas/TrackPointExtensionv2.xsd http://www.garmin.com/xmlschemas/PowerExtension/v1 http://www.garmin.com/xmlschemas/PowerExtensionv1.xsd">
        <metadata>
            <time>{datetime.now().isoformat()}</time>
        </metadata>
        <trk>
            <name>{trip.title}</name>
            <trkseg>
              {"".join(segments)}
            </trkseg>
        </trk>
    </gpx>
    """


def trip_to_kml(trip: ECRide) -> str:
    track_type = "cyclism"
    type_icon = "BIKE"

    count_item = len(trip.coordinates[0])
    interval = trip.end_time - trip.start_time
    total_points = interval / count_item

    positions = []
    for idx, coord in enumerate(trip.coordinates[0]):
        alt = trip.portal_altitudes[0][idx]
        lon_lat = f"{coord[1] or ''} {coord[0] or ''}".strip()
        if lon_lat:
            lon_lat += f" {alt or '0'}"
        point_when = trip.start_time + (total_points * idx)
        positions.append(
            f"""<when>{point_when.isoformat()}Z</when>
        <gx:coord>{lon_lat}</gx:coord>
        """
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2"
        xmlns:gx="http://www.google.com/kml/ext/2.2"
        xmlns:atom="http://www.w3.org/2005/Atom"
        xmlns:opentracks="http://opentracksapp.com/xmlschemas/v1">
        <Document>
            <open>1</open>
            <visibility>1</visibility>
            <name><![CDATA[{trip.title}]]></name>
            <atom:generator><![CDATA[JSON2KML]]></atom:generator>
            <Style id="track">
                <LineStyle>
                    <color>7f0000ff</color>
                    <width>4</width>
                </LineStyle>
                <IconStyle>
                    <scale>1.3</scale>
                    <Icon />
                </IconStyle>
            </Style>
            <Style id="waypoint">
                <IconStyle>
                    <Icon />
                </IconStyle>
            </Style>
            <Schema id="schema">
                <gx:SimpleArrayField name="speed" type="float">
                    <displayName><![CDATA[Vitesse (m/s)]]></displayName>
                </gx:SimpleArrayField>
                <gx:SimpleArrayField name="power" type="float">
                    <displayName><![CDATA[Puissance (W)]]></displayName>
                </gx:SimpleArrayField>
                <gx:SimpleArrayField name="cadence" type="float">
                    <displayName><![CDATA[Cadence (tr/min)]]></displayName>
                </gx:SimpleArrayField>
                <gx:SimpleArrayField name="heart_rate" type="float">
                    <displayName><![CDATA[Fréquence cardiaque (bpm)]]></displayName>
                </gx:SimpleArrayField>
            </Schema>
            <Placemark>
                <name><![CDATA[{trip.title}]]></name>
                <icon><![CDATA[{type_icon}]]></icon>
                <opentracks:trackid>{trip.id}</opentracks:trackid>
                <styleUrl>#track</styleUrl>
                <ExtendedData>
                    <Data name="type">
                        <value><![CDATA[{track_type}]]></value>
                    </Data>
                </ExtendedData>
                <gx:MultiTrack>
                    <altitudeMode>absolute</altitudeMode>
                    <gx:interpolate>1</gx:interpolate>
                    <gx:Track>
                        {"".join(positions)}
                        <ExtendedData>
                            <SchemaData schemaUrl="#schema">
                                <gx:SimpleArrayData name="speed">
                                    {''.join([f"<gx:value>{i or ''}</gx:value>" for i in trip.speed[0]])}
                                </gx:SimpleArrayData>
                                <gx:SimpleArrayData name="power">
                                    {''.join([f"<gx:value>{i or ''}</gx:value>" for i in trip.power_output[0]])}
                                </gx:SimpleArrayData>
                                <gx:SimpleArrayData name="cadence">
                                    {''.join([f"<gx:value>{i or ''}</gx:value>" for i in trip.cadence[0]])}
                                </gx:SimpleArrayData>
                                <gx:SimpleArrayData name="heart_rate">
                                    {''.join([f"<gx:value>{i or ''}</gx:value>" for i in trip.heart_rate[0]])}
                                </gx:SimpleArrayData>
                            </SchemaData>
                        </ExtendedData>
                    </gx:Track>
                </gx:MultiTrack>
            </Placemark>
        </Document>
    </kml>
    """


@app.command()
def to_gpx(
    file: Path = Option(
        ...,
        help="File downloaded from Ebike Portal (if a directory is given al *.json file in that directory) ",
        file_okay=True,
        dir_okay=True,
        exists=True,
    ),
):
    """Export json file(s) to a GPX"""
    for trip, in_file in load_trips(file):
        write_export(in_file, "gpx", trip_to_gpx(trip))


@app.command()
def to_kml(
    file: Path = Option(
        ...,
        help="File downloaded from Ebike Portal (if a directory is given al *.json file in that directory)",
        file_okay=True,
        dir_okay=True,
        exists=True,
    ),
):
    """Export json file(s) to KML"""
    for trip, in_file in load_trips(file):
        write_export(in_file, "kml", trip_to_kml(trip))


if __name__ == "__main__":
    app()
