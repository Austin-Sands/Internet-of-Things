<?php
$servername = "localhost";
$username = "austin-sands";
$password = "gardenpi_6551";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?>
