<?php

class kwzParser
{
  protected $data = null;
  protected $offset = 0;
  protected $size = 0;

  public $sections = [];
  public $meta = null;
  public $frameMeta = null;
  public $soundMeta = null;
  public $numCameraFrames = 0;
  public $frameFlagsMask = 0;
  public $cameraFlagsMask = 0;

  private $pubkey = <<<EOT
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuv+zHAXXvbbtRqxADDeJ
ArX2b9RMxj3T+qpRg3FnIE/jeU3tj7eoDzsMduY+D/UT9CSnP+QHYY/vf0n5lqX9
s6ljoZAmyUuruyj1e5Bg+fkDEu/yPEPQjqhbyywCyYL4TEAOJveopUBx9fdQxUJ6
J4J5oCE/Im1kFrlGW+puARiHmt3mmUyNzO8bI/Jx3cGSfoOHJG1foEaQsI5aaKqA
pBqxtzvwqMhudcZtAWSyRMBMlndvkRnVTDNTfTXLOYdHShCIgnKULCTH87uLBIP/
nsmr4/bnQz8q2rp/HyVO+0yjR6mVr0NX5APJQ+6riJmGg3t3VOldhKP7aTHDUW+h
kQIDAQAB
-----END PUBLIC KEY-----
EOT;

  // $data should be KWZ data formatted as a string (such as from file_get_contents())
  public function __construct(string $data)
  {
    if ($data) $this->load($data);
  }

  public function load(string $data)
  {
    $this->offset = 0;
    $this->data = $data;
    $this->size = strlen($data);
    $this->sections = [];
    $this->meta = null;
    $this->frameMeta = null;
    $this->soundMeta = null;
    $this->numCameraFrames = 0;
    $this->frameFlagsMask = 0;
    $this->cameraFlagsMask = 0;
    // Build section table
    $fileSize = $this->size - 256;
    $numSections = 0;
    while (($this->offset < $fileSize) && ($numSections < 6)) {
      $sectionStart = $this->offset;
      $sectionHeader = $this->unpack([
        'type' => 'a3',
        'flags' => 'C',
        'length' => 'V',
      ], 8);
      $this->sections[$sectionHeader['type']] = [
        'flags' => $sectionHeader['flags'],
        'length' => $sectionHeader['length'],
        'offset' => $sectionStart
      ];
      // Seek to the start of the next section
      $this->seek($this->offset + $sectionHeader['length']);
      $numSections += 1;
    }
  }

  public function close()
  {
    $this->offset = 0;
    $this->data = null;
    $this->size = 0;
    $this->sections = [];
    $this->meta = null;
    $this->frameMeta = null;
    $this->soundMeta = null;
    $this->numCameraFrames = 0;
    $this->frameFlagsMask = 0;
    $this->cameraFlagsMask = 0;
  }

  public function getSectionData(string $type)
  {
    $sectionStart = 0;
    $sectionSize = 0;
    if ($type === 'KMI') {
      $sectionStart = 8;
      $sectionSize = $this->sections[$type]['length'];
    } elseif ($type === 'KSN') {
      $sectionStart = 36;
      $sectionSize = $this->sections[$type]['length'] - 28;
    } else {
      $sectionStart = 12;
      $sectionSize = $this->sections[$type]['length'] - 4;
    }
    $this->seekToSection($type);
    $this->seek($sectionStart, 1);
    return $this->read($sectionSize);
  }

  public function getSectionHash(string $type)
  {
    return md5($this->getSectionData($type));
  }

