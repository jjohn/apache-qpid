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

__doc__ = """Describes the exceptions that are raised by qpid

          Exceptions fall into two categories: 
          
            ChannelExceptions : These are all associated with failures that affect the current channel but not
                                other channels in the same connection
            ConnectionExceptions : These are all associated with failures that preclude any further activity
                                   on the connection and require its closing.

          """

from constants import *

# ------------------------------
# ------------------------------
class QpidException(Exception):

    """
    base class of all qpid exceptions
    """
    
    # --------------------------------------------------------------------------
    def __init__(self, error_code = '', error_desc = '', additional_detail=''):
        """
        initialises the object and sets the error code
        """
        Exception.__init__(self)
        
        self._name = str(self.__class__).split('.')[1]
        self._error_code = str(error_code)
        self._error_desc = str(error_desc)
        if additional_detail:
            self._error_desc += '\nDETAILS:' + str(additional_detail)

    # ------------------
    def __str__(self):
        """
        returns a textual representation of the error object
        """
        return 'error name: %s  \nerror code: %s \nerror description: %s' % (self._name, self._error_code, self._error_desc)

        
    # ------------------
    def __repr__(self):
        """
        returns a textual representation of the error object
        """
        return 'error name: %s  \nerror code: %s \nerror description: %s' % (self._name, self._error_code, self._error_desc)
    
    # ----------------------
    def getObjName(self):
        """
        returns the error object class name
        """
        return self._name
    
    
    # ----------------------
    def getErrorCode(self):
        """
        returns the error code
        """
        return self._error_code
    
    # ----------------------
    def getErrorDesc(self):
        """
        returns the error description
        """
        return self._error_desc
        
    
# -------------------------------------
# -------------------------------------
class ChannelException(QpidException):

    """
    Channel Exception class
    """

    # ----------------------------------------------------------------
    def __init__(self, error_code, error_desc, additional_detail=''):
        """
        initialise the ChannelException object
        """
        QpidException.__init__(self, error_code, error_desc, additional_detail)

# ----------------------------------------
# ----------------------------------------
class ConnectionException(QpidException):

    """
    Connection Exception class
    """

    # ----------------------------------------------------------------
    def __init__(self, error_code, error_desc, additional_detail=''):
        """
        initialise the ConnectionException object
        """
        QpidException.__init__(self, error_code, error_desc, additional_detail)


# ---------------------------- #
# ChannelException subclasses  #
# ---------------------------- #

# ---------------------------------------------
# ---------------------------------------------
class NotDeliveredException(ChannelException):

    """
    The client asked for a specific message that is no longer available. The
    message was delivered to another client, or was purged from the queue for
    some other reason  
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the NotDeliveredException object
        """
        ChannelException.__init__(self, ERROR_CODE_NOT_DELIVERED, ERROR_DESC_NOT_DELIVERED, additional_detail)
        

# -----------------------------------------------
# -----------------------------------------------
class ContentTooLargeException(ChannelException):

    """
    The client attempted to transfer content larger than the server could accept
    at the present time. The client may retry at a later time.    
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the ContentTooLargeException object
        """
        ChannelException.__init__(self, ERROR_CODE_CONTENT_TOO_LARGE, ERROR_DESC_CONTENT_TOO_LARGE, additional_detail)
        
# -----------------------------------------
# -----------------------------------------
class NoRouteException(ChannelException):

    """
    When the exchange cannot route the result of a .Publish, most likely due to
    an invalid routing key. Only when the mandatory flag is set.
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the NoRouteException object
        """
        ChannelException.__init__(self, ERROR_CODE_NO_ROUTE, ERROR_DESC_NO_ROUTE, additional_detail)
        

# --------------------------------------------
# --------------------------------------------
class NoConsumersException(ChannelException):

    """
    When the exchange cannot deliver to a consumer when the immediate flag
    is set. As a result of pending data on the queue or the absence of any
    consumers of the queue.
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the NoConsumersException object
        """
        ChannelException.__init__(self, ERROR_CODE_NO_CONSUMERS, ERROR_DESC_NO_CONSUMERS, additional_detail)


