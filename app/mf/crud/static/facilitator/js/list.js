var tbFacilittor;
var modal_title;

function getData() {
    tbFacilittor = $('#data').DataTable({
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
            { "data": "names" },
            { "data": "contact" },
            { "data": "contact" },
        ],
        columnDefs: [
            {
                targets: [-3],
                orderable: true,
                render: function(data, type, row){
                    let client = data + ' ' + row.identity.identity + '-' + row.ci;
                    return client
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
        ],
        initComplete: function (settings, json) {

        }
    })
}

$(function () {

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-user-friends')

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Nuevo facilitador');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        $('form')[0].reset();
        $('#modalFacilitator').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('span').html('Editar datos del facilitador');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbFacilittor.cell($(this).closest('td, li')).index();
        let data = tbFacilittor.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="names"]').val(data.names);
        $('input[name="ci"]').val(data.ci);
        $('input[name="contact"]').val(data.contact);
        $('#modalFacilitator').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbFacilittor.cell($(this).closest('td, li')).index();
            let data = tbFacilittor.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Listado de facilitadores actualizado');
                setTimeout(tbFacilittor.ajax.reload(), 5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalFacilitator').modal('hide');
            alertSweetSuccess('Listado de facilitadores actualizado');
            setTimeout(tbFacilittor.ajax.reload(), 5000);
        });
    });
});

