# DSi Library DB Details
This page details everything about the database table the for Flipnote Gallery: DSi Library flipnotes.

# Columns

| Name | Type | Description |
|---|---|---|
| lock | boolean | If the flipnote is locked |
| loop | boolean | If the flipnote is to be looped |
| flags | smallint | [Click for details](https://github.com/Flipnote-Collective/flipnote-studio-3d-docs/wiki/kwz-format#kfh-flags) |
| layer_flags | smallint | [Click for details](https://github.com/Flipnote-Collective/flipnote-studio-3d-docs/wiki/kwz-format#layer-visibility-flags) |
| app_version | smallint | Assumed to be app version, seen as: `0`, `1`, and `3` |
| frame_count | smallint | The number of frames in the flipnote |
| frame_speed | smallint | The [frame speed value array](https://github.com/Flipnote-Collective/flipnote-studio-3d-docs/wiki/kwz-format#flipnote-playback-speeds) index |
| thumb_index | smallint | The frame index that the thumbnail is derived from |
| modified_timestamp | bigint | The number of seconds since the unix epoch of the when the flipnote was last modified |
| root_username | text | The username of the original flipnote's creator |
| root_fsid | text | The KWZ format FSID of the original flipnote's creator |
| root_fsid_ppm | text | The PPM format FSID of the original flipnote's creator |
| root_filename | text | The KWZ file name of the original flipnote |
| parent_username | text | The username of the parent flipnote's creator |
| parent_fsid | text | The KWZ format FSID of the parent flipnote's creator |
| parent_fsid_ppm | text | The PPM format FSID of the parent flipnote's creator |
| parent_filename | text | The KWZ format file name of the parent flipnote |
| current_username | text | The username of the current flipnote's creator |
| current_fsid | text | The KWZ format FSID of the current flipnote's creator |
| current_fsid_ppm | text | The PPM format FSID of the current flipnote's creator |
| current_filename | text | The file name of the current flipnote |
| track_frame_speed | smallint | Flipnote speed when the track was recorded |
| bgm_used | boolean | If the BGM track is used in the flipnote |
| se1_used | boolean |  |
| se2_used | boolean |  |
| se3_used | boolean |  |
| bgm_digest | text | The MD5 digest of the BGM track. `null` if it isn't used |
| se1_digest | text |  |
| se2_digest | text |  |
| se3_digest | text |  |

# Rows

Each row represents 1 flipnote file from the DSi Library S3 bucket
