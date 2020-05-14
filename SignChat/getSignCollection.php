<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";

$signCollection = array();
if(isset($_REQUEST['collectionId'])) {
    $collectionId = $_REQUEST['collectionId'];
    $sql = "SELECT * FROM signcollection WHERE signcollection.collectionId = '$collectionId'";

    $rs = mysqli_query($conn, $sql);
    while($rc = mysqli_fetch_assoc($rs)) {
        $signCollection['collectionId'] = $collectionId;
        $signCollection['name'] = $rc['name'];
        $signCollection['organisationId'] = $rc['organisationId'];

        $signCollection['contactPerson'] = $rc['contactPerson'];
        $signCollection['contactPersonEmail'] = $rc['contactPersonEmail'];
        $signCollection['contactPersonTel'] = $rc['contactPersonTel'];
        $signCollection['contactPersonTitle'] = $rc['contactPersonTitle'];
        $signCollection['signs'] = array();
        

        $sql = "SELECT meaning,COUNT(*) as num FROM sign WHERE collectionId = '$collectionId' GROUP BY meaning ORDER BY meaning";
        $rs1 = mysqli_query($conn, $sql);
        $signs = array();
        while($rc1 = mysqli_fetch_assoc($rs1)) {
            $signs['meaning'] = $rc1['meaning'];
            $signs['noOfDataset'] = $rc1['num'];
            $signCollection['signs'][] = $signs;
        }
        
    }
}

echo json_encode($signCollection);

?>