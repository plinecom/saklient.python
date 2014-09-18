# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.notforrouterexception

class NotForRouterException(HttpConflictException):
    ## 要求された操作を行えません。ルータには適用できません。
    
    # (class field) default_message = "要求された操作を行えません。ルータには適用できません。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(NotForRouterException, self).__init__(status, code, message)
    
