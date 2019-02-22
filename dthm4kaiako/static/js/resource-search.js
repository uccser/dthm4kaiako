$(document).ready(function () {
    // Clear form button.
    $('#clear-form').click(resetResourceSearchForm);
});

function resetResourceSearchForm() {
    /**
     * Clear all elements of form.
     *
     * @param {string} form_id - ID of form to clear.
     */
    $('#resource-search #id_q').val('');
    $('#resource-search input[type=checkbox]').prop('checked', false);
}
