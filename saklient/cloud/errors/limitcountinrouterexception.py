# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.limitcountinrouterexception

class LimitCountInRouterException(HttpConflictException):
    ## 要求を受け付けできません。ルータあたりのリソース数上限により、リソースの割り当てに失敗しました。
    
    # (class field) default_message = "要求を受け付けできません。ルータあたりのリソース数上限により、リソースの割り当てに失敗しました。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(LimitCountInRouterException, self).__init__(status, code, message)
    