<!DOCTYPE html>
<html>
<head>
  <title>Source Database Information</title>
</head>
<body>
  <?php
    $conn = pg_connect("host=localhost port=5432 dbname=data_warehouse user=postgres password=postgres");
    $sql = "SELECT * FROM metric;";
    $result = pg_query($conn, $sql);
    $resultCheck = pg_num_rows($result);
    if ($resultCheck > 0) {
      while ($row = pg_fetch_assoc($result)) {
        echo "metric_uid: " . $row['metric_uid'] . "<br>";
        echo "source_uid: " . $row['source_uid'] . "<br>";
        echo "data_type: " . $row['data_type'] . "<br>";
        echo "units: " . $row['units'] . "<br>";
        echo "name: " . $row['name'] . "<br>";
        echo "asc: " . $row['asc'] . "<br>";
        echo "<br>";
      }
    }
  ?>
</body>
</html>
