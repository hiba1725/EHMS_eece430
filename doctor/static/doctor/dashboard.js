$(document).ready(function() {
    $(".upload-input").change(function () {
        alert("The image has been uploaded. Press Upload to finalize.");
    });
    // console.log(week_appointment)
    for (let day in week_appointment){
        for (let slot in week_appointment[day]) {
            let idToFind = "#" + day.toString() + week_appointment[day][slot][0].toString()
            $(idToFind).addClass("myactive").append(week_appointment[day][slot][1]);
        }
    }
})