  public function getMeta()
  {
    if (isset($this->meta)) return $this->meta;
    $this->seekToSection('KFH');
    // Skip past section header and checksum
    $this->seek(12, 1);
    $meta = $this->unpack([
      'creationTimestamp' => 'V',
      'modifiedTimestamp' => 'V',
      'appVersion' => 'V',
      'rootAuthorId' => 'H20',
      'parentAuthorId' => 'H20',
      'currentAuthorId' => 'H20',
      'rootAuthorName' => 'a22',
      'parentAuthorName' => 'a22',
      'currentAuthorName' => 'a22',
      'rootFilename' => 'a28',
      'parentFilename' => 'a28',
      'currentFilename' => 'a28',
      'frameCount' => 'v',
      'thumbIndex' => 'v',
      'flags' => 'v',
      'frameSpeed' => 'C',
      'layerFlags' => 'C',
    ], 204);
    // Get frame author IDs
    $frameAuthorIds = array_map(function ($frame) {
      return $frame['fsid'];
    }, $this->getFrameMeta());
    // Get sound meta
    $soundMeta = $this->getSoundMeta();
    // Format metadata
    $this->meta = [
      'lock' => ($meta['flags'] & 0x1) === 1,
      'loop' => (($meta['flags'] >> 1) & 0x01) === 1,
      'flags' => $meta['flags'],
      'layer_flags' => $meta['layerFlags'],
      'app_version' => $meta['appVersion'],
      'frame_count' =>  $meta['frameCount'],
      'frame_speed' => $meta['frameSpeed'],
      'thumb_index' => $meta['thumbIndex'],
	  'modified_timestamp' => $meta['modifiedTimestamp'] + 946684800,
	  'created_timestamp' => $meta['creationTimestamp'] + 946684800,
      //'frame_fsids' => array_unique($frameAuthorIds),
      'num_camera_frames' => $this->numCameraFrames,
      'camera_flags_mask' => $this->cameraFlagsMask,
      'frame_flags_mask' => $this->frameFlagsMask,
	  'root_username' => $this->formatUsername($meta['rootAuthorName']),
      'root_fsid' => $this->formatAuthorId($meta['rootAuthorId']),
      'root_filename' => $this->formatFilename($meta['rootFilename']),
	  'parent_username' => $this->formatUsername($meta['parentAuthorName']),
      'parent_fsid' => $this->formatAuthorId($meta['parentAuthorId']),
      'parent_filename' => $this->formatFilename($meta['parentFilename']),
	  'current_username' => $this->formatUsername($meta['currentAuthorName']),
      'current_fsid' => $this->formatAuthorId($meta['currentAuthorId']),
      'current_filename' => $this->formatFilename($meta['currentFilename']),
      'track_frame_speed' => $soundMeta['track_frame_speed'],
	  'bgm_used' => $soundMeta['bgm_size'] > 0,
      'se1_used' => $soundMeta['se1_size'] > 0,
      'se2_used' => $soundMeta['se2_size'] > 0,
      'se3_used' => $soundMeta['se3_size'] > 0,
      'se4_used' => $soundMeta['se4_size'] > 0,
	  'bgm_digest' => ($soundMeta['bgm_size'] > 0) ? $this->getSoundtrackDigest('bgm') : null,
      'se1_digest' => ($soundMeta['se1_size'] > 0) ? $this->getSoundtrackDigest('se1') : null,
      'se2_digest' => ($soundMeta['se2_size'] > 0) ? $this->getSoundtrackDigest('se2') : null,
      'se3_digest' => ($soundMeta['se3_size'] > 0) ? $this->getSoundtrackDigest('se3') : null,
      'se4_digest' => ($soundMeta['se4_size'] > 0) ? $this->getSoundtrackDigest('se4') : null,
    ];
    return $this->meta;
  }

  public function getFrameMeta()
  {
    if (isset($this->frameMeta))
      return $this->frameMeta;
    $this->seekToSection('KMI');
    // Skip past section header
    $this->seek(8, 1);
    $offset = 0;
    $size = $this->sections['KMI']['length'];
    $this->frameMeta = [];
    do {
      $frame = $this->unpack([
        'colors' => 'V',
        'layer_size' => 'v3',
        'fsid' => 'H20',
        'depth' => 'C3',
        'sound' => 'C',
        'flags' => 'v',
        'camera_flags' => 'v',
      ], 28);
      // formar frame fsid properly...
      $frame['fsid'] = $this->formatAuthorId($frame['fsid']);
      // camera flags being set means uses this frame uses a photo import
      if (($frame['camera_flags'] & 0x7) > 0)
        $this->numCameraFrames += 1;
      // this will tell us which bits are used in these frames
      $this->frameFlagsMask |= $frame['flags'];
      $this->cameraFlagsMask |= $frame['camera_flags'];
      array_push($this->frameMeta, $frame);
      $offset += 28;
    } while ($offset <= $size - 28);
    return $this->frameMeta;
  }

