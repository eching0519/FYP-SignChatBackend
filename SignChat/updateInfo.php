<?php
require_once "connection/mysqli_conn.php";
session_start();

if (isset($_SESSION['collectionId'])) {

    if(isset($_REQUEST['info'])) {
        $info = json_decode($_REQUEST['info']);

        $organisation = $info->organisation;
        $signcollection = $info->collection;
        $verifyPassword = $info->verifyPassword;

        $collectionId = $signcollection->collectionId;

        // verify password
        $sql = "SELECT * FROM signcollection WHERE collectionId = '$collectionId' AND password = '$verifyPassword'";
        $rs = mysqli_query($conn, $sql);
        if(mysqli_num_rows($rs)) {
            // password is correct
            // update information here
            $collectionName = $signcollection->name;
            $password = $signcollection->password;
            if($password=="") {
                $password = $verifyPassword;
            }
            $contactPerson = $signcollection->contactPerson;
            $contactPersonTitle = $signcollection->contactPersonTitle;
            $contactPersonEmail = $signcollection->contactPersonEmail;
            $contactPersonTel = $signcollection->contactPersonTel;

            $organisationId = $signcollection->organisationId;
            $organisationName = $organisation->name;
            $organisationEmail = $organisation->email;
            $organisationAddress = $organisation->address;
            $organisationTel = $organisation->tel;

            $sql = "UPDATE signcollection SET password = '$password', name = '$collectionName', contactPerson = '$contactPerson', contactPersonEmail = '$contactPersonEmail', contactPersonTel = '$contactPersonTel', contactPersonTitle = '$contactPersonTitle' WHERE collectionId = '$collectionId';";
            $sql .= "UPDATE organisation SET name = '$organisationName', email = '$organisationEmail', address = '$organisationAddress', tel = '$organisationTel' WHERE id = $organisationId;";
            
            mysqli_multi_query($conn,$sql);
        } else {
            echo json_encode(array("message"=>"Current password is incorrect."));
        }
    } else {
        echo json_encode(array("message"=>"Info is not set."));
    }
    
} else {
    echo json_encode(array("message"=>"No session."));
}

?>