# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException
import saklient

# module saklient.cloud.errors.stillcreatingexception

class StillCreatingException(HttpConflictException):
    ## 要求された操作を行えません。リソースの作成処理が進行中です。完了後に再度お試しください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(StillCreatingException, self).__init__(status, code, "要求された操作を行えません。リソースの作成処理が進行中です。完了後に再度お試しください。" if message is None or message == "" else message)
    
