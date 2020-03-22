$(document).ready(function(){
    $("#title").append(details["title"]);
    $("#rating").append(details["numerical"]);
    $("#media").append("<img src=\"" + details["media"] + "\">");
    $("#description").append(details["description"]);
    $("#visit-site").append("<a href=\"" + details["external_link"] + "\" target=\"_blank\">Visit the original site</a>")
    for(let list_index in details["list"]){
        $("#list").append("<div>" + details["list"][list_index] + "</div>");
    }
});