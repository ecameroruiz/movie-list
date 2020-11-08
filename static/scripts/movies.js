/* -- Movies Script -- */

/**
 * Initialize Datatable
 */
$(document).ready(function() {
    $('#movies').DataTable( {
        'searching': false,
        'lengthMenu': [[25, 50, -1], [25, 50, 'All']],
    } );
});
