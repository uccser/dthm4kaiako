$(document).ready(function () {
    // Clear form button.
    updateFilterSummary();
    $('#clear-form').click(resetResourceSearchForm);
    $('#resource-search input[type=checkbox]').change(updateFilterSummary);
});

function resetResourceSearchForm() {
    /**
     * Clear all elements of form.
     */
    $('#resource-search #id_q').val('');
    $('#resource-search input[type=checkbox]').prop('checked', false);
    updateFilterSummary();
};


function updateFilterSummary() {
    /**
     * Update the summary of applied filters.
     */
    var $summary_text = $('#filter-summary-text');
    var $summary_badges = $('#filter-summary-badges');
    $summary_badges.empty();
    var filter_count = 0;

    $('#resource-search input[type=checkbox]:checked').each(function () {
        filter_count++;
        var label = $("label[for='" + $(this).attr('id') + "']");
        $summary_badges.append(label.html());
    });

    if (filter_count == 1) {
        $summary_text.text('1 filter applied');
    } else {
        $summary_text.text(filter_count + ' filters applied');
    }
};
