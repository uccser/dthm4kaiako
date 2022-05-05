var dayjs = require('dayjs');
var clock_element = document.getElementById('clock');
var schedule_element = document.getElementById('dashboard-schedule');


function updateClock() {
    var time = dayjs().format('h:mma');
    clock_element.innerHTML = time;
}


function updateSchedule() {
    $.ajax({
        type: "GET",
        url: JSON_URL,
        data: "slug=" + EVENT_SLUG,
        async: true,
        dataType: "json",
        success: updateScheduleHTML,
    });
}


function updateScheduleHTML(data) {
    schedule_element.innerHTML = data.schedule_html;
}

updateClock()
setInterval(updateClock, 1000);
updateSchedule()
setInterval(updateSchedule, 10000);