# ----------------------------------------------
# ----------------------------------------------
class AccessRefusedException(ChannelException):

    """
    The client attempted to work with a server entity to which it has no access
    due to security settings.
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the AccessRefusedException object
        """
        ChannelException.__init__(self, ERROR_CODE_ACCESS_REFUSED, ERROR_DESC_ACCESS_REFUSED, additional_detail)


# -----------------------------------------
# -----------------------------------------
class NotFoundException(ChannelException):

    """
    The client attempted to work with a server entity that does not exist.
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the NotFoundException object
        """
        ChannelException.__init__(self, ERROR_CODE_NOT_FOUND, ERROR_DESC_NOT_FOUND, additional_detail)


# -----------------------------------------------
# -----------------------------------------------
class ResourceLockedException(ChannelException):

    """
    The client attempted to work with a server entity to which it has no access
    because another client is working with it.
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the ResourceLockedException object
        """
        ChannelException.__init__(self, ERROR_CODE_RESOURCE_LOCKED, ERROR_DESC_RESOURCE_LOCKED, additional_detail)


# ---------------------------------------------------
# ---------------------------------------------------
class PreconditionFailedException(ChannelException):

    """
    The client requested a method that was not allowed because some
    precondition failed.
    """

    # -----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the PreconditionFailedException object
        """
        ChannelException.__init__(self, ERROR_CODE_PRECONDITION_FAILED, ERROR_DESC_PRECONDITION_FAILED, additional_detail)


# ------------------------------- #
# ConnectionException subclasses  #
# ------------------------------- #

# ----------------------------------------------------
# ----------------------------------------------------
class ConnectionForcedException(ConnectionException):

    """
    An operator intervened to close the connection for some reason. The client
    may retry at some later date.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the ConnectionForcedException object
        """
        ConnectionException.__init__(self, ERROR_CODE_CONNECTION_FORCED, ERROR_DESC_CONNECTION_FORCED, additional_detail)
 
# -----------------------------------------------
# -----------------------------------------------
class InvalidPathException(ConnectionException):

    """
    The client tried to work with an unknown virtual host.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the InvalidPathException object
        """
        ConnectionException.__init__(self, ERROR_CODE_INVALID_PATH, ERROR_DESC_INVALID_PATH, additional_detail)

# -----------------------------------------------
# -----------------------------------------------
class FrameErrorException(ConnectionException):

    """
    The client sent a malformed frame that the server could not decode. This
    strongly implies a programming error in the client.    
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the FrameErrorException object
        """
        ConnectionException.__init__(self, ERROR_CODE_FRAME_ERROR, ERROR_DESC_FRAME_ERROR, additional_detail)

# -----------------------------------------------
# -----------------------------------------------
class SyntaxErrorException(ConnectionException):

    """
    The client sent a frame that contained illegal values for one or more fields. 
    This strongly implies a programming error in the client.    
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the SyntaxErrorException object
        """
        ConnectionException.__init__(self, ERROR_CODE_SYNTAX_ERROR, ERROR_DESC_SYNTAX_ERROR, additional_detail)
    
# --------------------------------------------------
# --------------------------------------------------
class CommandInvalidException(ConnectionException):

    """
    The client sent an invalid sequence of frames, attempting to perform an
    operation that was considered invalid by the server. This usually implies a
    programming error in the client.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the CommandInvalidException object
        """
        ConnectionException.__init__(self, ERROR_CODE_COMMAND_INVALID, ERROR_DESC_COMMAND_INVALID, additional_detail)
    

# --------------------------------------------------
# --------------------------------------------------
class ChannelErrorException(ConnectionException):

    """
    The client attempted to work with a channel that had not been correctly
    opened. This most likely indicates a fault in the client layer.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the ChannelErrorException object
        """
        ConnectionException.__init__(self, ERROR_CODE_CHANNEL_ERROR, ERROR_DESC_CHANNEL_ERROR, additional_detail)
    

# --------------------------------------------------
# --------------------------------------------------
class ResourceErrorException(ConnectionException):

    """
    The server could not complete the method because it lacked sufficient
    resources. This may be due to the client creating too many of some type of
    entity.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the ResourceErrorException object
        """
        ConnectionException.__init__(self, ERROR_CODE_RESOURCE_ERROR, ERROR_DESC_RESOURCE_ERROR, additional_detail)
    

# --------------------------------------------------
# --------------------------------------------------
class NotAllowedException(ConnectionException):

    """
    The client tried to work with some entity in a manner that is prohibited by
    the server, due to security settings or by some other criteria.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the NotAllowedException object
        """
        ConnectionException.__init__(self, ERROR_CODE_NOT_ALLOWED, ERROR_DESC_NOT_ALLOWED, additional_detail)

# --------------------------------------------------
# --------------------------------------------------
class NotImplementedException(ConnectionException):

    """
    The client tried to use functionality that is not implemented in the server.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the NotImplementedException object
        """
        ConnectionException.__init__(self, ERROR_CODE_NOT_IMPLEMENTED, ERROR_DESC_NOT_IMPLEMENTED, additional_detail)

# --------------------------------------------------
# --------------------------------------------------
class InternalErrorException(ConnectionException):

    """
    The server could not complete the method because of an internal error. The
    server may require intervention by an operator in order to resume normal
    operations.
    """
    
    # ----------------------------------------
    def __init__(self, additional_detail=''):
        """
        initialise the InternalErrorException object
        """
        ConnectionException.__init__(self, ERROR_CODE_INTERNAL_ERROR, ERROR_DESC_INTERNAL_ERROR, additional_detail)


# --------------------------
# Testing...
# --------------------------
if __name__ == '__main__':

    
    obj1 = NotDeliveredException(' NotDeliveredException details...')
    obj2 = ContentTooLargeException(' ContentTooLargeException details...')
    obj3 = NoRouteException(' NoRouteException details...')
    obj4 = NoConsumersException(' NoConsumersException details...')
    obj5 = AccessRefusedException(' AccessRefusedException details...')
    obj6 = NotFoundException(' NotFoundException details...')
    obj7 = ResourceLockedException(' ResourceLockedException details...')
    obj8 = PreconditionFailedException(' PreconditionFailedException details...')
    obj9 = ConnectionForcedException(' ConnectionForcedException details...')
    obj10 = InvalidPathException(' InvalidPathException details...')
    obj11 = FrameErrorException(' FrameErrorException details...')
    obj12 = SyntaxErrorException(' SyntaxErrorException details...')
    obj13 = CommandInvalidException(' CommandInvalidException details...')
    obj14 = ChannelErrorException(' ChannelErrorException details...')
    obj15 = ResourceErrorException(' ResourceErrorException details...')
    obj16 = NotAllowedException(' NotAllowedException details...')
    obj17 = NotImplementedException(' NotImplementedException details...')
    obj18 = InternalErrorException(' InternalErrorException details...')

    
    print '# ---------------------------------------------------'
    print repr(obj1)
    print '# ---------------------------------------------------\n'
    print '# ---------------------------------------------------'
    print repr(obj2)
    print '# ---------------------------------------------------\n'
    print '# ---------------------------------------------------'
    print repr(obj3)
    print '# ---------------------------------------------------\n'
    print '# ---------------------------------------------------'
    print repr(obj4)
    print '# ---------------------------------------------------\n'
    print '# ---------------------------------------------------'
    print repr(obj5)
    print '# ---------------------------------------------------\n'
    print '# ---------------------------------------------------'
    print repr(obj6)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj7)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj8)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj9)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj10)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj11)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj12)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj13)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj14)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj15)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj16)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj17)
    print '# ---------------------------------------------------\n'    
    print '# ---------------------------------------------------'
    print repr(obj18)
    print '# ---------------------------------------------------\n'    
    

