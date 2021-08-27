var tbInvoicePay;
var modal_title;

function getData() {
    tbInvoicePay = $('#data').DataTable({
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
                render: function (data, type, row) {
                    let provider = data.names + ' (' + data.ci + ') ' + data.address;
                    return provider;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: true,
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
        maxDate: moment().format("YYYY-MM-DD")
    });

    $('.btnAddInvoicePay').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Registrar Pago');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus')
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('form')[0].reset();
        $('#modalInvoicePay').modal('show');
    });

    $('.btnAddProvider').on('click', function () {
        $('input[name="action"]').val('addProvider');
        modal_title.find('span').html('Nuevo Proveedor');
        $('form')[1].reset();
        $('#modalProviders').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('span').html('Editar Información de Pago');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit')
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbInvoicePay.cell($(this).closest('td, li')).index();
        let data = tbInvoicePay.row(tr.row).data();
        $('form')[0].reset();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('select[name="provider"]').val(data.provider.id);
        $('input[name="quantity"]').val(data.quantity);
        $('input[name="pay_date"]').val(data.pay_date);
        $('#id_description').val(data.description);
        $('#modalInvoicePay').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbInvoicePay.cell($(this).closest('td, li')).index();
            let data = tbInvoicePay.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar el siguiente registro?', parameters, function () {
                alertSweetSuccess('Listado de Pagos de Facturas actualizado');
                setTimeout(tbInvoicePay.ajax.reload(), 5000);
            });
        });

    $('.formInvoicePay').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalInvoicePay').modal('hide');
            alertSweetSuccess('Listado de Pagos de Facturas actualizado');
            setTimeout(tbInvoicePay.ajax.reload(), 5000);
        });
    });

    $('.formProviders').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalProviders').modal('hide');
            alertSweetSuccess('Nuevo Proveedor registrado con éxito');
            setTimeout(window.location.reload(), 5000);
        });
    });
});

