<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";

if(isset($_POST['collectionId']) && $_POST['password']) {
    $collectionId = $_POST['collectionId'];
    $password = $_POST['password'];

    $sql = "SELECT * FROM signcollection WHERE collectionId = '$collectionId' AND password = '$password'";
    $rs = mysqli_query($conn, $sql);
    if(mysqli_num_rows($rs)) {
        $rc = mysqli_fetch_assoc($rs);
        $collectionName = $rc['name'];
        session_start();
        $_SESSION['collectionId'] = $collectionId;
        $_SESSION['name'] = $collectionName;
        $message = array("message"=>"success");
    } else {
        $message = array("message"=>"Login fail");
    }
} else {
    $message = array("message"=>"Login fail");
}
echo json_encode($message);

mysqli_close($conn);
?>