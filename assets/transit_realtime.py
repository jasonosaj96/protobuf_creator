# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: trip_update.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


class FeedHeaderIncrementality(betterproto.Enum):
    FULL_DATASET = 0
    DIFFERENTIAL = 1


class TripUpdateStopTimeUpdateScheduleRelationship(betterproto.Enum):
    SCHEDULED = 0
    SKIPPED = 1
    NO_DATA = 2


class VehiclePositionVehicleStopStatus(betterproto.Enum):
    INCOMING_AT = 0
    STOPPED_AT = 1
    IN_TRANSIT_TO = 2


class VehiclePositionCongestionLevel(betterproto.Enum):
    UNKNOWN_CONGESTION_LEVEL = 0
    RUNNING_SMOOTHLY = 1
    STOP_AND_GO = 2
    CONGESTION = 3
    SEVERE_CONGESTION = 4


class VehiclePositionOccupancyStatus(betterproto.Enum):
    EMPTY = 0
    MANY_SEATS_AVAILABLE = 1
    FEW_SEATS_AVAILABLE = 2
    STANDING_ROOM_ONLY = 3
    CRUSHED_STANDING_ROOM_ONLY = 4
    FULL = 5
    NOT_ACCEPTING_PASSENGERS = 6


class AlertCause(betterproto.Enum):
    UNKNOWN_CAUSE = 1
    OTHER_CAUSE = 2
    TECHNICAL_PROBLEM = 3
    STRIKE = 4
    DEMONSTRATION = 5
    ACCIDENT = 6
    HOLIDAY = 7
    WEATHER = 8
    MAINTENANCE = 9
    CONSTRUCTION = 10
    POLICE_ACTIVITY = 11
    MEDICAL_EMERGENCY = 12


class AlertEffect(betterproto.Enum):
    NO_SERVICE = 1
    REDUCED_SERVICE = 2
    SIGNIFICANT_DELAYS = 3
    DETOUR = 4
    ADDITIONAL_SERVICE = 5
    MODIFIED_SERVICE = 6
    OTHER_EFFECT = 7
    UNKNOWN_EFFECT = 8
    STOP_MOVED = 9


class TripDescriptorScheduleRelationship(betterproto.Enum):
    SCHEDULED = 0
    ADDED = 1
    UNSCHEDULED = 2
    CANCELED = 3


@dataclass
class FeedMessage(betterproto.Message):
    """
    The contents of a feed message. A feed is a continuous stream of feed
    messages. Each message in the stream is obtained as a response to an
    appropriate HTTP GET request. A realtime feed is always defined with
    relation to an existing GTFS feed. All the entity ids are resolved with
    respect to the GTFS feed. Note that "required" and "optional" as stated in
    this file refer to Protocol Buffer cardinality, not semantic cardinality.
    See reference.md at https://github.com/google/transit/tree/master/gtfs-
    realtime for field semantic cardinality.
    """

    # Metadata about this feed and feed message.
    header: "FeedHeader" = betterproto.message_field(1)
    # Contents of the feed.
    entity: List["FeedEntity"] = betterproto.message_field(2)


@dataclass
class FeedHeader(betterproto.Message):
    """Metadata about a feed, included in feed messages."""

    # Version of the feed specification. The current version is 2.0.
    gtfs_realtime_version: str = betterproto.string_field(1)
    incrementality: "FeedHeaderIncrementality" = betterproto.enum_field(2)
    # This timestamp identifies the moment when the content of this feed has been
    # created (in server time). In POSIX time (i.e., number of seconds since
    # January 1st 1970 00:00:00 UTC).
    timestamp: int = betterproto.uint64_field(3)


@dataclass
class FeedEntity(betterproto.Message):
    """A definition (or update) of an entity in the transit feed."""

    # The ids are used only to provide incrementality support. The id should be
    # unique within a FeedMessage. Consequent FeedMessages may contain
    # FeedEntities with the same id. In case of a DIFFERENTIAL update the new
    # FeedEntity with some id will replace the old FeedEntity with the same id
    # (or delete it - see is_deleted below). The actual GTFS entities (e.g.
    # stations, routes, trips) referenced by the feed must be specified by
    # explicit selectors (see EntitySelector below for more info).
    id: str = betterproto.string_field(1)
    # Whether this entity is to be deleted. Relevant only for incremental
    # fetches.
    is_deleted: bool = betterproto.bool_field(2)
    # Data about the entity itself. Exactly one of the following fields must be
    # present (unless the entity is being deleted).
    trip_update: "TripUpdate" = betterproto.message_field(3)
    vehicle: "VehiclePosition" = betterproto.message_field(4)
    alert: "Alert" = betterproto.message_field(5)


