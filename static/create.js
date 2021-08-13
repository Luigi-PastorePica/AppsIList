$(document).ready(function(){

    $(".active").removeClass("active")
    $("#create").addClass("active");
    $("span .sr-only").remove();
    $("#create a").append("<span class=\"sr-only\">(current)</span>");

    $("#title-input").focus();
    $("form").bind("submit", preventDefault); // Default submit behavior for Bootstrap forms causes many undesirable effects

    $("#submit-button").on("click", function(){

        // TODO Extract class addition / removal.
        // TODO make class addition / removal code more elegant and less redundant (maybe a function that can be passed IDs and error message)
        let values_missing = true
        if(values_missing) {
            if ($("#title-input").val().trim() == '') {
                $("#title-warning").addClass("warning");
                $("#title-warning").html("Title field cannot be empty or consist of whitespaces");
                $("#title-input").focus();
                values_missing = true
            } else {
                $("#title-warning").removeClass("warning");
                $("#title-warning").html("");
                values_missing = false
            }
            // TODO Check that the link actually directs to a valid address. Better yet if it detects whether it is media.
            if ($("#media-link-input").val().trim() == '') {
                $("#media-link-warning").addClass("warning");
                $("#media-link-warning").html("Please provide a link to an image file that represents the resource");
                // $("#media-link-input").focus();
                values_missing = true
            } else {
                $("#media-link-warning").removeClass("warning");
                $("#media-link-warning").html("");
                values_missing = false
            }
            if ($("#format-input").val().trim() == '') {
                $("#format-warning").addClass("warning");
                $("#format-warning").html("Format field cannot be empty or consist of whitespaces");
                $("#format-input").focus();
                values_missing = true
            } else {
                $("#format-warning").removeClass("warning");
                $("#format-warning").html("");
                values_missing = false
            }
            if ($("#description-input").val().trim() == '') {
                $("#description-warning").addClass("warning");
                $("#description-warning").html("Description field cannot be empty or consist of whitespaces");
                // $("#description-input").focus();
                values_missing = true
            } else {
                $("#description-warning").removeClass("warning");
                $("#description-warning").html("");
                values_missing = false
            }
            // Notice ! at the beginning.
            if (!($("input[name='rating-selection']").is(":checked"))) {
                $("#rating-warning").addClass("warning");
                $("#rating-warning").html("Please select an option");
                values_missing = true
            } else {
                $("#rating-warning").removeClass("warning");
                $("#rating-warning").html("");
                values_missing = false
            }
            if ($("#review-input").val().trim() == '') {
                $("#review-warning").addClass("warning");
                $("#review-warning").html("Review field cannot be empty or consist of whitespaces");
                // $("#review-input").focus();
                values_missing = true
            } else {
                $("#review-warning").removeClass("warning");
                $("#review-warning").html("");
                values_missing = false
            }

            if ($("#external-link-input").val().trim() == '') {
                $("#external-link-warning").addClass("warning");
                $("#external-link-warning").html("Please provide a link to the page where the resource can be acquired (in a lawful manner)");
                // $("#external-link-input").focus();
                values_missing = true
            } else {
                $("#external-link-warning").removeClass("warning");
                $("#external-link-warning").html("");
                values_missing = false
            }
        }

        //TODO Show link to newly created document
        if(values_missing){
            // $("form").bind("submit", preventDefault);
            let warning_input_sibling = $("span.warning").first().prev();
            if (warning_input_sibling.className() !== "form-check") // This is brittle
                warning_input_sibling.focus(); // This is brittle and highly dependent on tag ordering. FIX
        } else {
            // $("form").unbind("submit", preventDefault);
            submit_new();
            // console.log("link returned by submit_new(): " + new_link);
            // clean_input();
            // $("#title-input").focus();
            // display_new_link(new_link);

        }
    });
});

//    Binding this function to the form disables the default behavior of the submit button, which clears the form when pressed.
//    Unbinding this function re-enables the default behavior of the submit button.
//    Obtained this solution from https://stackoverflow.com/questions/1164132/how-to-reenable-event-preventdefault
function preventDefault(event) {
    event.preventDefault();
};

// Temporary solution until I can figure out how to make Bootstrap forms submit functionality work nicely with JQuery.append
function clean_input(){
    $("#title-input").val('');
    $("#media-link-input").val('');
    $("#format-input").val('');
    $("#description-input").val('');
    // Incredibly helpful here https://stackoverflow.com/questions/977137/how-to-reset-radiobuttons-in-jquery-so-that-none-is-checked
    $('input[name="rating-selection"]').prop('checked', false);
    $("#review-input").val('');
    $("#external-link-input").val('');
};

function display_new_link(link){
    $("#create-successful").append(
        "<div><span class=\"bold text-center\">Success</span>. " +
        "New item successfully created. You can access it <a href=\"" + link + "\">here</a>" +
        "</div>");
}

function submit_new(){
    // console.log("submit_new was called");  // Debugging
    let new_item = {};
    new_item["title"] = $("#title-input").val();
    new_item["media"] = $("#media-link-input").val();
    new_item["format"] = $("#format-input").val();
    new_item["description"] = $("#description-input").val();
    // Learned how to extract value of selected radio input
    // https://www.tutorialrepublic.com/faq/how-to-get-the-value-of-selected-radio-button-using-jquery.php
    let rating = $("input[name='rating-selection']:checked").val();
    new_item["numerical"] = rating;
    new_item["external_link"] = $("#external-link-input").val();
    // new_item["list_elem"] = $("#review-input").val();
    let review = $("#review-input").val();
    new_item["list_elem"] = {};
    // This is used only to associate reviews to unique users.
    // Must be replaced by proper user id if the functionality is implemented in the future
    // A user should be able to leave only one review for a product or change their own review.
    let user_id = generate_placeholder_id();
    new_item["list_elem"][user_id] = {"rtng": rating, "review": review};
    console.log(JSON.stringify(new_item));
    $.ajax({
        type: "POST",
        url: "add_item",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(new_item),
        success: function(result) {
            // Should get the link to the new detail page and display it
            // console.log(result); // Debugging
            // console.log(result["link"]); // Debugging
            let new_link = result["link"];
            clean_input();
            $("#title-input").focus();
            display_new_link(new_link);
        },
        error: function(request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
        }
    });
};

// This function returns an integer between 1 and 1000 at random to be used as user id .
// It is not intended for production code.
function generate_placeholder_id() {
    // Copied randomizer from https://www.w3schools.com/js/js_random.asp
    return Math.floor(Math.random() * 1000) + 1;
}