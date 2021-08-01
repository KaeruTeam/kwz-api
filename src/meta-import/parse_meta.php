<?php
require 'class.kwzParser.php';

$password = trim(fopen("password.txt", "r"))
$conn_string = "host=localhost port=5432 dbname=flipnotes user=meta_import password = " . $password;
$db_conn = pg_connect($conn_string);

pg_prepare($db_conn, "meta_query",
           "insert into meta(
            lock,
            loop,
            flags,
            layer_flags,
            app_version,
            frame_count,
            frame_speed,
            thumb_index,
            modified_timestamp,
            created_timestamp,
            num_camera_frames,
            camera_flags_mask,
            frame_flags_mask,
            root_username,
            root_fsid,
            root_filename,
            parent_username,
            parent_fsid,
            parent_filename,
            current_username,
            current_fsid,
            current_filename,
            track_frame_speed,
            bgm_used,
            se1_used,
            se2_used,
            se3_used,
            se4_used,
            bgm_digest,
            se1_digest,
            se2_digest,
            se3_digest,
            se4_digest
            ) values (
            $1, $2, $3, $4, $5, $6, $7, $8, $9,
            $10, $11, $12, $13, $14, $15, $16, $17,
            $18, $19, $20, $21, $22, $23, $24, $25,
            $26, $27, $28, $29, $30, $31, $32, $33)");

$file_paths = file("files.txt");

foreach ($file_paths as $file) {
    $data = file_get_contents(trim($file));
    $kwz = new kwzParser($data);
    $meta = $kwz->getMeta();

    pg_execute($db_conn, "meta_query", array(
               $meta["lock"] ? "true" : "false",
               $meta["loop"] ? "true" : "false",
               strval($meta["flags"]),
               strval($meta["layer_flags"]),
               strval($meta["app_version"]),
               strval($meta["frame_count"]),
               strval($meta["frame_speed"]),
               strval($meta["thumb_index"]),
               strval($meta["modified_timestamp"]),
               strval($meta["created_timestamp"]),
               strval($meta["num_camera_frames"]),
               strval($meta["camera_flags_mask"]),
               strval($meta["frame_flags_mask"]),
               $meta["root_username"],
               $meta["root_fsid"],
               $meta["root_filename"],
               $meta["parent_username"],
               $meta["parent_fsid"],
               $meta["parent_filename"],
               $meta["current_username"],
               $meta["current_fsid"],
               $meta["current_filename"],
               strval($meta["track_frame_speed"]),
               $meta["bgm_used"] ? "true" : "false",
               $meta["se1_used"] ? "true" : "false",
               $meta["se2_used"] ? "true" : "false",
               $meta["se3_used"] ? "true" : "false",
               $meta["se4_used"] ? "true" : "false",
               $meta["bgm_digest"],
               $meta["se1_digest"],
               $meta["se2_digest"],
               $meta["se3_digest"],
               $meta["se4_digest"]));
}
