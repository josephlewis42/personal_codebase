function Reload(timeoutPeriod)
{
    setTimeout("location.reload(true);",timeoutPeriod);
}

function Update(timeoutPeriod, widgetname, updateurl)
{
    $(widgetname).load(updateurl);  //Reload right away
    var html = setInterval("$(\""+widgetname+"\").load(\""+updateurl+"\")", timeoutPeriod);
}