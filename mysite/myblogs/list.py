from django.shortcuts import render
import os
from keystoneclient.v3 import client as lient
from swiftclient import client
from keystoneauth1 import session
from keystoneauth1.identity import v3
def con():
    _authurl = 'http://object:35357/v3'
    _auth_version = '3'
    _user = 'admin'
    _key = '684739'
    _os_options = {
        'user_domain_name': 'default',
        'project_domain_name': 'default',
        'project_name': 'admin'
    }

    conn = client.Connection(
       authurl=_authurl,
       user=_user,
       key=_key,
       os_options=_os_options,
       auth_version=_auth_version
    )
    return conn
def list():
    conn=con()
    resp_headers,objects = conn.get_container('Ben')
    #print("Response headers: %s" % resp_headers)
    for object in objects:
        #print(object.get(u'name'))
         print(object)
list()      
def keys():
    auth = v3.Password(auth_url='http://object:35357/v3/',
                   username='admin',
                   password='684739',
                   user_domain_name='default',
                   project_name='admin',
                   project_domain_name='default')
    keystone_session = session.Session(auth=auth)
    conn =client. Connection(session=keystone_session)
    return conn 

