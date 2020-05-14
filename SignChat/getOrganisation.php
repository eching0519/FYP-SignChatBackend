<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";

$organisation = array();
if(isset($_REQUEST['organisationId'])) {
    $organisationId = $_REQUEST['organisationId'];
    $sql = "SELECT organisation.name, organisation.email, organisation.address, organisation.tel, COUNT(signcollection.collectionId) AS 'collectionCount' FROM organisation,signcollection WHERE signcollection.organisationId = organisation.id AND organisation.id = $organisationId";

    $rs = mysqli_query($conn, $sql);
    while($rc = mysqli_fetch_assoc($rs)) {
        $organisation['organisationId'] = $organisationId;
        $organisation['name'] = $rc['name'];
        $organisation['email'] = $rc['email'];
        $organisation['address'] = $rc['address'];
        $organisation['tel'] = $rc['tel'];
        $organisation['collectionCount'] = $rc['collectionCount'];
    }
}

echo json_encode($organisation);

?>