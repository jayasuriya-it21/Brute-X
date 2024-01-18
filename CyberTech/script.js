$(document).ready(function () {
    // Animate between registration and login forms
    $("#RightToLeft").on("click", function () {
        $("#slide").animate({
            marginLeft: "0",
        });
        $(".top").animate({
            marginLeft: "100%",
        });
    });
    $("#LeftToRight").on("click", function () {
        $("#slide").animate({
            marginLeft: "50%",
        });
        $(".top").animate({
            marginLeft: "0",
        });
    });
});

