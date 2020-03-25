$(document).ready(function(){

    $("form").bind("submit", preventDefault); // Default submit behavior for Bootstrap forms causes many undesirable effects

    $("#go-button").on("click", function () {
        let search_string = $("#search-input").val().trim();
        if(search_string !== ''){
            search(search_string);
        }
        else {
            warn_no_string();
        }
    });

    // let fragment_url = "/auto/" + fragment;
    $("#search-input").autocomplete("option", "source", "/auto/");
})


//    Binding this function to the form disables the default behavior of the submit button, which clears the form when pressed.
//    Unbinding this function re-enables the default behavior of the submit button.
//    Obtained this solution from https://stackoverflow.com/questions/1164132/how-to-reenable-event-preventdefault
function preventDefault(event) {
    event.preventDefault();
}

function search(search_string){
    console.log("search string: " + search_string);
    window.location.href="/search/" + search_string;
    // let search_url = "search/" + search_string;
    // $.ajax({
    //     type: "GET",
    //     url: search_url,
    //     dataType: "json",
    //     // contentType: "application/json; charset=utf-8",
    //     // data: JSON.stringify(new_item),
    //     success: function(results) {
    //         console.log("Received search results: " + results);
    //         window.location.href="/search_results";
    //     },
    //     error: function(request, status, error) {
    //         console.log("Error");
    //         console.log(request);
    //         console.log(status);
    //         console.log(error);
    //     }
    // })
}

function search_fragment(fragment){
    let fragment_url = "/auto/" + fragment;
    $("#search-input").autocomplete("option", "source", fragment_url);
}

function warn_no_string() {
    let no_string_message = "Please input a term to search for in the search box. Then click on \"Go\"."
    $("#search-warning").append("<div class=\"warning\" offset-1 col-10 offset-md-8 col-md-4>" + no_string_message + "</div>");
}