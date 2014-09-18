# -*- coding:utf-8 -*-

from .httpexception import HttpException

# module saklient.errors.httprequesttimeoutexception

class HttpRequestTimeoutException(HttpException):
    ## HTTPエラー。Request Timeout.
    
    # (class field) default_message = "HTTPエラー。Request Timeout."
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(HttpRequestTimeoutException, self).__init__(status, code, message)
    
