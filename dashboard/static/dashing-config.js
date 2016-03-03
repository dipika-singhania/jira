/* global $, Dashboard */

var dashboard = new Dashboard();

function httpGet(theUrl,callback,name,type,row,col)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            callback(xmlHttp.responseText,name,type,row,col);
        }
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function curEvalWidget(json_text,name,type,row,col){
    dashboard.addWidget(name, type , {
      row: row,
      col: col,
      getData: function () {
        $.extend(this.scope,JSON.parse(json_text));
      }
    });
}

function callMethods(projectid) {
    // httpGet('http://localhost:8000/dashing/widgets/custom_widget/3', curEvalWidget , 'c1' , 'Number',1,1)
    httpGet('http://localhost:8000/dashing/widgets/open_issues/'+projectid, curEvalWidget , 'open_issues' , 'Number',1,3)
    // httpGet('http://localhost:8000/dashing/widgets/close_issues/'+projectid, curEvalWidget , 'close_issues' , 'Number',1,3)
    // httpGet('http://localhost:8000/dashing/widgets/open_list/'+projectid, curEvalWidget , 'open_list' , 'List',3,1)
    // httpGet('http://localhost:8000/dashing/widgets/completion/'+projectid, curEvalWidget , 'completion' , 'Graph',2,3)
}