@dataclass
class TripUpdate(betterproto.Message):
    """
    Realtime update of the progress of a vehicle along a trip. Depending on the
    value of ScheduleRelationship, a TripUpdate can specify: - A trip that
    proceeds along the schedule. - A trip that proceeds along a route but has
    no fixed schedule. - A trip that have been added or removed with regard to
    schedule. The updates can be for future, predicted arrival/departure
    events, or for past events that already occurred. Normally, updates should
    get more precise and more certain (see uncertainty below) as the events
    gets closer to current time. Even if that is not possible, the information
    for past events should be precise and certain. In particular, if an update
    points to time in the past but its update's uncertainty is not 0, the
    client should conclude that the update is a (wrong) prediction and that the
    trip has not completed yet. Note that the update can describe a trip that
    is already completed. To this end, it is enough to provide an update for
    the last stop of the trip. If the time of that is in the past, the client
    will conclude from that that the whole trip is in the past (it is possible,
    although inconsequential, to also provide updates for preceding stops).
    This option is most relevant for a trip that has completed ahead of
    schedule, but according to the schedule, the trip is still proceeding at
    the current time. Removing the updates for this trip could make the client
    assume that the trip is still proceeding. Note that the feed provider is
    allowed, but not required, to purge past updates - this is one case where
    this would be practically useful.
    """

    # The Trip that this message applies to. There can be at most one TripUpdate
    # entity for each actual trip instance. If there is none, that means there is
    # no prediction information available. It does *not* mean that the trip is
    # progressing according to schedule.
    trip: "TripDescriptor" = betterproto.message_field(1)
    # Additional information on the vehicle that is serving this trip.
    vehicle: "VehicleDescriptor" = betterproto.message_field(3)
    # Updates to StopTimes for the trip (both future, i.e., predictions, and in
    # some cases, past ones, i.e., those that already happened). The updates must
    # be sorted by stop_sequence, and apply for all the following stops of the
    # trip up to the next specified one. Example 1: For a trip with 20 stops, a
    # StopTimeUpdate with arrival delay and departure delay of 0 for
    # stop_sequence of the current stop means that the trip is exactly on time.
    # Example 2: For the same trip instance, 3 StopTimeUpdates are provided: -
    # delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 -
    # delay of unspecified duration for stop_sequence 10 This will be interpreted
    # as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9
    # have delay of 1 min. - stop_sequences 10,... have unknown delay.
    stop_time_update: List["TripUpdateStopTimeUpdate"] = betterproto.message_field(2)
    # Moment at which the vehicle's real-time progress was measured. In POSIX
    # time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC).
    timestamp: int = betterproto.uint64_field(4)
    # The current schedule deviation for the trip.  Delay should only be
    # specified when the prediction is given relative to some existing schedule
    # in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is
    # late) or negative (meaning that the vehicle is ahead of schedule). Delay of
    # 0 means that the vehicle is exactly on time. Delay information in
    # StopTimeUpdates take precedent of trip-level delay information, such that
    # trip-level delay is only propagated until the next stop along the trip with
    # a StopTimeUpdate delay value specified. Feed providers are strongly
    # encouraged to provide a TripUpdate.timestamp value indicating when the
    # delay value was last updated, in order to evaluate the freshness of the
    # data. NOTE: This field is still experimental, and subject to change. It may
    # be formally adopted in the future.
    delay: int = betterproto.int32_field(5)


@dataclass
class TripUpdateStopTimeEvent(betterproto.Message):
    """
    Timing information for a single predicted event (either arrival or
    departure). Timing consists of delay and/or estimated time, and
    uncertainty. - delay should be used when the prediction is given relative
    to some   existing schedule in GTFS. - time should be given whether there
    is a predicted schedule or not. If   both time and delay are specified,
    time will take precedence   (although normally, time, if given for a
    scheduled trip, should be   equal to scheduled time in GTFS + delay).
    Uncertainty applies equally to both time and delay. The uncertainty roughly
    specifies the expected error in true delay (but note, we don't yet define
    its precise statistical meaning). It's possible for the uncertainty to be
    0, for example for trains that are driven under computer timing control.
    """

    # Delay (in seconds) can be positive (meaning that the vehicle is late) or
    # negative (meaning that the vehicle is ahead of schedule). Delay of 0 means
    # that the vehicle is exactly on time.
    delay: int = betterproto.int32_field(1)
    # Event as absolute time. In Unix time (i.e., number of seconds since January
    # 1st 1970 00:00:00 UTC).
    time: int = betterproto.int64_field(2)
    # If uncertainty is omitted, it is interpreted as unknown. If the prediction
    # is unknown or too uncertain, the delay (or time) field should be empty. In
    # such case, the uncertainty field is ignored. To specify a completely
    # certain prediction, set its uncertainty to 0.
    uncertainty: int = betterproto.int32_field(3)


