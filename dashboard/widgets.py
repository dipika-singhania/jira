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
        import ipdb; ipdb.set_trace()
        url = "https://gale43.atlassian.net/rest/api/2/search"
        variable = "(status IN (1,3,4,10006,10403,\
            10701,10900,11100,11200))"
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
        variable = "status IN (5,6,10000,10601,11101)"
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
            if(totalIssues == 0):
                perComp = 0
            else:
                perComp = (resolvedIssues * 100) / totalIssues

            data.append({'x': i, 'y': perComp})
            initialDate = initialDate + datetime.timedelta(days=5)
            i += 1
        data.append({'x': i, 'y': 100})
        print data
        return data

class Top20OpenList(ListWidget):
    title = "Top 20 Candis with max open bugs"
    def getValueFromJsonObj(self, obj, avatars_Dict):
        issues = obj['issues']
        for issue in issues:
            try:
                assignee = issue['fields']['assignee']['displayName']
                try:
                    avatars_Dict[assignee] += 1
                except KeyError:
                    avatars_Dict[assignee] = 1
            except:
                continue
        return avatars_Dict

    def get_data(self):
        url = "https://gale43.atlassian.net/rest/api/2/search"
        condition = "(status IN (1,3,4,10006,10403,\
                10701,10900,11100,11200))"
        data_api = json.dumps({
                        "jql": condition,
                        "startAt": 0
                        })
        res = getAPIResponse(url, data_api)
        json_obj = json.loads(res)
        total_issues = int(json_obj['total'])
        max_results = int(json_obj['maxResults'])
        avatars_dict = {}
        avatars_dict = self.getValueFromJsonObj(json_obj, avatars_dict)
        loop_count = 0
        if(total_issues > max_results):
            loop_count = total_issues / max_results
            if((total_issues % max_results) != 0):
                loop_count += 1

        for i in range(1, loop_count+1):
            start_var = i * max_results
            data_api = json.dumps({
                            "jql": condition,
                            "startAt": start_var
                            })
            res = getAPIResponse(url, data_api)
            json_obj = json.loads(res)
            avatars_dict = self.getValueFromJsonObj(json_obj, avatars_dict)
            print(i, ":", avatars_dict)

        import operator
        sorted_avatars = sorted(avatars_dict.items(), key=operator.itemgetter(1), reverse=True )
        print sorted_avatars
        data = [{'label': key, 'value': value} for key, value in sorted_avatars[:21]]
        return data
