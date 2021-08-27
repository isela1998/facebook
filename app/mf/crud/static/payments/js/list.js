var tbPayments;
var modal_title;

function getData() {
    tbPayments = $('#data').DataTable({
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
            { "data": "pay_date" },
            { "data": "provider" },
            { "data": "description" },
            { "data": "quantity" },
            { "data": "image" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-5],
                class: 'text-left',
                orderable: false,
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let img = '<a class="img-capture" href="../../../media/' + data + '" target="_blank"><i class="fas fa-search"></i></a>';
                    return img;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" data-title="Editar" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" type="button" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ]
    })
}

$(function () {

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-file-invoice-dollar')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-dollar-sign')

    getData();

    $('#pay_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        let tr = tbPayments.cell($(this).closest('td, li')).index();
        let data = tbPayments.row(tr.row).data();
        $('form')[0].reset();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="provider"]').val(data.provider);
        $('input[name="quantity"]').val(data.quantity);
        $('input[name="pay_date"]').val(data.pay_date);
        $('#id_description').val(data.description);
        $('#modalPayments').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbPayments.cell($(this).closest('td, li')).index();
            let data = tbPayments.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Listado de Abonos de Facturas actualizado');
                setTimeout(tbPayments.ajax.reload(), 5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalPayments').modal('hide');
            alertSweetSuccess('Listado de Abonos de Facturas actualizado');
            setTimeout(tbPayments.ajax.reload(), 5000);
        });
    });
});

