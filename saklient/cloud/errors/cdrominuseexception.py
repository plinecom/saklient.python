# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.cdrominuseexception

class CdromInUseException(HttpConflictException):
    ## 要求された操作を行えません。ISOイメージをサーバから排出後に実行してください。
    
    # (class field) default_message = "要求された操作を行えません。ISOイメージをサーバから排出後に実行してください。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(CdromInUseException, self).__init__(status, code, message)
    
