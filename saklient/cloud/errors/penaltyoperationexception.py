# -*- coding:utf-8 -*-

from ...errors.httppaymentrequiredexception import HttpPaymentRequiredException

# module saklient.cloud.errors.penaltyoperationexception

class PenaltyOperationException(HttpPaymentRequiredException):
    ## お客様のご都合により操作を受け付けることができません。
    
    # (class field) default_message = "お客様のご都合により操作を受け付けることができません。"
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(PenaltyOperationException, self).__init__(status, code, message)
    