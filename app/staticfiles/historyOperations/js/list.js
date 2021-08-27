var tbOperationsHistory;
var modal_title;

function getData() {
    tbOperationsHistory = $('#data').DataTable({
        ordering: true,
        searching: true,
        paging: true,
        info: false,
        pagingType: 'simple_numbers',
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        dom: '<"myCustomClass"f>rt<"bottom"lp><"clear">',
        fnDrawCallback: function () {
            $("input[type='search']").attr("id", "searchBox");
            $("input[type='search']").attr("autocomplete", "off");
            $("select[name='data_length'], #searchBox").removeClass("input-sm");
            $('#searchBox').css("width", "350px").focus();
            $('#data').removeClass('dataTables_filter');
        },
        columns: [
            { "data": "datejoined" },
            { "data": "user" },
            { "data": "name" },
            { "data": "action" },
        ],
        columnDefs: [
            // {
            //     targets: [-1,-2],
            //     class: 'text-center',
            //     orderable: true,
            //     render: $.fn.dataTable.render.number('.', ',', 2)
            // },
        ],
        initComplete: function (settings, json) {

        }
    })
}

$(function () {

    modal_title = $('.modal-title')

    $('#i_card_title').removeClass().addClass('text-dark fas fa-money-check-alt')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-check-square')

    getData();

    $('.delete-history').on('click', function() {
        let parameters = new FormData();
        parameters.append('action', 'delete');
        submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar todo el historial de operaciones?', parameters, function () {
            alertSweetSuccess('Realizado con éxito');
            setTimeout(tbOperationsHistory.ajax.reload(), 4000);
        });
    });
});