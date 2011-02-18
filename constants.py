#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

__doc__ = """ Contains all constants used by qpid """

# ------------ #
# Error codes  #
# ------------ #

ERROR_CODE_NOT_DELIVERED = 310
ERROR_CODE_CONTENT_TOO_LARGE = 311
ERROR_CODE_NO_ROUTE = 312
ERROR_CODE_NO_CONSUMERS = 313
ERROR_CODE_CONNECTION_FORCED = 320
ERROR_CODE_INVALID_PATH = 402 
ERROR_CODE_ACCESS_REFUSED = 403
ERROR_CODE_NOT_FOUND = 404
ERROR_CODE_RESOURCE_LOCKED = 405
ERROR_CODE_PRECONDITION_FAILED = 406
ERROR_CODE_FRAME_ERROR = 501
ERROR_CODE_SYNTAX_ERROR = 502
ERROR_CODE_COMMAND_INVALID = 503
ERROR_CODE_CHANNEL_ERROR = 504
ERROR_CODE_RESOURCE_ERROR = 506
ERROR_CODE_NOT_ALLOWED = 530
ERROR_CODE_NOT_IMPLEMENTED = 540
ERROR_CODE_INTERNAL_ERROR = 541

# ------------------- #
# Error descriptions  #
# ------------------- #

ERROR_DESC_NOT_DELIVERED = 'The client asked for a specific message that is no longer available. The message was delivered to another client, or was purged from the queue for some other reason.'
ERROR_DESC_CONTENT_TOO_LARGE = 'The client attempted to transfer content larger than the server could accept at the present time. The client may retry at a later time.'
ERROR_DESC_NO_ROUTE = 'When the exchange cannot route the result of a .Publish, most likely due to an invalid routing key. Only when the mandatory flag is set.'
ERROR_DESC_NO_CONSUMERS = 'When the exchange cannot deliver to a consumer when the immediate flag is set. As a result of pending data on the queue or the absence of any consumers of the queue.'
ERROR_DESC_CONNECTION_FORCED = 'An operator intervened to close the connection for some reason. The client may retry at some later date.'
ERROR_DESC_INVALID_PATH = 'The client tried to work with an unknown virtual host.'
ERROR_DESC_ACCESS_REFUSED = 'The client attempted to work with a server entity to which it has no access due to security settings.'
ERROR_DESC_NOT_FOUND = 'The client attempted to work with a server entity that does not exist.'
ERROR_DESC_RESOURCE_LOCKED = 'The client attempted to work with a server entity to which it has no access because another client is working with it.'
ERROR_DESC_PRECONDITION_FAILED = 'The client requested a method that was not allowed because some precondition failed.'
ERROR_DESC_FRAME_ERROR = 'The client sent a malformed frame that the server could not decode. This strongly implies a programming error in the client.'
ERROR_DESC_SYNTAX_ERROR = 'The client sent a frame that contained illegal values for one or more fields. This strongly implies a programming error in the client.'
ERROR_DESC_COMMAND_INVALID = 'The client sent an invalid sequence of frames, attempting to perform an operation that was considered invalid by the server. This usually implies a programming error in the client.'
ERROR_DESC_CHANNEL_ERROR = 'The client attempted to work with a channel that had not been correctly opened. This most likely indicates a fault in the client layer.'
ERROR_DESC_RESOURCE_ERROR = 'The server could not complete the method because it lacked sufficient resources. This may be due to the client creating too many of some type of entity.'
ERROR_DESC_NOT_ALLOWED = 'The client tried to work with some entity in a manner that is prohibited by the server, due to security settings or by some other criteria.'
ERROR_DESC_NOT_IMPLEMENTED = 'The client tried to use functionality that is not implemented in the server.'
ERROR_DESC_INTERNAL_ERROR = 'The server could not complete the method because of an internal error. The server may require intervention by an operator in order to resume normal operations.'




