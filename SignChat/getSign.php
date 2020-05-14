<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";

session_start();
if(isset($_SESSION['collectionId'])) {
    $collectionId = $_SESSION['collectionId'];
    $collectionName = $_SESSION['name'];

    $sql = "SELECT meaning,COUNT(*) FROM sign WHERE collectionId = '$collectionId' GROUP BY meaning ORDER BY meaning";
    $rs = mysqli_query($conn,$sql);

    $sign_arr = array();
    while($rc = mysqli_fetch_assoc($rs)) {
        $sign_arr[] = array("meaning"=>$rc['meaning'], "count"=>$rc['COUNT(*)']);
    }
    echo json_encode(array("name"=>$collectionName,"sign"=>$sign_arr));
        
} else {
    $message = array("message"=>"Session timeout. Please login again.");
    echo json_encode($message);
}

mysqli_close($conn);
?>