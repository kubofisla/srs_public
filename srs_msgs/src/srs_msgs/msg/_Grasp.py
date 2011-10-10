"""autogenerated by genmsg_py from Grasp.msg. Do not edit."""
import roslib.message
import struct

import trajectory_msgs.msg
import roslib.rostime
import geometry_msgs.msg
import srs_msgs.msg
import std_msgs.msg

class Grasp(roslib.message.Message):
  _md5sum = "ebd0462690e2e7b4da2b335d97c908d9"
  _type = "srs_msgs/Grasp"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """srs_msgs/GraspConfiguration[] grasp_configuration

================================================================================
MSG: srs_msgs/GraspConfiguration
std_msgs/Float32 object_id
std_msgs/String hand_type
trajectory_msgs/JointTrajectory sconfiguration
geometry_msgs/PoseStamped palm_pose
std_msgs/String category
std_msgs/Float32 score

================================================================================
MSG: std_msgs/Float32
float32 data
================================================================================
MSG: std_msgs/String
string data

================================================================================
MSG: trajectory_msgs/JointTrajectory
Header header
string[] joint_names
JointTrajectoryPoint[] points
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.secs: seconds (stamp_secs) since epoch
# * stamp.nsecs: nanoseconds since stamp_secs
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: trajectory_msgs/JointTrajectoryPoint
float64[] positions
float64[] velocities
float64[] accelerations
duration time_from_start
================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of postion and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

"""
  __slots__ = ['grasp_configuration']
  _slot_types = ['srs_msgs/GraspConfiguration[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.
    
    The available fields are:
       grasp_configuration
    
    @param args: complete set of field values, in .msg order
    @param kwds: use keyword arguments corresponding to message field names
    to set specific fields. 
    """
    if args or kwds:
      super(Grasp, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.grasp_configuration is None:
        self.grasp_configuration = []
    else:
      self.grasp_configuration = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    @param buff: buffer
    @type  buff: StringIO
    """
    try:
      length = len(self.grasp_configuration)
      buff.write(_struct_I.pack(length))
      for val1 in self.grasp_configuration:
        _v1 = val1.object_id
        buff.write(_struct_f.pack(_v1.data))
        _v2 = val1.hand_type
        _x = _v2.data
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        _v3 = val1.sconfiguration
        _v4 = _v3.header
        buff.write(_struct_I.pack(_v4.seq))
        _v5 = _v4.stamp
        _x = _v5
        buff.write(_struct_2I.pack(_x.secs, _x.nsecs))
        _x = _v4.frame_id
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        length = len(_v3.joint_names)
        buff.write(_struct_I.pack(length))
        for val3 in _v3.joint_names:
          length = len(val3)
          buff.write(struct.pack('<I%ss'%length, length, val3.encode()))
        length = len(_v3.points)
        buff.write(_struct_I.pack(length))
        for val3 in _v3.points:
          length = len(val3.positions)
          buff.write(_struct_I.pack(length))
          pattern = '<%sd'%length
          buff.write(struct.pack(pattern, *val3.positions))
          length = len(val3.velocities)
          buff.write(_struct_I.pack(length))
          pattern = '<%sd'%length
          buff.write(struct.pack(pattern, *val3.velocities))
          length = len(val3.accelerations)
          buff.write(_struct_I.pack(length))
          pattern = '<%sd'%length
          buff.write(struct.pack(pattern, *val3.accelerations))
          _v6 = val3.time_from_start
          _x = _v6
          buff.write(_struct_2i.pack(_x.secs, _x.nsecs))
        _v7 = val1.palm_pose
        _v8 = _v7.header
        buff.write(_struct_I.pack(_v8.seq))
        _v9 = _v8.stamp
        _x = _v9
        buff.write(_struct_2I.pack(_x.secs, _x.nsecs))
        _x = _v8.frame_id
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        _v10 = _v7.pose
        _v11 = _v10.position
        _x = _v11
        buff.write(_struct_3d.pack(_x.x, _x.y, _x.z))
        _v12 = _v10.orientation
        _x = _v12
        buff.write(_struct_4d.pack(_x.x, _x.y, _x.z, _x.w))
        _v13 = val1.category
        _x = _v13.data
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        _v14 = val1.score
        buff.write(_struct_f.pack(_v14.data))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    @param str: byte array of serialized message
    @type  str: str
    """
    try:
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.grasp_configuration = []
      for i in range(0, length):
        val1 = srs_msgs.msg.GraspConfiguration()
        _v15 = val1.object_id
        start = end
        end += 4
        (_v15.data,) = _struct_f.unpack(str[start:end])
        _v16 = val1.hand_type
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v16.data = str[start:end]
        _v17 = val1.sconfiguration
        _v18 = _v17.header
        start = end
        end += 4
        (_v18.seq,) = _struct_I.unpack(str[start:end])
        _v19 = _v18.stamp
        _x = _v19
        start = end
        end += 8
        (_x.secs, _x.nsecs,) = _struct_2I.unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v18.frame_id = str[start:end]
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        _v17.joint_names = []
        for i in range(0, length):
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          start = end
          end += length
          val3 = str[start:end]
          _v17.joint_names.append(val3)
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        _v17.points = []
        for i in range(0, length):
          val3 = trajectory_msgs.msg.JointTrajectoryPoint()
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          pattern = '<%sd'%length
          start = end
          end += struct.calcsize(pattern)
          val3.positions = struct.unpack(pattern, str[start:end])
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          pattern = '<%sd'%length
          start = end
          end += struct.calcsize(pattern)
          val3.velocities = struct.unpack(pattern, str[start:end])
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          pattern = '<%sd'%length
          start = end
          end += struct.calcsize(pattern)
          val3.accelerations = struct.unpack(pattern, str[start:end])
          _v20 = val3.time_from_start
          _x = _v20
          start = end
          end += 8
          (_x.secs, _x.nsecs,) = _struct_2i.unpack(str[start:end])
          _v17.points.append(val3)
        _v21 = val1.palm_pose
        _v22 = _v21.header
        start = end
        end += 4
        (_v22.seq,) = _struct_I.unpack(str[start:end])
        _v23 = _v22.stamp
        _x = _v23
        start = end
        end += 8
        (_x.secs, _x.nsecs,) = _struct_2I.unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v22.frame_id = str[start:end]
        _v24 = _v21.pose
        _v25 = _v24.position
        _x = _v25
        start = end
        end += 24
        (_x.x, _x.y, _x.z,) = _struct_3d.unpack(str[start:end])
        _v26 = _v24.orientation
        _x = _v26
        start = end
        end += 32
        (_x.x, _x.y, _x.z, _x.w,) = _struct_4d.unpack(str[start:end])
        _v27 = val1.category
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v27.data = str[start:end]
        _v28 = val1.score
        start = end
        end += 4
        (_v28.data,) = _struct_f.unpack(str[start:end])
        self.grasp_configuration.append(val1)
      return self
    except struct.error as e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    @param buff: buffer
    @type  buff: StringIO
    @param numpy: numpy python module
    @type  numpy module
    """
    try:
      length = len(self.grasp_configuration)
      buff.write(_struct_I.pack(length))
      for val1 in self.grasp_configuration:
        _v29 = val1.object_id
        buff.write(_struct_f.pack(_v29.data))
        _v30 = val1.hand_type
        _x = _v30.data
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        _v31 = val1.sconfiguration
        _v32 = _v31.header
        buff.write(_struct_I.pack(_v32.seq))
        _v33 = _v32.stamp
        _x = _v33
        buff.write(_struct_2I.pack(_x.secs, _x.nsecs))
        _x = _v32.frame_id
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        length = len(_v31.joint_names)
        buff.write(_struct_I.pack(length))
        for val3 in _v31.joint_names:
          length = len(val3)
          buff.write(struct.pack('<I%ss'%length, length, val3.encode()))
        length = len(_v31.points)
        buff.write(_struct_I.pack(length))
        for val3 in _v31.points:
          length = len(val3.positions)
          buff.write(_struct_I.pack(length))
          pattern = '<%sd'%length
          buff.write(val3.positions.tostring())
          length = len(val3.velocities)
          buff.write(_struct_I.pack(length))
          pattern = '<%sd'%length
          buff.write(val3.velocities.tostring())
          length = len(val3.accelerations)
          buff.write(_struct_I.pack(length))
          pattern = '<%sd'%length
          buff.write(val3.accelerations.tostring())
          _v34 = val3.time_from_start
          _x = _v34
          buff.write(_struct_2i.pack(_x.secs, _x.nsecs))
        _v35 = val1.palm_pose
        _v36 = _v35.header
        buff.write(_struct_I.pack(_v36.seq))
        _v37 = _v36.stamp
        _x = _v37
        buff.write(_struct_2I.pack(_x.secs, _x.nsecs))
        _x = _v36.frame_id
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        _v38 = _v35.pose
        _v39 = _v38.position
        _x = _v39
        buff.write(_struct_3d.pack(_x.x, _x.y, _x.z))
        _v40 = _v38.orientation
        _x = _v40
        buff.write(_struct_4d.pack(_x.x, _x.y, _x.z, _x.w))
        _v41 = val1.category
        _x = _v41.data
        length = len(_x)
        buff.write(struct.pack('<I%ss'%length, length, _x.encode()))
        _v42 = val1.score
        buff.write(_struct_f.pack(_v42.data))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    @param str: byte array of serialized message
    @type  str: str
    @param numpy: numpy python module
    @type  numpy: module
    """
    try:
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.grasp_configuration = []
      for i in range(0, length):
        val1 = srs_msgs.msg.GraspConfiguration()
        _v43 = val1.object_id
        start = end
        end += 4
        (_v43.data,) = _struct_f.unpack(str[start:end])
        _v44 = val1.hand_type
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v44.data = str[start:end]
        _v45 = val1.sconfiguration
        _v46 = _v45.header
        start = end
        end += 4
        (_v46.seq,) = _struct_I.unpack(str[start:end])
        _v47 = _v46.stamp
        _x = _v47
        start = end
        end += 8
        (_x.secs, _x.nsecs,) = _struct_2I.unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v46.frame_id = str[start:end]
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        _v45.joint_names = []
        for i in range(0, length):
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          start = end
          end += length
          val3 = str[start:end]
          _v45.joint_names.append(val3)
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        _v45.points = []
        for i in range(0, length):
          val3 = trajectory_msgs.msg.JointTrajectoryPoint()
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          pattern = '<%sd'%length
          start = end
          end += struct.calcsize(pattern)
          val3.positions = numpy.frombuffer(str[start:end], dtype=numpy.float64, count=length)
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          pattern = '<%sd'%length
          start = end
          end += struct.calcsize(pattern)
          val3.velocities = numpy.frombuffer(str[start:end], dtype=numpy.float64, count=length)
          start = end
          end += 4
          (length,) = _struct_I.unpack(str[start:end])
          pattern = '<%sd'%length
          start = end
          end += struct.calcsize(pattern)
          val3.accelerations = numpy.frombuffer(str[start:end], dtype=numpy.float64, count=length)
          _v48 = val3.time_from_start
          _x = _v48
          start = end
          end += 8
          (_x.secs, _x.nsecs,) = _struct_2i.unpack(str[start:end])
          _v45.points.append(val3)
        _v49 = val1.palm_pose
        _v50 = _v49.header
        start = end
        end += 4
        (_v50.seq,) = _struct_I.unpack(str[start:end])
        _v51 = _v50.stamp
        _x = _v51
        start = end
        end += 8
        (_x.secs, _x.nsecs,) = _struct_2I.unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v50.frame_id = str[start:end]
        _v52 = _v49.pose
        _v53 = _v52.position
        _x = _v53
        start = end
        end += 24
        (_x.x, _x.y, _x.z,) = _struct_3d.unpack(str[start:end])
        _v54 = _v52.orientation
        _x = _v54
        start = end
        end += 32
        (_x.x, _x.y, _x.z, _x.w,) = _struct_4d.unpack(str[start:end])
        _v55 = val1.category
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        start = end
        end += length
        _v55.data = str[start:end]
        _v56 = val1.score
        start = end
        end += 4
        (_v56.data,) = _struct_f.unpack(str[start:end])
        self.grasp_configuration.append(val1)
      return self
    except struct.error as e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill

_struct_I = roslib.message.struct_I
_struct_f = struct.Struct("<f")
_struct_2I = struct.Struct("<2I")
_struct_4d = struct.Struct("<4d")
_struct_2i = struct.Struct("<2i")
_struct_3d = struct.Struct("<3d")
