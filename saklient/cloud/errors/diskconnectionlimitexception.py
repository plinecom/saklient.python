# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.diskconnectionlimitexception

class DiskConnectionLimitException(HttpConflictException):
    ## 要求された操作を行えません。この接続インタフェースにこれ以上のディスクを接続することができません。
    
    # (class field) default_message = "要求された操作を行えません。この接続インタフェースにこれ以上のディスクを接続することができません。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(DiskConnectionLimitException, self).__init__(status, code, message)
    