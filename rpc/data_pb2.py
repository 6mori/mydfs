# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data.proto',
  package='rpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\ndata.proto\x12\x03rpc\"\x07\n\x05\x45mpty\"\x17\n\x05\x43hunk\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\"C\n\rUploadRequest\x12\x12\n\x08\x66ilename\x18\x01 \x01(\tH\x00\x12\x10\n\x06\x62uffer\x18\x02 \x01(\x0cH\x00\x42\x0c\n\ntest_oneof\":\n\x08Response\x12\x1d\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x0f.rpc.StatusCode\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1c\n\x08\x46ilename\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"U\n\x08\x46ileList\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x02\x12\x13\n\x0b\x63reatedtime\x18\x03 \x01(\x02\x12\x14\n\x0cmodifiedtime\x18\x04 \x01(\x02* \n\nStatusCode\x12\x06\n\x02OK\x10\x00\x12\n\n\x06\x46\x61iled\x10\x01\x32\xc2\x02\n\nFileSystem\x12,\n\nCreateFile\x12\r.rpc.Filename\x1a\r.rpc.Response\"\x00\x12,\n\nDeleteFile\x12\r.rpc.Filename\x1a\r.rpc.Response\"\x00\x12*\n\tListFiles\x12\n.rpc.Empty\x1a\r.rpc.FileList\"\x00\x30\x01\x12/\n\x06Upload\x12\x12.rpc.UploadRequest\x1a\r.rpc.Response\"\x00(\x01\x12)\n\x08\x44ownload\x12\r.rpc.Filename\x1a\n.rpc.Chunk\"\x00\x30\x01\x12&\n\x04Lock\x12\r.rpc.Filename\x1a\r.rpc.Response\"\x00\x12(\n\x06Unlock\x12\r.rpc.Filename\x1a\r.rpc.Response\"\x00\x62\x06proto3')
)

_STATUSCODE = _descriptor.EnumDescriptor(
  name='StatusCode',
  full_name='rpc.StatusCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Failed', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=299,
  serialized_end=331,
)
_sym_db.RegisterEnumDescriptor(_STATUSCODE)

StatusCode = enum_type_wrapper.EnumTypeWrapper(_STATUSCODE)
OK = 0
Failed = 1



_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='rpc.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=26,
)


_CHUNK = _descriptor.Descriptor(
  name='Chunk',
  full_name='rpc.Chunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buffer', full_name='rpc.Chunk.buffer', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=51,
)


_UPLOADREQUEST = _descriptor.Descriptor(
  name='UploadRequest',
  full_name='rpc.UploadRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='rpc.UploadRequest.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='buffer', full_name='rpc.UploadRequest.buffer', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='test_oneof', full_name='rpc.UploadRequest.test_oneof',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=53,
  serialized_end=120,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='rpc.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='rpc.Response.code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='rpc.Response.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=180,
)


_FILENAME = _descriptor.Descriptor(
  name='Filename',
  full_name='rpc.Filename',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='rpc.Filename.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=182,
  serialized_end=210,
)


_FILELIST = _descriptor.Descriptor(
  name='FileList',
  full_name='rpc.FileList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='rpc.FileList.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size', full_name='rpc.FileList.size', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='createdtime', full_name='rpc.FileList.createdtime', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='modifiedtime', full_name='rpc.FileList.modifiedtime', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=212,
  serialized_end=297,
)

_UPLOADREQUEST.oneofs_by_name['test_oneof'].fields.append(
  _UPLOADREQUEST.fields_by_name['filename'])
_UPLOADREQUEST.fields_by_name['filename'].containing_oneof = _UPLOADREQUEST.oneofs_by_name['test_oneof']
_UPLOADREQUEST.oneofs_by_name['test_oneof'].fields.append(
  _UPLOADREQUEST.fields_by_name['buffer'])
_UPLOADREQUEST.fields_by_name['buffer'].containing_oneof = _UPLOADREQUEST.oneofs_by_name['test_oneof']
_RESPONSE.fields_by_name['code'].enum_type = _STATUSCODE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['Chunk'] = _CHUNK
DESCRIPTOR.message_types_by_name['UploadRequest'] = _UPLOADREQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['Filename'] = _FILENAME
DESCRIPTOR.message_types_by_name['FileList'] = _FILELIST
DESCRIPTOR.enum_types_by_name['StatusCode'] = _STATUSCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:rpc.Empty)
  ))
_sym_db.RegisterMessage(Empty)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), dict(
  DESCRIPTOR = _CHUNK,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:rpc.Chunk)
  ))
_sym_db.RegisterMessage(Chunk)

UploadRequest = _reflection.GeneratedProtocolMessageType('UploadRequest', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADREQUEST,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:rpc.UploadRequest)
  ))
_sym_db.RegisterMessage(UploadRequest)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:rpc.Response)
  ))
_sym_db.RegisterMessage(Response)

Filename = _reflection.GeneratedProtocolMessageType('Filename', (_message.Message,), dict(
  DESCRIPTOR = _FILENAME,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:rpc.Filename)
  ))
_sym_db.RegisterMessage(Filename)

FileList = _reflection.GeneratedProtocolMessageType('FileList', (_message.Message,), dict(
  DESCRIPTOR = _FILELIST,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:rpc.FileList)
  ))
_sym_db.RegisterMessage(FileList)



_FILESYSTEM = _descriptor.ServiceDescriptor(
  name='FileSystem',
  full_name='rpc.FileSystem',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=334,
  serialized_end=656,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateFile',
    full_name='rpc.FileSystem.CreateFile',
    index=0,
    containing_service=None,
    input_type=_FILENAME,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteFile',
    full_name='rpc.FileSystem.DeleteFile',
    index=1,
    containing_service=None,
    input_type=_FILENAME,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ListFiles',
    full_name='rpc.FileSystem.ListFiles',
    index=2,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_FILELIST,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Upload',
    full_name='rpc.FileSystem.Upload',
    index=3,
    containing_service=None,
    input_type=_UPLOADREQUEST,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Download',
    full_name='rpc.FileSystem.Download',
    index=4,
    containing_service=None,
    input_type=_FILENAME,
    output_type=_CHUNK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Lock',
    full_name='rpc.FileSystem.Lock',
    index=5,
    containing_service=None,
    input_type=_FILENAME,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Unlock',
    full_name='rpc.FileSystem.Unlock',
    index=6,
    containing_service=None,
    input_type=_FILENAME,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_FILESYSTEM)

DESCRIPTOR.services_by_name['FileSystem'] = _FILESYSTEM

# @@protoc_insertion_point(module_scope)
