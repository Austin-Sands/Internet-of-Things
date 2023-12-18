<!doctype html>

<!--
 TITLE:             gallery.php
 AUTHOR:            Austin Sands (ANS)
 CREATE DATE:       04/13/2023
 PURPOSE:           This page will display all images taken of the plants growing progress
-->

<html lang="en">
<head>

	<meta charset="utf-8">

	<title>GardenPi - Image Gallery</title>
	
    <link rel="stylesheet" href="css/gallery.css">	

</head>

<body>
	<div id="header">
		GardenPi - Automated Gardening Solution
	</div>

	<!-- nav bar -->
	<ul id="nav-bar">
		<li><a href="index.php">Home</a></li>
		<li><a class="active" href="gallery.php">Gallery</a></li>
		<li><a href="temp.php">Temp Data</a></li>
		<li><a href="light.php">Light Data</a></li>
		<li><a href="moisture.php">Moisture Data</a></li>
		<li><a href="waterlog.php">Watering Log</a></li>
	</ul>
	<!-- end nav bar -->

	<h1>Image Gallery</h1>
	<div class="flex-container">
        <!-- PHP code to fetch images from image directory -->
	    <?php 
        // get images from folder excluding recent.jpg because it's a duplicate
        $directory = "images/";
        $images = preg_grep('/recent\.jpg$/', glob($directory . "*.jpg"), PREG_GREP_INVERT);
        $total_imgs = count($images);
        $last_img_indx = $total_imgs - 1;
        $per_page = 10;
        $final_page = ceil($total_imgs / $per_page);

        if(isset($_GET["page"]) && ($_GET["page"] <= $final_page) && ($_GET["page"] > 0)) {
            $page = $_GET["page"];
            $first_img = ($per_page) * ($page - 1);
        } else {
            $page = 1;
            $first_img = 0;
        }
        $final_img = $first_img + ($per_page - 1);
        if($final_img > $last_img_indx) {
            $final_img = $last_img_indx;
        }

        //display ten images at a time and create paging 
        //echo "Processing page: $page First Image: $first_img Final Image: $final_img Total Images: $total_imgs Last Page: $final_page";
        create_pagination($page, $final_page);
        for ($i = $first_img; $i <= $final_img; $i++) {
            $image = $images[$i];
            $filename = pathinfo($image)['filename'];
            echo '
            <div>
                '.$filename.'<br>
                <img src="'.$image.'">
            </div>
            ';
        }
        create_pagination($page, $final_page);

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

	    ?> <!-- end php script -->
	</div>

</body>

</html>
