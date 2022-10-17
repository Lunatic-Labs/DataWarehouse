<!DOCTYPE html>
<html>
<head>
  <title>Source Database Information</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <?php
    $conn = pg_connect("host=localhost port=5432 dbname=data_warehouse user=postgres password=postgres");

    $sql = "SELECT * FROM \"group\";";
    echo "<h3>----------------------------------GROUP TABLE----------------------------------</h3>" . "<br>";
    $result = pg_query($conn, $sql);
    $resultCheck = pg_num_rows($result);
    if ($resultCheck > 0) {
      while ($row = pg_fetch_assoc($result)) {
        echo "name: "           . $row['name']           . "<br>";
        echo "location: "       . $row['location']       . "<br>";
        echo "classification: " . $row['classification'] . "<br>";
        echo "group_uid: "      . $row['group_uid']      . "<br>";
        echo "<br>";
      }
    }

    $sql = "SELECT * FROM source;";
    echo "<h3>----------------------------------SOURCE TABLE----------------------------------</h3>" . "<br>";
    $result = pg_query($conn, $sql);
    $resultCheck = pg_num_rows($result);
    if ($resultCheck > 0) {
      while ($row = pg_fetch_assoc($result)) {
        echo "source_uid: " . $row['source_uid'] . "<br>";
        echo "name: "       . $row['name']       . "<br>";
        echo "group_uid: "  . $row['group_uid']  . "<br>";
        echo "tz_info: "    . $row['tz_info']    . "<br>";
        echo "<br>";
      }
    }

    $sql = "SELECT * FROM metric;";
    echo "<h3>----------------------------------METRIC TABLE----------------------------------</h3>" . "<br>";
    $result = pg_query($conn, $sql);
    $resultCheck = pg_num_rows($result);
    if ($resultCheck > 0) {
        while ($row = pg_fetch_assoc($result)) {
            echo "metric_uid: " . $row['metric_uid'] . "<br>";
            echo "source_uid: " . $row['source_uid'] . "<br>";
            echo "data_type: "  . $row['data_type']  . "<br>";
            echo "units: "      . $row['units']      . "<br>";
            echo "name: "       . $row['name']       . "<br>";
            echo "asc: "        . $row['asc']        . "<br>";
            echo "<br>";
        }
    }

    // Go through the database and make a list of all of the tablenames that are not metric, source, or group.
    $tables= "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name != 'metric' AND table_name != 'source' AND table_name != 'group';";
    // print the tablenames
    echo "<h3>----------------------------------CREATED TABLES----------------------------------</h3>" . "<br>";
    $result = pg_query($conn, $tables);
    $resultCheck = pg_num_rows($result);
    if ($resultCheck > 0) {
      while ($row = pg_fetch_assoc($result)) {
        echo $row['table_name'] . "<br>";
      }
    }
  ?>
</body>
</html>
