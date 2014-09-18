# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.cdromisincompleteexception

class CdromIsIncompleteException(HttpConflictException):
    ## 要求された操作を行えません。このISOイメージは不完全です。複製処理等の完了後に再度お試しください。
    
    # (class field) default_message = "要求された操作を行えません。このISOイメージは不完全です。複製処理等の完了後に再度お試しください。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(CdromIsIncompleteException, self).__init__(status, code, message)
    