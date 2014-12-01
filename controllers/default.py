# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
	redirect(URL('cassandra'))
	return dict()

def ins():
	print "hello"
	import requests
	import urllib2
	import os
	ans = "/"
	i=0
	while i < len(request.args):
			ans = ans + request.args[i]+'/'
			i+=1
	some_url = 'curl -X PUT http://localhost:8080/flask/data'
	some_url+=ans
	

	some_url+=" -d " + "\"{\\\"Description\\\":\\\"GDP (in Rs. Cr.)\\\",\\\"Araria\\\":\\\"886.89\\\",\\\"Arwal\\\":\\\"263.82\\\",\\\"Aurangabad\\\":\\\"1000.92\\\",\\\"Banka\\\":\\\"681.84\\\",\\\"Begusarai\\\":\\\"1747.91\\\",\\\"Bhabhua\\\":\\\"681.95\\\",\\\"Bhagalpur\\\":\\\"1551.67\\\",\\\"Bhojpur\\\":\\\"1239.83\\\",\\\"Buxar\\\":\\\"761.04\\\",\\\"Champaran: East\\\":\\\"1764.31\\\",\\\"Champaran: West\\\":\\\"1657.79\\\",\\\"Darbhanga\\\":\\\"1516.72\\\",\\\"Gaya\\\":\\\"1869.33\\\",\\\"Gopalgang\\\":\\\"1020.65\\\",\\\"Jahanabad\\\":\\\"457.46\\\",\\\"Jamui\\\":\\\"624.65\\\",\\\"Katihar\\\":\\\"1191.06\\\",\\\"Khagaria\\\":\\\"631.9\\\",\\\"Kisangang\\\":\\\"607.44\\\",\\\"Lakhisarai\\\":\\\"411.19\\\",\\\"Madhepura\\\":\\\"681.41\\\",\\\"Madhubani\\\":\\\"1561.3\\\",\\\"Munger\\\":\\\"958.73\\\",\\\"Muzaffarpur\\\":\\\"2395.42\\\",\\\"Nalanda\\\":\\\"1269.13\\\",\\\"Nawada\\\":\\\"810.4\\\",\\\"Patna\\\":\\\"10355.18\\\",\\\"Purnia\\\":\\\"1225.58\\\",\\\"Rohtas\\\":\\\"1486.02\\\",\\\"Saharsa\\\":\\\"827.97\\\",\\\"Samstipur\\\":\\\"1666.73\\\",\\\"Saran\\\":\\\"1455.46\\\",\\\"Sekhpura\\\":\\\"248.52\\\",\\\"Sheohar\\\":\\\"168.39\\\",\\\"Sitamarhi\\\":\\\"1118.78\\\",\\\"Siwan\\\":\\\"1227.12\\\",\\\"Supaul\\\":\\\"792.83\\\",\\\"Vaishali\\\":\\\"1382.59\\\"}\""
	
	some_url+=" --noproxy localhost"
	print some_url
	os.system(some_url)
	redirect(URL('cassandra'))

def cassandra():

	import requests
	import urllib2
	import json
	import collections
	
	ans = "/"
	try:
		page=int(request.vars["page"])
	except:
		page = 0
	pass
	print page
	print "*"	
	i=0
	while i < len(request.args):
			ans = ans + request.args[i]+'/'
			i+=1
	items_per_page=10

	proxy_handler = urllib2.ProxyHandler({})
	opener = urllib2.build_opener(proxy_handler)
	some_url = 'http://localhost:8080/flask/data'
	some_url+=ans
	r = urllib2.Request(some_url)
	x = opener.open(r)
	y = x.read()
	result = json.loads(y)
	flag = 1
	print some_url
	print len(result)
	if type(result) is not list:
		flag = 0
	response.flash = T("Cassandra WebAPI!")
	return dict(args2=request.args,flag=flag,result=result,page=page,items_per_page=items_per_page)

def delete_row():
	import requests
	import urllib2
	import os
	ans = "/"
	i=0
	while i < len(request.args):
			ans = ans + request.args[i]+'/'
			i+=1
	some_url = 'curl -X DELETE http://localhost:8080/flask/data'
	some_url+=ans
	some_url+=" --noproxy localhost"
	print some_url
	os.system(some_url)
	redirect(URL('cassandra'))
	
def user():

    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
