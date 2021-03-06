let newest_url = "/newest";
// let db = [];
// let newest = {{newest|tojson}}
$(window).on("load", function(){

    $(document).ready(function(){
        $(".active").removeClass("active")
        $("#home").addClass("active");
        $("span .sr-only").remove();
        $("#home a").append("<span class=\"sr-only\">(current)</span>");
        display_newest();
    })

})

function display_newest(){

    for(let item_idx in newest){
        item = newest[item_idx]
        card_html =
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
                      "<h6 class=\"card-subtitle text-muted\">" + "Category here" + "</h6>" +
                      "<p class=\"card-text\">Rating" + item["numerical"] + "</p>" +
                    "</div>" +
                  "</div>" +
                "</div>" +
              "</div>" +
            "</div>";
        $("#newest-entries").prepend(card_html)
    }
}