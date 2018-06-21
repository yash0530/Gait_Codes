<?php
    // Prepare variables for database connection
    $dbusername = "yash";  // enter database username, I used "arduino" in step 2.2
    $dbpassword = "qwerty123";  // enter database password, I used "arduinotest" in step 2.2

    try{
        $conn = new PDO('mysql:dbname=test;host=localhost',$dbusername,$dbpassword);
        $aX = $_GET["aX"]; $aY = $_GET["aY"]; $aZ = $_GET["aZ"]; $gX = $_GET["gX"]; $gY = $_GET["gY"]; $gZ= $_GET["gZ"]; $time= $_GET["time"];
        $sql = "INSERT INTO `imu_readings` ( `aX`, `aY`, `aZ`, `gX`, `gY`, `gZ`, `time` ) VALUES (:aX, :aY, :aZ, :gX, :gY, :gZ, :time);";
        $stm = $conn->prepare($sql);
        $stm->execute(['aX' => $aX, 'aY' => $aY,'aZ' => $aZ,'gX' => $gX,'gY' => $gY,'gZ' => $gZ, 'time' => $time]);
        echo 'done';
    }
    catch (Exception $e){
        echo $e->getMessage();
    }
?>