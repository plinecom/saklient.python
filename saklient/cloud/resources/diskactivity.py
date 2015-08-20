# -*- coding:utf-8 -*-

# This code is automatically transpiled by Saklient Translator

import six
from ..client import Client
from .activity import Activity
from .diskactivitysample import DiskActivitySample
from ...util import Util
import saklient

str = six.text_type
# module saklient.cloud.resources.diskactivity

class DiskActivity(Activity):
    
    # (instance field) _samples
    
    ## @return {saklient.cloud.resources.diskactivitysample.DiskActivitySample[]}
    def get_samples(self):
        return self._samples
    
    ## サンプル列
    samples = property(get_samples, None, None)
    
    ## @private
    # @return {str}
    def _api_path_prefix(self):
        return "/disk"
    
    ## @ignore
    # @param {saklient.cloud.client.Client} client
    def __init__(self, client):
        super(DiskActivity, self).__init__(client)
        Util.validate_type(client, "saklient.cloud.client.Client")
    
    ## @private
    # @param {str} atStr
    # @param {any} data
    # @return {void}
    def _add_sample(self, atStr, data):
        Util.validate_type(atStr, "str")
        self._samples.append(DiskActivitySample(atStr, data))
    
    ## 現在の最新のアクティビティ情報を取得し、samplesに格納します。
    #  
    #  	 * @return this
    # 
    # @param {NativeDate} startDate=None
    # @param {NativeDate} endDate=None
    # @return {saklient.cloud.resources.diskactivity.DiskActivity}
    def fetch(self, startDate=None, endDate=None):
        Util.validate_type(startDate, "NativeDate")
        Util.validate_type(endDate, "NativeDate")
        self._samples = []
        return self._fetch(startDate, endDate)
    
