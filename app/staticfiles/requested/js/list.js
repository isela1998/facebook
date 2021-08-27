var modal_title;
var tableSale;

function getData() {
    tableSale = $('#data').DataTable({
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
            { "data": "name" },
            { "data": "description" },
            { "data": "description" },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" data-title="Editar" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    })
}

$(function () {
    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-boxes')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-bookmark')

    getData();

    $('.btnAddRequested').on('click', function () {
        $('form')[0].reset();
        modal_title.find('span').html('Registrar Solicitud');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        $('input[name="action"]').val('add');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('#modalRequested').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();
        modal_title.find('span').html('Editar Solicitud');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tableSale.cell($(this).closest('td, li')).index();
        let data = tableSale.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="name"]').val(data.name);
        $('textarea[name="description"]').val(data.description);
        $('#modalRequested').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tableSale.cell($(this).closest('td, li')).index();
            let data = tableSale.row(tr.row).data();
            let parameters = new FormData();

            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Estas seguro de realizar eliminar el siguiente registro?', parameters, function () {
                alertSweetSuccess('Listado de solicitudes actualizado');
                setTimeout(tableSale.ajax.reload(), 5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalRequested').modal('hide');
            alertSweetSuccess('Listado de solicitudes actualizado');
            setTimeout(tableSale.ajax.reload(), 5000);
        });
    });
});