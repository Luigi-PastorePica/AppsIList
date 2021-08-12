

$(document).ready(function(){

    render_view();

    $("#edit-description").on("click", function(){
        make_description_editable();
    });

    $("#edit-link").on("click", function () {
        make_external_link_editable();
    })

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
    console.log(details);
    let reviews = JSON.parse(details["list"]);
    let user_ids = Object.keys(reviews);
    let rating_cumulative = parseFloat(details["numerical"]);
    let nbr_of_reviews = user_ids.length;
    let rating_avg = rating_cumulative / nbr_of_reviews;
    console.log(rating_cumulative);
    console.log(nbr_of_reviews);
    console.log(rating_avg);
    $("#title").append(details["title"]);
    $("#rating").append("Usefulness: " + rating_avg.toString());
    $("#media").append("<img class=\"img-fluid\" src=\"" + details["media"] + "\">");
    // $("#description").prepend("<p>" + details["description"] + "</p>");
    $("#description").prepend(details["description"]);
    $("#visit-site").prepend("<a href=\"" + details["external_link"] + "\" target=\"_blank\">Visit the original site</a>");

    // console.log(reviews); // Debugging
    // console.log(user_ids); // Debugging
    // console.log(reviews[user_ids[0]]); // Debugging

    for(let id in user_ids){
        let review_row_html =
            "<div class=\"col-12\">" +
            "<div class=\"row\">" +
            "<div class=\"col-3\"> User ID: " + user_ids[id] + "</div>" +
            "<div class=\"text-left col-9\">Usefulness: " + reviews[user_ids[id]]["rtng"] + "</div>" +
            "</div>" +
            "<div class=\"row\">" +
            "<div class=\"col-11\">" + reviews[user_ids[id]]["review"] + "</div>" +
            "<div class=\"col-1\">" +
            "<button id=\"delete-review-" + user_ids[id] + "\">Delete" +
            "</button>" +
            "</div>" +
            "</div>" +
            "</div>";
        $("#list").append(review_row_html);
        // $("#list").append("<div class=\"col-4\"> User ID: " + user_ids[id] + "</div>");
        // $("#list").append("<div class=\"text-left col-8\">" + reviews[user_ids[id]]["rtng"] + "</div>");
        // $("#list").append("<div class=\"col-12\">" + reviews[user_ids[id]]["review"] + "</div>");
    }

}

// TODO These two below can be combined and passed the id.
function make_description_editable(){
    let parent = $("#edit-description").parent();
    parent.empty();
    parent.append("<textarea class=\"editable-textarea\" rows=\"11\">" + details["description"] + "</textarea>");
    $("textarea").focus();
    parent.append("<button type=\"button\" id=\"submit-changes\" class=\"btn btn-outline-success\">Submit</button>");
    parent.append("<button type=\"button\" id=\"discard-changes\" class=\"btn btn-outline-danger\">Discard</button>");
}

function make_external_link_editable(){
    let parent = $("#edit-link").parent();
    parent.empty();
    parent.append("<textarea class=\"editable-textarea\">" + details["external_link"] + "</textarea>");
    $("textarea").focus();
    parent.append("<button id=\"submit-changes\">Submit</button>");
    parent.append("<button id=\"discard-changes\">Discard</button>");
}

// Not used anymore, but can come in handy in the future.
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

