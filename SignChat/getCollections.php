<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";

$sql = "SELECT name, sign.collectionId, COUNT(*) AS 'total' FROM signcollection,sign WHERE signcollection.collectionId = sign.collectionId GROUP BY sign.collectionId ORDER BY total DESC";

$rs = mysqli_query($conn, $sql);
$result = array();
while($rc = mysqli_fetch_assoc($rs)) {
    $collectionId = $rc['collectionId'];
    $collectionName = $rc['name'];
    $total = $rc['total'];

    $mlModel = "./ai_model/$collectionId.h5";
    if(file_exists($mlModel)) {
        $result[] = array("collectionId"=>$collectionId, "collectionName"=>$collectionName, "total"=>$total);
    }
}
echo json_encode($result);

mysqli_close($conn);
?>