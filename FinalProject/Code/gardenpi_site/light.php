<!doctype html>

<!--
 TITLE:             light.php
 AUTHOR:            Austin Sands (ANS)
 CREATE DATE:       04/13/2023
 PURPOSE:           This page will display all data for light readings
-->

<html lang="en">
<head>

	<meta charset="utf-8">

	<title>GardenPi - Light Data</title>
	
    <link rel="stylesheet" href="css/data.css">	

</head>

<body>
<!-- php script to pull light data from database -->
<?php
	$servername = "localhost";
	$username = "austin-sands";
	$password = "gardenpi_6551";
	$database = "gardenpidb";

	try {
		$conn = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
		$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		//echo "Connected Succesfully";

        $stmt = $conn->query("SELECT * FROM light_data");

        if($stmt === false) {
            die("Error - No data");
        }

        $result = $stmt->fetchAll();

        $total_records = count($result);
        $last_record_index = $total_records - 1;
        $per_page = 25;
        $final_page = ceil($total_records / $per_page);

        if(isset($_GET["page"]) && ($_GET["page"] <= $final_page) && ($_GET["page"] > 0)) {
            $page = $_GET["page"];
            $first_record = ($per_page) * ($page - 1);
        } else {
            $page = 1;
            $first_record = 0;
        }
        $final_record = $first_record + ($per_page - 1);
        if($final_record > $last_record_index) {
            $final_record = $last_record_index;
        }

        //function to create paging functionality
        function create_pagination($current_page, $final_page) {
            echo '<div class="pagination">';
            if ($current_page > 1) {
                echo '<a href="?page='.($current_page - 1).'"> &lt;&lt;Previous </a>';
            } else { echo "Page $current_page"; }
            echo " - ";
            if ($current_page < $final_page) {
                echo '<a href="?page='.($current_page + 1).'"> Next&gt;&gt; </a>';
            } else { echo $current_page; }
            echo '</div>';
        }

    } catch(PDOException $e) {
		echo "Connection failed: " . $e->getMessage();
	}
	?> <!-- end php script -->

	<div id="header">
		GardenPi - Automated Gardening Solution
	</div>

	<!-- nav bar -->
	<ul id="nav-bar">
		<li><a href="index.php">Home</a></li>
		<li><a href="gallery.php">Gallery</a></li>
		<li><a href="temp.php">Temp Data</a></li>
		<li><a class="active" href="light.php">Light Data</a></li>
		<li><a href="moisture.php">Moisture Data</a></li>
		<li><a href="waterlog.php">Watering Log</a></li>
	</ul>
	<!-- end nav bar -->

	<h1>Light Data</h1>
    <h2>Lower Number = More Light</h2>

	<div class="flex-container">
        <?php create_pagination($page, $final_page); ?>
        <div>
            <table>
                <thead>
                    <tr>
                        <th>EntryID</th>
                        <th>Datetime</th>
                        <th>Reading</th>
                        <th>Manual Read</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                        //display 25 records at a time and create paging 
                        //debug line below
                        //echo "Processing page: $page First Record: $first_record Final Record: $final_record Total Records: $total_records Last Page: $final_page";
                        for ($i = $first_record; $i <= $final_record; $i++) {
                            $record = $result[$i];
                            echo '
                                <tr>
                                    <td>'.$record['EntryID'].'</td>
                                    <td>'.$record['date_time'].'</td>
                                    <td>'.$record['reading'].'</td>
                                    <td>'.$record['manual_read'].'</td>
                                </tr>
                            ';
                        }
                    ?>
                </tbody>
            </table>
        </div>
        <?php create_pagination($page, $final_page); ?>
	</div>

</body>

</html>