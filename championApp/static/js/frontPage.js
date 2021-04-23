$(document).ready(function () {
    $(".content2").hide();
    $("#toggle").click(function () {
        var txt =$(".content2").is(":visible")? "Read More" : "Read Less";
        $("#toggle").text(txt);
        $(".content2").slideToggle("slow")   
    });
});