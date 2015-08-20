# -*- coding:utf-8 -*-

# This code is automatically transpiled by Saklient Translator

import six
from ...errors.httpbadrequestexception import HttpBadRequestException
import saklient

str = six.text_type
# module saklient.cloud.errors.missingparamexception

class MissingParamException(HttpBadRequestException):
    ## 不適切な要求です。必要なパラメータが指定されていません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(MissingParamException, self).__init__(status, code, "不適切な要求です。必要なパラメータが指定されていません。" if message is None or message == "" else message)
    
