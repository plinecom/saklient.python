# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.ftpisalreadyopenexception

class FtpIsAlreadyOpenException(HttpConflictException):
    ## 要求された操作を行えません。FTP共有は既に開始されています。
    
    # (class field) default_message = "要求された操作を行えません。FTP共有は既に開始されています。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(FtpIsAlreadyOpenException, self).__init__(status, code, message)
    
