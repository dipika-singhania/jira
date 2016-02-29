from dashing.widgets import NumberWidget, GraphWidget, ListWidget
import json
import urllib2
import base64
from datetime import date
import datetime

def getAPIResponse(url, data):
    username = 'dipika.singhania'
    password = 'gale@123!'
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request = urllib2.Request(url, data, {
        'Authorization': 'Basic %s' % auth,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })
    return urllib2.urlopen(request).read()


class OpenIssuesWidget(NumberWidget):
    title = "Issues in Blue-Gray or Yellow Belt"
    detail = "Todo/Open/ReOpened/InProgress/Verification/Escalation issues for all projects"
    col = 2
    def get_value(self):
        url = "https://gale43.atlassian.net/rest/api/2/search"
        variable = "(status IN (1,3,4,10006,10403,10701,10900,11100,11200))"
        data = json.dumps({
                        "jql": variable,
                        "startAt": 0
                        })
        res = getAPIResponse(url, data)
        value = json.loads(res)['total']
        print("Value = ", value)
        return value

class ClosedIssuesWidget(NumberWidget):
    title = "Issues in Green Belt"
    detail = "Done/Resolved/Delivered/QAVerified/Accepted issues for all projects"
    col = 2
    def get_value(self):
        url = "https://gale43.atlassian.net/rest/api/2/search"
        variable = "status NOT IN (5,6,4,10006,10403,10701,10900,11100,11200)"
        data = json.dumps({
                        "jql": variable,
                        "startAt": 0
                        })
        res = getAPIResponse(url, data)
        value = json.loads(res)['total']
        print("Value = ", value)
        return value

class CompletionGraph(GraphWidget):
    title = "Completion Percentage"
    def get_data(self):
        data = []
        initialDate = datetime.date(2015, 12, 30)
        i = 0
        while(initialDate < date.today()):
            url = "https://gale43.atlassian.net/rest/api/2/search"
            d = "\"" + initialDate.strftime("%Y/%m/%d") + "\""
            variable = '(due < %s)' % d
            print("variable=%s" % variable)
            data_api = json.dumps({
                            "jql": variable,
                            "startAt": 0
                            })
            res = getAPIResponse(url, data_api)
            totalIssues = json.loads(res)['total']

            variable = '(resolved < %s) and (due < %s)' % (d, d)
            data_api = json.dumps({
                            "jql": variable,
                            "startAt": 0
                            })
            res = getAPIResponse(url, data_api)
            resolvedIssues = json.loads(res)['total']
            print ("(resolved,totalissues)=(%s,%s)" % (resolvedIssues, totalIssues))
            if(totalIssues==0):
                perComp = 0
            else:
                perComp = (resolvedIssues * 100) / totalIssues

            data.append({'x': i, 'y': perComp})
            initialDate = initialDate + datetime.timedelta(days=5)
            i += 1
        data.append({'x': i, 'y': 100})
        print data
        return data

def Top10OpenList(ListWidget):
    print "hello"
    '''
    title: "Top 20 Candis with max open bugs"
    url = "https://gale43.atlassian.net//rest/api/2/project"
    res = getAPIResponse(url, none)
    projects = json.loads(res)
    for project in projects:
        url = project['self'] + "/avatars"
        projectid = project['id']
        res = getAPIResponse(url, none)
        avatars = json.loads(res)
        for avatar in avatars:
            avatar_id = avatar['id']
            url = "https://gale43.atlassian.net/rest/api/2/search"
            d = "\"" + initialDate.strftime("%Y/%m/%d") + "\""
            variable = '(due < %s)' % d
            print("variable=%s" % variable)
            data_api = json.dumps({
                            "jql": variable,
                            "startAt": 0
                            })
            res = getAPIResponse(url, data_api)
            totalIssues = json.loads(res)['total']
    '''
