# -*- coding:utf-8 -*-

# This code is automatically transpiled by Saklient Translator

import six
from ...errors.httpconflictexception import HttpConflictException
import saklient

str = six.text_type
# module saklient.cloud.errors.cdromdisabledexception

class CdromDisabledException(HttpConflictException):
    ## 要求された操作を行えません。ISOイメージが無効化されています。排出後に再度お試しください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(CdromDisabledException, self).__init__(status, code, "要求された操作を行えません。ISOイメージが無効化されています。排出後に再度お試しください。" if message is None or message == "" else message)
    