@dataclass
class TripUpdateStopTimeUpdate(betterproto.Message):
    """
    Realtime update for arrival and/or departure events for a given stop on a
    trip. Updates can be supplied for both past and future events. The producer
    is allowed, although not required, to drop past events.
    """

    # Must be the same as in stop_times.txt in the corresponding GTFS feed.
    stop_sequence: int = betterproto.uint32_field(1)
    # Must be the same as in stops.txt in the corresponding GTFS feed.
    stop_id: str = betterproto.string_field(4)
    arrival: "TripUpdateStopTimeEvent" = betterproto.message_field(2)
    departure: "TripUpdateStopTimeEvent" = betterproto.message_field(3)
    schedule_relationship: "TripUpdateStopTimeUpdateScheduleRelationship" = (
        betterproto.enum_field(5)
    )


@dataclass
class VehiclePosition(betterproto.Message):
    """Realtime positioning information for a given vehicle."""

    # The Trip that this vehicle is serving. Can be empty or partial if the
    # vehicle can not be identified with a given trip instance.
    trip: "TripDescriptor" = betterproto.message_field(1)
    # Additional information on the vehicle that is serving this trip.
    vehicle: "VehicleDescriptor" = betterproto.message_field(8)
    # Current position of this vehicle.
    position: "Position" = betterproto.message_field(2)
    # The stop sequence index of the current stop. The meaning of
    # current_stop_sequence (i.e., the stop that it refers to) is determined by
    # current_status. If current_status is missing IN_TRANSIT_TO is assumed.
    current_stop_sequence: int = betterproto.uint32_field(3)
    # Identifies the current stop. The value must be the same as in stops.txt in
    # the corresponding GTFS feed.
    stop_id: str = betterproto.string_field(7)
    # The exact status of the vehicle with respect to the current stop. Ignored
    # if current_stop_sequence is missing.
    current_status: "VehiclePositionVehicleStopStatus" = betterproto.enum_field(4)
    # Moment at which the vehicle's position was measured. In POSIX time (i.e.,
    # number of seconds since January 1st 1970 00:00:00 UTC).
    timestamp: int = betterproto.uint64_field(5)
    congestion_level: "VehiclePositionCongestionLevel" = betterproto.enum_field(6)
    occupancy_status: "VehiclePositionOccupancyStatus" = betterproto.enum_field(9)


@dataclass
class Alert(betterproto.Message):
    """
    An alert, indicating some sort of incident in the public transit network.
    """

    # Time when the alert should be shown to the user. If missing, the alert will
    # be shown as long as it appears in the feed. If multiple ranges are given,
    # the alert will be shown during all of them.
    active_period: List["TimeRange"] = betterproto.message_field(1)
    # Entities whose users we should notify of this alert.
    informed_entity: List["EntitySelector"] = betterproto.message_field(5)
    cause: "AlertCause" = betterproto.enum_field(6)
    effect: "AlertEffect" = betterproto.enum_field(7)
    # The URL which provides additional information about the alert.
    url: "TranslatedString" = betterproto.message_field(8)
    # Alert header. Contains a short summary of the alert text as plain-text.
    header_text: "TranslatedString" = betterproto.message_field(10)
    # Full description for the alert as plain-text. The information in the
    # description should add to the information of the header.
    description_text: "TranslatedString" = betterproto.message_field(11)


@dataclass
class TimeRange(betterproto.Message):
    """
    A time interval. The interval is considered active at time 't' if 't' is
    greater than or equal to the start time and less than the end time.
    """

    # Start time, in POSIX time (i.e., number of seconds since January 1st 1970
    # 00:00:00 UTC). If missing, the interval starts at minus infinity.
    start: int = betterproto.uint64_field(1)
    # End time, in POSIX time (i.e., number of seconds since January 1st 1970
    # 00:00:00 UTC). If missing, the interval ends at plus infinity.
    end: int = betterproto.uint64_field(2)


@dataclass
class Position(betterproto.Message):
    """A position."""

    # Degrees North, in the WGS-84 coordinate system.
    latitude: float = betterproto.float_field(1)
    # Degrees East, in the WGS-84 coordinate system.
    longitude: float = betterproto.float_field(2)
    # Bearing, in degrees, clockwise from North, i.e., 0 is North and 90 is East.
    # This can be the compass bearing, or the direction towards the next stop or
    # intermediate location. This should not be direction deduced from the
    # sequence of previous positions, which can be computed from previous data.
    bearing: float = betterproto.float_field(3)
    # Odometer value, in meters.
    odometer: float = betterproto.double_field(4)
    # Momentary speed measured by the vehicle, in meters per second.
    speed: float = betterproto.float_field(5)


