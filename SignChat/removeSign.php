<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";

session_start();
if (isset($_SESSION['collectionId'])) {
    $collectionId = $_SESSION['collectionId'];
    if (isset($_REQUEST['signId'])) {
        $signId = $_REQUEST['signId'];

        $sql = "SELECT meaning FROM sign WHERE signId = $signId AND collectionId = '$collectionId'";
        $rs = mysqli_query($conn, $sql);
        if ($rc = mysqli_fetch_assoc($rs)) {
            $meaning = $rc['meaning'];

            $sql = "DELETE FROM frame WHERE signId = $signId;";
            $sql .= "DELETE FROM sign WHERE signId = $signId;";
            mysqli_multi_query($conn,$sql);

            if (mysqli_affected_rows($conn)>0) {
                echo json_encode(array("meaning"=>$meaning,"collectionId"=>$collectionId));
            } else {
                $message = array("message" => "No sign is removed.");
                echo json_encode($message);
            }
        } else {
            $message = array("message" => "The sign is not exist.");
            echo json_encode($message);
        }
    } else {
        $message = array("message" => "Sign ID is not set.");
        echo json_encode($message);
    }
} else {
    $message = array("message" => "Please login.");
    echo json_encode($message);
}

mysqli_close($conn);
