var tbBankTransfer;
var modal_title;

function getData() {
    tbBankTransfer = $('#data').DataTable({
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
            { "data": "referenceNumber" },
            { "data": "bank" },
            { "data": "total" },
            { "data": "description" },
            { "data": "image" },
            { "data": "id" }
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let img = '<a data-title="Ver Comprobante" class="img-capture" href="../../../media/' + data + '" target="_blank"><i class="fas fa-search"></i></a>';
                    return img;
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let referenceNumber = '<span class="badge badge-info font-15 fill-available">' + data + '</span>';
                    return referenceNumber;
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    let bank = data.bank + ' ' + data.accountHolder + ' ' + data.holderId + '<br>' + data.accountNumber;
                    return bank;
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: true,
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" data-title="Editar datos" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" type="button" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ]
    })
}

$(function () {

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-university')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-tasks')

    getData();

    $('#pay_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });

    $('.btnAddBankTransfers').on('click', function () {
        $('form')[0].reset();
        modal_title.find('span').html('Registrar Transferencia');
        $('input[name="action"]').val('add');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('#modalBankTransfers').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();
        modal_title.find('span').html('Editar Datos de la Transferencia');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbBankTransfer.cell($(this).closest('td, li')).index();
        let data = tbBankTransfer.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="pay_date"]').val(data.pay_date);
        $('input[name="referenceNumber"]').val(data.referenceNumber);
        $('select[name="bank"]').val(data.bank.id);
        $('input[name="total"]').val(data.total);
        $('textarea[name="description"]').val(data.description);
        $('#modalBankTransfers').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbBankTransfer.cell($(this).closest('td, li')).index();
            let data = tbBankTransfer.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Listado de transferencias actualizado');
                setTimeout(tbBankTransfer.ajax.reload(), 5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalBankTransfers').modal('hide');
            alertSweetSuccess('Listado de transferencias actualizado');
            setTimeout(tbBankTransfer.ajax.reload(), 5000);
        });
    });
});