@dataclass
class TripDescriptor(betterproto.Message):
    """
    A descriptor that identifies an instance of a GTFS trip, or all instances
    of a trip along a route. - To specify a single trip instance, the trip_id
    (and if necessary,   start_time) is set. If route_id is also set, then it
    should be same as one   that the given trip corresponds to. - To specify
    all the trips along a given route, only the route_id should be   set. Note
    that if the trip_id is not known, then stop sequence ids in   TripUpdate
    are not sufficient, and stop_ids must be provided as well. In   addition,
    absolute arrival/departure times must be provided.
    """

    # The trip_id from the GTFS feed that this selector refers to. For non
    # frequency-based trips, this field is enough to uniquely identify the trip.
    # For frequency-based trip, start_time and start_date might also be
    # necessary.
    trip_id: str = betterproto.string_field(1)
    # The route_id from the GTFS that this selector refers to.
    route_id: str = betterproto.string_field(5)
    # The direction_id from the GTFS feed trips.txt file, indicating the
    # direction of travel for trips this selector refers to. This field is still
    # experimental, and subject to change. It may be formally adopted in the
    # future.
    direction_id: int = betterproto.uint32_field(6)
    # The initially scheduled start time of this trip instance. When the trip_id
    # corresponds to a non-frequency-based trip, this field should either be
    # omitted or be equal to the value in the GTFS feed. When the trip_id
    # corresponds to a frequency-based trip, the start_time must be specified for
    # trip updates and vehicle positions. If the trip corresponds to
    # exact_times=1 GTFS record, then start_time must be some multiple (including
    # zero) of headway_secs later than frequencies.txt start_time for the
    # corresponding time period. If the trip corresponds to exact_times=0, then
    # its start_time may be arbitrary, and is initially expected to be the first
    # departure of the trip. Once established, the start_time of this frequency-
    # based trip should be considered immutable, even if the first departure time
    # changes -- that time change may instead be reflected in a StopTimeUpdate.
    # Format and semantics of the field is same as that of
    # GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35.
    start_time: str = betterproto.string_field(2)
    # The scheduled start date of this trip instance. Must be provided to
    # disambiguate trips that are so late as to collide with a scheduled trip on
    # a next day. For example, for a train that departs 8:00 and 20:00 every day,
    # and is 12 hours late, there would be two distinct trips on the same time.
    # This field can be provided but is not mandatory for schedules in which such
    # collisions are impossible - for example, a service running on hourly
    # schedule where a vehicle that is one hour late is not considered to be
    # related to schedule anymore. In YYYYMMDD format.
    start_date: str = betterproto.string_field(3)
    schedule_relationship: "TripDescriptorScheduleRelationship" = (
        betterproto.enum_field(4)
    )


@dataclass
class VehicleDescriptor(betterproto.Message):
    """Identification information for the vehicle performing the trip."""

    # Internal system identification of the vehicle. Should be unique per
    # vehicle, and can be used for tracking the vehicle as it proceeds through
    # the system.
    id: str = betterproto.string_field(1)
    # User visible label, i.e., something that must be shown to the passenger to
    # help identify the correct vehicle.
    label: str = betterproto.string_field(2)
    # The license plate of the vehicle.
    license_plate: str = betterproto.string_field(3)


@dataclass
class EntitySelector(betterproto.Message):
    """A selector for an entity in a GTFS feed."""

    # The values of the fields should correspond to the appropriate fields in the
    # GTFS feed. At least one specifier must be given. If several are given, then
    # the matching has to apply to all the given specifiers.
    agency_id: str = betterproto.string_field(1)
    route_id: str = betterproto.string_field(2)
    # corresponds to route_type in GTFS.
    route_type: int = betterproto.int32_field(3)
    trip: "TripDescriptor" = betterproto.message_field(4)
    stop_id: str = betterproto.string_field(5)


@dataclass
class TranslatedString(betterproto.Message):
    """
    An internationalized message containing per-language versions of a snippet
    of text or a URL. One of the strings from a message will be picked up. The
    resolution proceeds as follows: 1. If the UI language matches the language
    code of a translation,    the first matching translation is picked. 2. If a
    default UI language (e.g., English) matches the language code of a
    translation, the first matching translation is picked. 3. If some
    translation has an unspecified language code, that translation is
    picked.
    """

    # At least one translation must be provided.
    translation: List["TranslatedStringTranslation"] = betterproto.message_field(1)


@dataclass
class TranslatedStringTranslation(betterproto.Message):
    # A UTF-8 string containing the message.
    text: str = betterproto.string_field(1)
    # BCP-47 language code. Can be omitted if the language is unknown or if no
    # i18n is done at all for the feed. At most one translation is allowed to
    # have an unspecified language tag.
    language: str = betterproto.string_field(2)
