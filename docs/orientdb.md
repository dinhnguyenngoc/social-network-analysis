# Tìm hiểu đặt tính của OrientDB, cách thức cài đặt và kết nối
Dũng, Nghĩa



Run docker image

```docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=root orientdb:latest```

Với lastest version thì dy2ng pyorient sẽ gặp error như bên dưới

```pyorient.exceptions.PyOrientWrongProtocolVersionException: Protocol version 38 is not supported yet by this client.```

Giải pháp: downgrade version của OrientDB xuống

```docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=123 orientdb:2.2.35```

*Nghĩa tìm giải pháp dùng thư viện pyorientdb, do community đã khắc phục được lỗi trên, đã connect được đến server VPS của Nghĩa setup*