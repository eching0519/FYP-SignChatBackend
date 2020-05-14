<?php
header('Content-Type: application/json; charset=utf-8');
require_once "connection/mysqli_conn.php";


if(isset($_POST["sign"])) {
    $sign_json = $_POST["sign"];
    $sign = json_decode($sign_json);
    if(isset($_SESSION['collectionId'])) {
        $collectionId = $_SESSION['collectionId'];
    } else {
        $collectionId = $sign->collectionId;
    }
    $meaning = $sign->meaning;
    $camera_x = $sign->camera_x;
    $camera_y = $sign->camera_y;
    $camera_z = ($sign->camera_z)-20;
    $frames_arr = $sign->frames;

    $sql = "INSERT INTO sign (signId, collectionId, meaning) VALUES (NULL, '$collectionId', '$meaning')";
    if (mysqli_query($conn,$sql) === TRUE) {
        $last_id = $conn->insert_id;

        $sql = "";
        for ($i = 0; $i < count($frames_arr); $i++) {
            $sequenceNo = $i;
            $hands_arr = $frames_arr[$i]->hands;

            $fieldNames = "signId, sequenceNo";
            $frameValue = "$last_id, $sequenceNo";
            if(count($hands_arr) > 0) {
                for ($j = 0; $j < count($hands_arr); $j++) {
                    $point_dic = $hands_arr[$j];
                    $pointName = $point_dic->pointName;
                    $x = ($point_dic->x) - $camera_x;
                    $y = ($point_dic->y) - $camera_y;
                    $z = ($point_dic->z) - $camera_z;
                    $fieldNames .= ", " . $pointName . "_x, " . $pointName . "_y, " . $pointName . "_z";
                    $frameValue .= ", " . $x . ", " . $y . ", " . $z;
                }
            } else {
                $fieldNames .= ", left_0_x, left_0_y, left_0_z, left_1_x, left_1_y, left_1_z, left_2_x, left_2_y, left_2_z, left_3_x, left_3_y, left_3_z, left_4_x, left_4_y, left_4_z, left_5_x, left_5_y, left_5_z, left_6_x, left_6_y, left_6_z, left_7_x, left_7_y, left_7_z, left_8_x, left_8_y, left_8_z, left_9_x, left_9_y, left_9_z, left_10_x, left_10_y, left_10_z, left_11_x, left_11_y, left_11_z, left_12_x, left_12_y, left_12_z, left_13_x, left_13_y, left_13_z, left_14_x, left_14_y, left_14_z, left_15_x, left_15_y, left_15_z, left_16_x, left_16_y, left_16_z, left_17_x, left_17_y, left_17_z, left_18_x, left_18_y, left_18_z, left_19_x, left_19_y, left_19_z, left_20_x, left_20_y, left_20_z, right_0_x, right_0_y, right_0_z, right_1_x, right_1_y, right_1_z, right_2_x, right_2_y, right_2_z, right_3_x, right_3_y, right_3_z, right_4_x, right_4_y, right_4_z, right_5_x, right_5_y, right_5_z, right_6_x, right_6_y, right_6_z, right_7_x, right_7_y, right_7_z, right_8_x, right_8_y, right_8_z, right_9_x, right_9_y, right_9_z, right_10_x, right_10_y, right_10_z, right_11_x, right_11_y, right_11_z, right_12_x, right_12_y, right_12_z, right_13_x, right_13_y, right_13_z, right_14_x, right_14_y, right_14_z, right_15_x, right_15_y, right_15_z, right_16_x, right_16_y, right_16_z, right_17_x, right_17_y, right_17_z, right_18_x, right_18_y, right_18_z, right_19_x, right_19_y, right_19_z, right_20_x, right_20_y, right_20_z";
                $frameValue .= ",NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL ,NULL";
            }
            $sql .= "INSERT INTO frame ($fieldNames) VALUES ($frameValue);";
        }

        if ($conn->multi_query($sql) === TRUE) {
            $message = array("message"=>"Your sign has been saved.", "title"=>"Success", "collectionId"=>$collectionId);
            echo json_encode($message);
        } else {
            $message = array("message"=>$conn->error,"title"=>"Error");
            echo json_encode($message);

            $sql = "DELETE FROM frame WHERE signId = $last_id;";
            $sql .= "DELETE FROM sign WHERE signId = $last_id;";
            $conn->multi_query($sql);
        }
    } else {
        $message = array("message"=>$conn->error,"title"=>"Error");
        echo json_encode($message);
    }

} else {
    $message = array("message"=>"No data is received.","title"=>"Fail");
    echo json_encode($message);
}
mysqli_close($conn);
?>