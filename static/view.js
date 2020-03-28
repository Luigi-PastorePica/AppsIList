$(document).ready(function(){

    render_view();

    $("#edit-description").on("click", function(){
        make_description_editable();
    });

    //TODO make these functions be generic.
    $("#submit-changes").on("click", function(){
        let new_value = $("textarea").val();
        //TODO make changes on server
        $.ajax({
            type: 'POST',
            url: "update/" + details["id"],
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({new_value: new_value}),
            success: function(result){

            },
            error: function(request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
            }
        })
        //TODO request /view/<id> again
    });

    $("#discard-changes").on("click", function(){
        //TODO request /view/<id> again OR rerender section of the page.
    });
});

function render_view(){
    $("#title").append(details["title"]);
    $("#rating").append(details["numerical"]);
    $("#media").append("<img class=\"img-fluid\" src=\"" + details["media"] + "\">");
    $("#description").prepend("<p>" + details["description"] + "</p>");
    $("#visit-site").prepend("<a href=\"" + details["external_link"] + "\" target=\"_blank\">Visit the original site</a>");
    // details_list = details["list"].split("', ");
    // for(let list_index in details_list){
    //     console.log(typeof(details_list));
    //     console.log((details_list));
    //     // console.log(typeof(details["list"][list_index]));
    //     // console.log(details["list"][list_index]);
    //     $("#list").append("<div class=\"col-12\">" + details_list[list_index] + "</div>");
    for(let list_idx in details["list"]){
        console.log("type of details[\"list\"]" + typeof(details["list"])); // Debugging
        console.log("details[\"list\"]" + details["list"]); // Debugging
        console.log("type of details[\"list\"][list_idx]" + typeof(details["list"][list_idx])); // Debugging
        console.log("details[\"list\"][list_idx]" + details["list"][list_idx]); // Debugging
        details["list"][list_idx] = trim_quotes(details["list"][list_idx]);
        console.log("details[\"list\"][list_idx]" + details["list"][list_idx]); // Debugging
        $("#list").append("<div class=\"col-12\">" + details["list"][list_idx] + "</div>");
    }
}

function trim_quotes(string){
    let start = 0;
    let end = string.length - 1;
    if(string[start] === "'" || string[start] === "\""){
        start += 1;
    }
    if(string[end] === "'" || string[end] === "\""){
        end -= 1
    }

    return string.slice(start, end + 1)
}

function make_description_editable(){
    alert("i was called!!!")
    let parent = $("#edit-description").parent();
    parent.empty();
    parent.append("<textarea>" + details["description"] + "</textarea>");
    $("textarea").focus();
    parent.append("<button id=\"submit-changes\">Submit</button>");
    parent.append("<button id=\"discard-changes\">Discard</button>");
}