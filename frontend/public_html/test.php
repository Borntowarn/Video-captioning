<?php
sleep(60);

if($_REQUEST['is_special'] == '1'){
    echo json_encode(array("path"=>'http://pink.cats.kion/assets/video/video1.mp4'));
}else{
    echo json_encode(array("path"=>'http://pink.cats.kion/assets/video/site.mov'));
}