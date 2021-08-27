var classTd;
var dl;
var tbDebts;
var modal_title;

function getData() {
    tbDebts = $('#data').DataTable({
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
            { "data": "type_debts.name" },
            { "data": "start_date" },
            { "data": "end_date" },
            { "data": "client" },
            { "data": "description" },
            { "data": "dollars" },
            { "data": "rate" },
            { "data": "bs" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-9],
                class: 'text-center',
                render: function (data, type, row) {
                    let type_debt = '<span class="' + row.css + '">' + data + '</span>';
                    return type_debt;
                }
            },
            {
                targets: [-2,-3,-4],
                class: 'text-center',
                orderable: true,
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" data-title="Editar Cuenta" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="down" data-title="Registrar Abono" class="btn btn-success btn-smp btn-flat"><i class="fas text-dark fa-arrow-down"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" type="button" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ] 
    })
}

$(function () {

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-file-alt')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-book-reader')

    getData();

    $('#start_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });

    $('#end_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('#pay_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });


    $('.btnAdd').on('click', function () {
        $('form')[0].reset();
        $("#searchClient").empty();
        $('input[name="action"]').val('add');
        modal_title.find('#id_span').html('Nueva Cuenta');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('#modalDebts').modal('show');
    });

    $('.btnAddClient').on('click', function () {
        $('input[name="action"]').val('addClient');
        $('form')[1].reset();
        $('#modalClient').modal('show');
    });

    $('.btnAddProvider').on('click', function () {
        $('input[name="action"]').val('addProvider');
        $('form')[2].reset();
        $('#modalProviders').modal('show');
    });

    $('select[name="searchClient"]').select2({
        theme: "bootstrap4",
        language: 'es',
        // allowClear: True,
        ajax: {
            delay: 150,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_client'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Búsqueda por Nombre/Cédula/RIF',
        minimunInputLength: 1,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        $('input[name="client"]').val(data.type_client);
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('#id_span').html('Editar Cuenta');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbDebts.cell($(this).closest('td, li')).index();
        let data = tbDebts.row(tr.row).data();
        document.getElementById('searchClient').innerHTML = '<option>' + data.client + '</option>';
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('select[name="type_debts"]').val(data.type_debts.id);
        $('input[name="client"]').val(data.client);
        $('input[name="start_date"]').val(data.start_date);
        $('input[name="end_date"]').val(data.end_date);
        $('textarea[name="description"]').val(data.description);
        $('input[name="rate"]').val(data.rate);
        $('input[name="dollars"]').val(data.dollars);
        $('#modalDebts').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbDebts.cell($(this).closest('td, li')).index();
            let data = tbDebts.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Listado de cuentas actualizado');
                setTimeout(tbDebts.ajax.reload(), 5000);
            });
        }).on('click', 'a[rel="down"]', function () {
            let tr = tbDebts.cell($(this).closest('td, li')).index();
            let data = tbDebts.row(tr.row).data();
            $('form')[3].reset();
            $('input[name="debtInput"]').val(data.dollars);
            $('input[name="debtInput"]').addClass('disabled');
            $('input[name="idCredit"]').val(data.id);
            $('input[name="provider"]').val(data.client);
            $('#modalDollarPurchase').modal('show');
        });


    $('.formClient').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalClient').modal('hide');
            alertSweetSuccess('Nuevo cliente registrado con éxito');
            setTimeout(window.location.reload(), 5000);
        });
    });

    $('.formProviders').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalProviders').modal('hide');
            alertSweetSuccess('Nuevo proveedor registrado con éxito');
            setTimeout(window.location.reload(), 5000);
        });
    });

    $('.formCredit').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalDollarPurchase').modal('hide');
            alertSweetSuccess('Abono de cuenta registrado con éxito');
            setTimeout(tbDebts.ajax.reload(), 5000);
        });
    });

    $('.formDebts').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let client = $('input[name="client"]').val();
        let parameters = new FormData(this);
        parameters.append('client', client);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalDebts').modal('hide');
            alertSweetSuccess('Listado de cuentas actualizado');
            setTimeout(tbDebts.ajax.reload(), 5000);
        });
    });
});

