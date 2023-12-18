<!doctype html>

<!--
 TITLE:             index.php
 AUTHOR:            Austin Sands (ANS)
 CREATE DATE:       04/12/2023
 PURPOSE:           This will serve as the landing page for my Apache server for 
 	my CSCI 43300 final project
-->

<html lang="en">
<head>

	<meta charset="utf-8">

	<title>GardenPi - Austin Sands Final Project</title>
	
    <link rel="stylesheet" href="css/homepage.css">	
</head>

<body>
	<!-- PHP code to fetch data from gardenpi database -->
	<?php
	$servername = "localhost";
	$username = "austin-sands";
	$password = "gardenpi_6551";
	$database = "gardenpidb";

	try {
		$conn = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
		$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		//echo "Connected Succesfully";

		$last_script_run = $conn->query("SELECT date_time FROM temp_data WHERE manual_read = 0 
		ORDER BY EntryID DESC LIMIT 1")->fetch();

		$temp_stmt = $conn->query("SELECT date_time, reading, manual_read FROM temp_data ORDER BY EntryID DESC LIMIT 1");
		$temp_result = $temp_stmt->fetch();
		$temp_date = $temp_result['date_time'];
		$temp_reading = $temp_result['reading'];
		if($temp_result['manual_read'] == 0) {
			$temp_usercall = "False";
		} else { $temp_usercall = "True"; }
		
		$light_stmt = $conn->query("SELECT date_time, reading, manual_read FROM light_data ORDER BY EntryID DESC LIMIT 1");
		$light_result = $light_stmt->fetch();
		$light_date = $light_result['date_time'];
		$light_reading = $light_result['reading'];
		if($light_result['manual_read'] == 0) {
			$light_usercall = "False";
		} else { $light_usercall = "True"; }

		$moisture_stmt = $conn->query("SELECT date_time, reading, manual_read FROM moisture_data ORDER BY EntryID DESC LIMIT 1");
		$moisture_result = $moisture_stmt->fetch();
		$moisture_date = $moisture_result['date_time'];
		if($moisture_result['reading'] == 0) {
			$moisture_reading = "Dry";
		} else { $moisture_reading = "Wet"; }
		if($moisture_result['manual_read'] == 0) {
			$moisture_usercall = "False";
		} else { $moisture_usercall = "True"; }

		$watering_stmt = $conn->query("SELECT date_time, manual_call FROM watering_log ORDER BY EntryID DESC LIMIT 1");
		$watering_result = $watering_stmt->fetch();
		$watering_date = $watering_result['date_time'];
		if($watering_result['manual_call'] == 0) {
			$watering_usercall = "False";
		} else { $watering_usercall = "True"; }

	} catch(PDOException $e) {
		echo "Connection failed: " . $e->getMessage();
	}
	?> <!-- end php script -->

	<div id="header">
		GardenPi - Automated Gardening Solution
	</div>

	<!-- nav bar -->
	<ul id="nav-bar">
		<li><a class="active" href="index.php">Home</a></li>
		<li><a href="gallery.php">Gallery</a></li>
		<li><a href="temp.php">Temp Data</a></li>
		<li><a href="light.php">Light Data</a></li>
		<li><a href="moisture.php">Moisture Data</a></li>
		<li><a href="waterlog.php">Watering Log</a></li>
	</ul>
	<!-- end nav bar -->
	<!-- php script to check for button presses -->
	<?php 
		if(isset($_POST['request'])){
			if($_POST['request'] == 'get_temp') {
				shell_exec('python scripts/get_temp.py');
			} else if($_POST['request'] == 'get_light') {
				shell_exec('python scripts/get_light.py');
			} else if($_POST['request'] == 'get_moisture') {
				shell_exec('python scripts/get_moisture.py');
			} else if($_POST['request'] == 'water_plant') {
				shell_exec('python scripts/water_plant.py');
			}
		}
	?>

	<h1>Last Automatic Script Call: <?php echo $last_script_run['date_time'] ?></h1>
	<div class="flex-container">
		<div id="image-container">	
			<div>	
				Most Recent Picture

				<img src="images/recent.jpg" onerror="this.onerror=null; this.remove();">
			</div>
		</div>

		<div><u>Temp Reading</u><br>
			<?php echo "Datetime: " . $temp_date.
			"<br>Reading: " . $temp_reading.
			"<br>User read: " . $temp_usercall ?>
			<form id="get_temp" method="post">
				<button name="request" value="get_temp" type="submit" >Request Temp Reading</button>
			</form>
		</div>
		<div><u>Light Reading</u><br>
			<?php echo "Datetime: " . $light_date.
			"<br>Reading: " . $light_reading.
			"<br>User read: " . $light_usercall ?>
			<form id="get_light" method="post">
				<button name="request" value="get_light" type="submit">Request Light Reading</button>
			</form>
		</div>
		<div><u>Moisture Reading</u><br>
			<?php echo "Datetime: " . $moisture_date.
			"<br>Reading: " . $moisture_reading.
			"<br>User read: " . $moisture_usercall ?>
			<form id="get_moisture" method="post">
				<button name="request" value="get_moisture" type="submit" >Request Moisture Reading</button>
			</form>
		</div>
		<div><u>Last Watered</u><br>
			<?php echo "Datetime: " . $watering_date.
			"<br>User call: " . $watering_usercall ?>
			<form id="water_plant" method="post">
				<button name="request" value="water_plant" type="submit" >Request Plant Watering</button>
			</form>
		</div>
	</div>
</body>

</html>
