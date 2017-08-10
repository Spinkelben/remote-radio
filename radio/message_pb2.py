# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\rmessage.proto\"}\n\x07\x43ommand\x12\"\n\x04type\x18\x01 \x01(\x0e\x32\x14.Command.CommandType\x12\x0f\n\x07\x63hannel\x18\x02 \x01(\t\"=\n\x0b\x43ommandType\x12\x08\n\x04PLAY\x10\x00\x12\t\n\x05PAUSE\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\x0f\n\x0bSET_CHANNEL\x10\x03\"8\n\x08MetaInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x62itrate\x18\x02 \x01(\x05\x12\r\n\x05\x63odec\x18\x03 \x01(\tb\x06proto3')
)



_COMMAND_COMMANDTYPE = _descriptor.EnumDescriptor(
  name='CommandType',
  full_name='Command.CommandType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PLAY', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAUSE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOP', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SET_CHANNEL', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=81,
  serialized_end=142,
)
_sym_db.RegisterEnumDescriptor(_COMMAND_COMMANDTYPE)


_COMMAND = _descriptor.Descriptor(
  name='Command',
  full_name='Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Command.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channel', full_name='Command.channel', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMMAND_COMMANDTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=142,
)


_METAINFO = _descriptor.Descriptor(
  name='MetaInfo',
  full_name='MetaInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='MetaInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bitrate', full_name='MetaInfo.bitrate', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='codec', full_name='MetaInfo.codec', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=200,
)

_COMMAND.fields_by_name['type'].enum_type = _COMMAND_COMMANDTYPE
_COMMAND_COMMANDTYPE.containing_type = _COMMAND
DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
DESCRIPTOR.message_types_by_name['MetaInfo'] = _METAINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), dict(
  DESCRIPTOR = _COMMAND,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:Command)
  ))
_sym_db.RegisterMessage(Command)

MetaInfo = _reflection.GeneratedProtocolMessageType('MetaInfo', (_message.Message,), dict(
  DESCRIPTOR = _METAINFO,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:MetaInfo)
  ))
_sym_db.RegisterMessage(MetaInfo)


# @@protoc_insertion_point(module_scope)