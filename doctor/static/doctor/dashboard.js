$(document).ready(function() {
    $(".upload-input").change(function () {
        alert("The image has been uploaded. Press Upload to finalize.");
    });
    for (app in week_appointment){
        idToFind = "#"+app.toString()+week_appointment[app][0].toString()
        $(idToFind).addClass("active").append(week_appointment[app][1]);
    }
})

