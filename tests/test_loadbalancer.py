# -*- coding:utf-8 -*-

import unittest, sys, os, re, random, string, time, subprocess
sys.path[:0] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import socket, struct
from datetime import datetime
from saklient.util import Util
from saklient.cloud.api import API
from saklient.cloud.resources.swytch import Swytch
from saklient.cloud.resources.ipv4net import Ipv4Net
from saklient.cloud.resources.loadbalancer import LoadBalancer
from saklient.cloud.enums.eserverinstancestatus import EServerInstanceStatus
from saklient.errors.saklientexception import SaklientException
from saklient.errors.httpconflictexception import HttpConflictException


def ip2long(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]

def long2ip(num):
    return socket.inet_ntoa(struct.pack('!L', num))

class TestLoadbalancer(unittest.TestCase):
    
    
    
    TESTS_CONFIG_READYMADE_LB_ID = None
    
    def test_should_be_cruded(self):
        
        # load config file
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_ok_file = root + '/testok'
        if not os.path.exists(test_ok_file):
            print("詳細テストを行うには " + test_ok_file + " をtouchしてください。")
            sys.exit(0)
        
        config_file = root + '/config.sh'
        self.assertTrue(os.path.exists(config_file)) # config_file を作成してください。
        
        config = {}
        fh = open(config_file, "r")
        for line in fh:
            m = re.search("^\\s*export\\s+(\\w+)\\s*=\\s*(.+?)\\s*$", line)
            if m is None: continue
            key = m.group(1)
            value = m.group(2)
            value = re.sub("'([^']*)'|\"([^\"]*)\"|\\\\(.)|(.)", lambda m: m.group(1) or m.group(2) or m.group(3) or m.group(4), value)
            config[key] = value
        fh.close()
        
        self.assertIn('SACLOUD_TOKEN', config)
        self.assertIn('SACLOUD_SECRET', config)
        self.assertIn('SACLOUD_ZONE', config)
        
        # authorize
        api = API.authorize(config['SACLOUD_TOKEN'], config['SACLOUD_SECRET'], config['SACLOUD_ZONE'])
        self.assertIsInstance(api, API)
        
        
        
        # should be CRUDed
        name = '!python_test-' + datetime.now().strftime('%Y%m%d_%H%M%S') + '-' + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
        description = 'This instance was created by saklient.python test'
        tag = 'saklient-test'
        
        
        
        # create a LB
        if self.TESTS_CONFIG_READYMADE_LB_ID is None:
            
            # search a switch
            print('作成済みのルータ＋スイッチを検索しています...')
            swytches = api.swytch.with_name_like('saklient-lb-attached').limit(1).find()
            if 0 < len(swytches):
                swytch = swytches[0]
            else:
                print('ルータ＋スイッチを作成しています...')
                router = api.router.create()
                router.name = 'saklient-lb-attached'
                router.band_width_mbps = 100
                router.network_mask_len = 28
                router.save()
                
                print('ルータ＋スイッチの作成完了を待機しています...')
                if not router.sleep_while_creating(): fail('ルータが正常に作成されません')
                swytch = router.get_swytch()
            
            self.assertIsInstance(swytch, Swytch)
            self.assertTrue(len(swytch.ipv4_nets) > 0)
            net = swytch.ipv4_nets[0]
            print('%s/%d -> %s' % (net.address, net.mask_len, net.default_route))
            
            # create a loadbalancer
            print('ロードバランサを作成しています...')
            vrid = 123
            real_ip1 = Util.long2ip(Util.ip2long(net.default_route) + 3)
            real_ip2 = Util.long2ip(Util.ip2long(net.default_route) + 4)
            lb = api.appliance.create_load_balancer(swytch, vrid, [real_ip1, real_ip2], True)
            
            def test_required():
                lb.save()
            self.assertRaises(SaklientException, test_required)
            # Requiredフィールドが未set時は SaklientException がスローされなければなりません
            lb.name = name
            lb.description = ''
            lb.tags = [tag]
            lb.save()
            
            lb.reload()
            self.assertEqual(lb.default_route, net.default_route)
            self.assertEqual(lb.mask_len, net.mask_len)
            self.assertEqual(lb.vrid, vrid)
            self.assertEqual(lb.swytch_id, swytch.id)
            
            # wait the LB becomes up
            print('ロードバランサの起動を待機しています...')
            if not lb.sleep_until_up(): fail('ロードバランサが正常に起動しません')
        
        else:
            
            lb = api.appliance.get_by_id(self.TESTS_CONFIG_READYMADE_LB_ID)
            self.assertIsInstance(lb, LoadBalancer)
            swytch = lb.get_swytch()
            self.assertIsInstance(swytch, Swytch)
            net = swytch.ipv4_nets[0]
            self.assertIsInstance(net, Ipv4Net)
            print('%s/%d -> %s' % (net.address, net.mask_len, net.default_route))
        
        
        
        # clear virtual ips
        
        lb.clear_virtual_ips()
        lb.save()
        lb.reload()
        self.assertEqual(len(lb.virtual_ips), 0)
        
        
        
        # setting virtual ips test 1
        
        vip1Ip     = long2ip(ip2long(net.default_route) + 5)
        vip1SrvIp1 = long2ip(ip2long(net.default_route) + 6)
        vip1SrvIp2 = long2ip(ip2long(net.default_route) + 7)
        vip1SrvIp3 = long2ip(ip2long(net.default_route) + 8)
        vip1SrvIp4 = long2ip(ip2long(net.default_route) + 9)
        
        lb.add_virtual_ip({
            'vip': vip1Ip,
            'port': 80,
            'delay': 15,
            'servers': [
                { 'ip':vip1SrvIp1, 'port':80, 'protocol':'http', 'path_to_check':'/index.html', 'response_expected':200 },
                { 'ip':vip1SrvIp2, 'port':80, 'protocol':'https', 'path_to_check':'/', 'response_expected':200 },
                { 'ip':vip1SrvIp3, 'port':80, 'protocol':'tcp' }
            ]
        })
        
        vip2Ip     = long2ip(ip2long(net.default_route) + 10)
        vip2SrvIp1 = long2ip(ip2long(net.default_route) + 11)
        vip2SrvIp2 = long2ip(ip2long(net.default_route) + 12)
        
        vip2 = lb.add_virtual_ip()
        vip2.virtual_ip_address = vip2Ip
        vip2.port = 80
        vip2.delay_loop = 15
        vip2Srv1 = vip2.add_server()
        vip2Srv1.ip_address = vip2SrvIp1
        vip2Srv1.port = 80
        vip2Srv1.protocol = 'http'
        vip2Srv1.path_to_check = '/index.html'
        vip2Srv1.response_expected = 200
        vip2Srv2 = vip2.add_server()
        vip2Srv2.ip_address = vip2SrvIp2
        vip2Srv2.port = 80
        vip2Srv2.protocol = 'tcp'
        lb.save()
        lb.reload()
        
        self.assertEqual(len(lb.virtual_ips), 2)
        self.assertEqual(lb.virtual_ips[0].virtual_ip_address, vip1Ip)
        self.assertEqual(len(lb.virtual_ips[0].servers), 3)
        self.assertEqual(lb.virtual_ips[0].servers[0].ip_address, vip1SrvIp1)
        self.assertEqual(lb.virtual_ips[0].servers[0].port, 80)
        self.assertEqual(lb.virtual_ips[0].servers[0].protocol, 'http')
        self.assertEqual(lb.virtual_ips[0].servers[0].path_to_check, '/index.html')
        self.assertEqual(lb.virtual_ips[0].servers[0].response_expected, 200)
        self.assertEqual(lb.virtual_ips[0].servers[1].ip_address, vip1SrvIp2)
        self.assertEqual(lb.virtual_ips[0].servers[1].port, 80)
        self.assertEqual(lb.virtual_ips[0].servers[1].protocol, 'https')
        self.assertEqual(lb.virtual_ips[0].servers[1].path_to_check, '/')
        self.assertEqual(lb.virtual_ips[0].servers[1].response_expected, 200)
        self.assertEqual(lb.virtual_ips[0].servers[2].ip_address, vip1SrvIp3)
        self.assertEqual(lb.virtual_ips[0].servers[2].port, 80)
        self.assertEqual(lb.virtual_ips[0].servers[2].protocol, 'tcp')
        self.assertEqual(lb.virtual_ips[1].virtual_ip_address, vip2Ip)
        self.assertEqual(len(lb.virtual_ips[1].servers), 2)
        self.assertEqual(lb.virtual_ips[1].servers[0].ip_address, vip2SrvIp1)
        self.assertEqual(lb.virtual_ips[1].servers[0].port, 80)
        self.assertEqual(lb.virtual_ips[1].servers[0].protocol, 'http')
        self.assertEqual(lb.virtual_ips[1].servers[0].path_to_check, '/index.html')
        self.assertEqual(lb.virtual_ips[1].servers[0].response_expected, 200)
        self.assertEqual(lb.virtual_ips[1].servers[1].ip_address, vip2SrvIp2)
        self.assertEqual(lb.virtual_ips[1].servers[1].port, 80)
        self.assertEqual(lb.virtual_ips[1].servers[1].protocol, 'tcp')
        
        
        
        # setting virtual ips test 2
        
        lb.get_virtual_ip_by_address(vip1Ip).add_server({
            'ip': vip1SrvIp4,
            'port': 80,
            'protocol': 'ping'
        })
        lb.save()
        lb.reload()
        
        self.assertEqual(len(lb.virtual_ips), 2)
        self.assertEqual(len(lb.virtual_ips[0].servers), 4)
        self.assertEqual(lb.virtual_ips[0].servers[3].ip_address, vip1SrvIp4)
        self.assertEqual(lb.virtual_ips[0].servers[3].port, 80)
        self.assertEqual(lb.virtual_ips[0].servers[3].protocol, 'ping')
        self.assertEqual(len(lb.virtual_ips[1].servers), 2)
        
        
        
        # checking status
        
        lb.reload_status()
        for vip in lb.virtual_ips:
            print('  vip %s:%s every %ssec(s)' % (vip.virtual_ip_address, vip.port, vip.delay_loop))
            for server in vip.servers:
                msg = '    [%s(%s)]' % (server.status, server.active_connections)
                msg += ' server %s://%s' % (server.protocol, server.ip_address)
                if server.port: msg += ':%d' % (server.port)
                if server.path_to_check: msg += server.path_to_check
                msg += ' answers'
                if server.response_expected: msg += ' %d' % (server.response_expected)
                print(msg)
                # self.assertEqual(server.status, 'down')
        
        
        
        if not self.TESTS_CONFIG_READYMADE_LB_ID:
            
            # stop the LB
            time.sleep(1)
            print('ロードバランサを停止しています...')
            if not lb.stop().sleep_until_down(): fail('ロードバランサが正常に停止しません')
            
            # delete the LB
            print('ロードバランサを削除しています...')
            lb.destroy()



if __name__ == '__main__':
    unittest.main()