  public function getFrameData(int $frameIndex)
  {
    $frameMetaTable = $this->getFrameMeta();
    // Calculate frame offset
    $frameOffset = 0;
    for ($i = 0; $i < $frameIndex; $i++) {
      $frameMeta = $frameMetaTable[$i];
      $frameOffset += $frameMeta['layer_size1'] + $frameMeta['layer_size2'] + $frameMeta['layer_size3'];
    }
    $this->seekToSection('KMC');
    // Skip to the start of the frame data
    $this->seek(12 + $frameOffset, 1);
    // Get size of current frame
    $frameMeta = $frameMetaTable[$frameIndex];
    $frameSize = $frameMeta['layer_size1'] + $frameMeta['layer_size2'] + $frameMeta['layer_size3'];
    return $this->read($frameSize);
  }

  public function getFrameHash(int $frameIndex)
  {
    return md5($this->getFrameData($frameIndex));
  }

  public function getFrameHashes()
  {
    $meta = $this->getMeta();
    $hashes = [];
    for ($frameIndex = 0; $frameIndex < $meta['frame_count']; $frameIndex++) {
      array_push($hashes, $this->getFrameHash($frameIndex));
    }
    return $hashes;
  }

  public function getSoundMeta()
  {
    if (isset($this->soundMeta)) return $this->soundMeta;
    $this->seekToSection('KSN');
    // Skip past section header
    $this->seek(8, 1);
    $this->soundMeta = $this->unpack([
      'track_frame_speed' => 'V',
      'bgm_size' => 'V',
      'se1_size' => 'V',
      'se2_size' => 'V',
      'se3_size' => 'V',
      'se4_size' => 'V',
    ], 48);
    return $this->soundMeta;
  }

  public function getSoundtrackData(string $id)
  {
    $soundMeta = $this->getSoundMeta();
    $offset = 8;
    foreach (['bgm', 'se1', 'se2', 'se3', 'se4'] as $key) {
      if ($key === $id) break;
      $offset += $soundMeta[$key . '_size'];
    }
    $this->seekToSection('KSN');
    // Skip to start of sound data
    $this->seek($offset + 28, 1);
    return $this->read($soundMeta[$id . '_size']);
  }

  public function getSoundtrackDigest(string $id)
  {
    $track = $this->getSoundtrackData($id);
    if (strlen($track) == 0) {
      return null;
    } else {
      return md5($track);
    }
  }

  public function isSignatureValid()
  {
    $this->seek(0);
    $content = $this->read($this->size - 256);
    $signature = $this->read(256);
    return openssl_verify($content, $signature, $this->pubkey, 'sha256WithRSAEncryption') === 1;
  }

  public function areSectionsValid()
  {
    $areValid = [];
    foreach ($this->sections as $type => $section) {
      if (in_array($type, ['KFH', 'KTN', 'KMC'])) {
        $this->seekToSection($type);
        $this->seek(8, 1); // skip section header
        $sectionSize = $this->sections[$type]['length'];
        $checksum = unpack('V', $this->read(4))[1]; // read checksum
        $body = $this->getSectionData($type);
        $areValid[$type] = $checksum === crc32($body);
      }
    }
    // KMI section doesn't have a checksum
    // KSN checksum is in a different place, not rly sure why but ok nintendo
    if (array_key_exists('KSN', $this->sections)) {
      $this->seekToSection('KSN');
      $this->seek(8 + 24, 1); // skip section header + sound meta
      $sectionSize = $this->sections['KSN']['length'];
      $checksum = unpack('V', $this->read(4))[1];
      $body = $this->getSectionData($type);
      $areValid[$type] = $checksum === crc32($body);
    }
    return $areValid;
  }

