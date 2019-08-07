// require('tooltip.js');

$(document).ready(function () {
    progress_outcomes.forEach(function (progress_outcome, index) {
        var element_ref = 'input[value="' + progress_outcome.code + '"] + label';
        $(element_ref).tooltip({
            placement: 'top',
            title: progress_outcome.content,
            html: true
        });
    });
});
