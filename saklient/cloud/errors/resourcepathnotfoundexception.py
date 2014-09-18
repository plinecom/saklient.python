# -*- coding:utf-8 -*-

from ...errors.httpnotfoundexception import HttpNotFoundException

# module saklient.cloud.errors.resourcepathnotfoundexception

class ResourcePathNotFoundException(HttpNotFoundException):
    ## 対象が見つかりません。パスに誤りがあります。
    
    # (class field) default_message = "対象が見つかりません。パスに誤りがあります。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(ResourcePathNotFoundException, self).__init__(status, code, message)
    