  public function validate()
  {
    $meta = $this->getMeta();
    $frameMeta = $this->getFrameMeta();
    $soundMeta = $this->getSoundMeta();
    $err = [];
    // Check signature validity
    if (!$this->isSignatureValid()) {
      array_push($err, 'SIGNATURE_INVALID');
    }
    // Check that the sum of the section + checksum lengths match the data length
    $calcSize = 0;
    foreach ($this->sections as $type => $section) {
      $calcSize += $section['length'] + 8;
    }
    if ($calcSize + 256 !== $this->size) {
      array_push($err, 'FILE_SIZE_INVALID');
    }
    // Check sections are present and are the correct length
    foreach (['KFH', 'KTN', 'KMC', 'KMI', 'KSN'] as $type) {
      if (!array_key_exists($type, $this->sections)) {
        array_push($err, $type . '_SECTION_MISSING');
      }
      if (($type === 'KFH') && ($this->sections['KFH']['length'] !== 204)) {
        array_push($err, 'KFH_SIZE_INVALID');
      }
      if (($type === 'KMI') && ($meta['frame_count'] !== $this->sections['KMI']['length'] / 28)) {
        array_push($err, 'KMI_SIZE_INVALID');
      }
      if ($type === 'KMC') {
        $calcSize = 0;
        foreach ($frameMeta as &$frame) {
          $calcSize += $frame['layer_size1'] + $frame['layer_size2'] + $frame['layer_size3'];
        }
        if ($calcSize > $this->sections['KMC']['length']) array_push($err, 'KMC_SIZE_INVALID'); // (allowing for padding)
      }
      if ($type === 'KSN') {
        $calcSize = 0;
        foreach (['bgm', 'se1', 'se2', 'se3', 'se4'] as $key) {
          $calcSize += $soundMeta[$key . '_size'];
        }
        if ($calcSize + 28 > $this->sections['KSN']['length']) array_push($err, 'KSN_SIZE_INVALID'); // (allowing for padding)
      }
    }
    // Check section crc32 hashes
    foreach ($this->areSectionsValid() as $type => $isValid) {
      if (!$isValid) array_push($err, $type . '_CRC32_INVALID');
    }
    // Validate metadata
    // ====
    // Check frame count matches number of frames in
    if ($meta['frame_count'] !== $this->sections['KMI']['length'] / 28) {
      array_push($err, 'FRAME_COUNT_INVALID');
    }
    // Check frame speed is in valid range
    if ($meta['frame_speed'] > 10) {
      array_push($err, 'FRAME_SPEED_INVALID');
    }
    // Check recording frame speed is in valid range
    if ($meta['track_frame_speed'] > 10) {
      array_push($err, 'TRACK_FRAME_SPEED_INVALID');
    }
    // Check thumb index is in valid range
    if ($meta['thumb_index'] > $meta['frame_count'] - 1) {
      array_push($err, 'THUMB_INDEX_INVALID');
    }
    return $err;
  }

  private function formatUsername(string $username)
  {
    return trim(mb_convert_encoding($username, 'UTF-8', 'UTF-16LE'));
  }

  private function formatAuthorId(string $id)
  {
    // Could trim the trailing null byte here, I don't think it's used, but I'm gonna leave it and see if Nintendo surprises us
    return strtoupper($id);
  }

  private function formatFilename(string $filename)
  {
    // If filename matches Flipnote Studio's PPM format, unpack it
    if (preg_match('/^[\x{00}-\x{FF}]{3}[A-Fa-f0-9]{13}[\x{00}-\x{FF}]{3}/', $filename)) {
      $f = unpack('H6mac/a13random/vedits', $filename);
      return strtoupper(sprintf('%6s_%13s_%03d', $f['mac'], $f['random'], $f['edits']));
    }
    return $filename;
  }

  private function read(int $nbytes = 1)
  {
    $ret = substr($this->data, $this->offset, $nbytes);
    $this->offset += $nbytes;
    return $ret;
  }

  private function seek(int $offset, int $whence = 0)
  {
    switch ($whence) {
      case 2:
        $this->offset = $this->size + $offset;
        break;
      case 1:
        $this->offset += $offset;
        break;
      case 0:
      default:
        $this->offset = $offset;
        break;
    }
  }

  private function seekToSection(string $type)
  {
    $this->seek($this->sections[$type]['offset']);
  }

  private function unpack(array $struct, int $nbytes = 0)
  {
    $structArr = [];
    foreach ($struct as $name => $type) {
      array_push($structArr, $type . $name);
    }
    return unpack(join('/', $structArr), $this->read($nbytes));
  }
}
