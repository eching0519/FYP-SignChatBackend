<?php
$hostname = "localhost";
$username = "root";
$password = "";
$db = "sign_chat";
$conn = mysqli_connect($hostname, $username, $password, $db) or die(mysqli_connect_error());
mysqli_set_charset($conn, "utf8");
?>