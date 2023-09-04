from assets.transit_realtime import  FeedMessage, FeedHeader, FeedEntity, TripUpdate, TripUpdateStopTimeUpdate, TripUpdateStopTimeEvent, VehiclePosition, VehiclePositionOccupancyStatus, VehiclePositionVehicleStopStatus


# Retrieve some realtime data from a json

# Creating the message
new_feed_message = FeedMessage()

# Creating the header
feed_header = FeedHeader()

# Updating the header
feed_header.gtfs_realtime_version = '1'
feed_header.incrementality = 1
# feed_header.timestamp =  1658283241

new_feed_message.header = feed_header
# Initializing a trip update
trip_of_message = TripUpdate()

# Initializing a StoptimeUpdate update
test_stoptime_delay = TripUpdateStopTimeUpdate()

# Updating the trip info
trip_of_message.trip.trip_id = '1'
trip_of_message.trip.route_id = '1'

# Serializing to bytes
print('Serialized TripUpdate ', bytes(trip_of_message))

# Updating the StoptimeUpdate delay
test_stoptime_delay.arrival.delay= 5

print('Serialized StoptimeUpdate ', bytes(test_stoptime_delay))

trip_of_message.stop_time_update.append(test_stoptime_delay)

print('Serialized TripUpdate with StoptimeUpdate ', bytes(trip_of_message))


# Initializing a VehiclePosition update
vehicle_position = VehiclePosition()

# Updating the VehiclePosition info
vehicle_position.trip.trip_id = '1'
vehicle_position.trip.route_id = '1'

vehicle_position.congestion_level = 3
vehicle_position.current_status = 4

vehicle_position.position.latitude = 38.009984
vehicle_position.position.longitude = 23.80153310

# meters per second
vehicle_position.position.speed = 30

print(vehicle_position)

# Creating a new entity to be added
new_feed_entity = FeedEntity()
new_feed_entity.id = '1'
new_feed_entity.trip_update = trip_of_message
# new_feed_entity.vehicle = vehicle_position

new_feed_message.entity = new_feed_entity
print('message to send to google', new_feed_message.SerializeToString())