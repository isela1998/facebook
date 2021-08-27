var tbBankAccount;
var modal_title;

function getData() {
    tbBankAccount = $('#data').DataTable({
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
            { "data": "bank" },
            { "data": "accountHolder" },
            { "data": "holderId" },
            { "data": "accountNumber" },
            { "data": "id" }
        ],
        columnDefs: [
            {
                targets: [-5],
                render: function (data, type, row) {
                    let bank = '<b>' + data + '</b>';
                    return bank;
                }
            },

            {
                targets: [-2],
                render: function (data, type, row) {
                    let accountNumber = '<span class="badge text-dark badge-info">' + data + '</span>';
                    return accountNumber;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" data-title="Editar cuenta" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" type="button" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ]
    })
}

$(function () {

    modal_title = $('.modal-title')

    getData();

    $('#i_card_title').removeClass().addClass('text-dark fas fa-file-alt')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-university')

    $('.btnAddBankAccount').on('click', function () {
        $('form')[0].reset();
        modal_title.find('span').html('Nueva Cuenta Bancaria');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('input[name="action"]').val('add');
        $('#modalBankAccount').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();
        let tr = tbBankAccount.cell($(this).closest('td, li')).index();
        let data = tbBankAccount.row(tr.row).data();
        modal_title.find('span').html('Editar Datos de la Cuenta');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="bank"]').val(data.bank);
        $('input[name="accountHolder"]').val(data.accountHolder);
        $('input[name="holderId"]').val(data.holderId);
        $('input[name="accountNumber"]').val(data.accountNumber);
        $('#modalBankAccount').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbBankAccount.cell($(this).closest('td, li')).index();
            let data = tbBankAccount.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Cuentas Bancarias Actualizadas');
                setTimeout(tbBankAccount.ajax.reload(),5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalBankAccount').modal('hide');
            alertSweetSuccess('Cuentas Bancarias Actualizadas');
            setTimeout(tbBankAccount.ajax.reload(),5000);
        });
    });
});

