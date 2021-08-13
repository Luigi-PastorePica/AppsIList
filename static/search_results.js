$(document).ready(function(){

    // $("form").bind("submit", preventDefault); // Default submit behavior for Bootstrap forms causes many undesirable effects

    if(title_results.length === 0 && content_results.length === 0){
        display_no_results();
    }
    else {
        let search_results = {"title_results": title_results, "content_results": content_results};
        display_search_results(search_results);
    }
    display_search_results();
    highlight_search_string();
})


function display_search_results(search_results) {
    let title_result_count_html =
        "<div id=\"title-results-count\" class=\"col-12 mb-2 results\">" +
        "There were <span class=\"bold\">" + search_results["title_results"].length + "</span> results with " +
        "<span class=\"bold\">" + search_str + "</span> in the title" +
        "</div>";
    let content_result_count_html =
        "<div id=\"content-results-count\" class=\"col-12 mb-2 results\">" +
        "There were <span class=\"bold\">" + search_results["content_results"].length + "</span> results with " +
        "<span class=\"bold\">" + search_str + "</span> in other parts of the item's details." +
        "</div>";

    $("#search-results").append(title_result_count_html);
    append_cards(search_results["title_results"], $("#search-results"));
    $("#search-results").append("<div class=\"col-12 my-2\"><hr></div>");
    $("#search-results").append(content_result_count_html);
    append_cards(search_results["content_results"], $("#search-results"));
    // highlight_search_string();

}

function append_cards(search_results, jq_selector){
    // TODO Duplicate code from home.js. Refactor.
    for(let item_idx in search_results){
        let item = search_results[item_idx];
        console.log("result item: " + JSON.stringify(item)); // Debugging
        let card_html =
            "<div class=\"col-12 col-md-6\">" +
              "<div class=\"card border-dark mb-3\">" +
                "<div class=\"row\">" +
                  "<div class=\"col-4\">" +
                    "<a href=\"/view/" + item["id"] + "\">" +
                      "<img class=\"card-img img-fluid\" src=\"" + item["media"] + "\" href alt=\"\">" +
                    "</a>" +
                  "</div>" +
                  "<div class=\"col-8\"" +
                    "<div class=\"card-body\">" +
                      "<h5 class=\"card-title\">" + item["title"] + "</h5>" +
                      "<h6 class=\"card-subtitle text-muted\">" + item["format"] + "</h6>" +
                      "<p class=\"card-text\">Rating" + item["numerical"] + "</p>" +
                    "</div>" +
                  "</div>" +
                "</div>" +
              "</div>" +
            "</div>";
        jq_selector.append(card_html)
    }
}

function display_no_results() {
    let no_results_message = "Sorry, no results found. Maybe you can try a different search term in the search box above."
    $("#search-results").append("<div class=\"no-results\">" + no_results_message + "</div>");
}

function highlight_search_string() {
    let search_str = search_str;
    // let search_str_lower = search_str.toLowerCase();
    // console.log("Trying to highlight: " + search_str); // Debugging
    // console.log("search_str: " + search_str); // Debugging
    // $("div").filter(function() { return $(this).text().toLowerCase() === "Python".toLowerCase();}).addClass("highlight-string");
}