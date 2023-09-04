mkdir assets
protoc -I . --python_betterproto_out=assets gtfs-realtime.proto