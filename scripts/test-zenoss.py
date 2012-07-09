#!/usr/bin/python

import json
import urllib
import urllib2

ROUTERS = { 'MessagingRouter': 'messaging',
            'EventsRouter': 'evconsole',
            'ProcessRouter': 'process',
            'ServiceRouter': 'service',
            'DeviceRouter': 'device',
            'NetworkRouter': 'network',
            'TemplateRouter': 'template',
            'DetailNavRouter': 'detailnav',
            'ReportRouter': 'report',
            'MibRouter': 'mib',
            'ZenPackRouter': 'zenpack' }


class ZenossAPI(object):
    def __init__(self,zenoss_url,zenoss_user,zenoss_pw,debug=False):
        try:
            self._server=urllib2.build_opener(urllib2.HTTPCookieProcessor())
            if debug:
                self._server.add_handler(urllib2.HTTPSHandler(debuglevel=1))
        except Exception,e:
            print e

        self._zenoss_url=zenoss_url
        self._reqCount=1
        loginParams=urllib.urlencode(dict(
            __ac_name=zenoss_user,
            __ac_password=zenoss_pw,
            submitted = 'true',
            came_from=zenoss_url+'/zport/dmd'))
        result=self._server.open(zenoss_url+'/zport/acl_users/cookieAuthHelper/login',loginParams)

    def _router_request(self,router,method,data=[]):
        if router not in ROUTERS:
            raise Exception('Router "'+router+'" not available')
        url='%s/zport/dmd/%s_router' % (self._zenoss_url,ROUTERS[router])
        print url
        reqData=json.dumps([dict(
            action=router,
            method=method,
            data=data,
            type='rpc',
            tid=self._reqCount
        )])
 
        req=urllib2.Request(url,reqData)
        req.add_header('Content-Header','application/json; charset=utf-8')
        reqData=json.dumps([dict(
            action=router,
            method=method,
            data=data,
            type='rpc',
            tid=self._reqCount
        )])
        print reqData 
        self._reqCount+=1
        request=self._server.open(req)
        return json.loads(request.read())

    def get_devices(self,deviceClass='/zport/dmd/Devices'):
        result=self._router_request('DeviceRouter','getDevices',data=[{'uid':deviceClass,'params':{"limit":1000}}])
        print result


if __name__=='__main__':
    zo=ZenossAPI('https://zenossdev.qai.expertcity.com','sadig','Cd12vf34!',True)
    print zo.get_devices()