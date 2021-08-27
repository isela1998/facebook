var tbEarnings;
var modal_title;

function getData() {
    tbEarnings = $('#data').DataTable({
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
            { "data": "date" },
            { "data": "concept" },
            { "data": "amount_dl" },
            { "data": "amount_bs" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-2,-3],
                class: 'text-center',
                orderable: false,
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: true,
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
    $('#i_card_title').removeClass().addClass('text-dark fas fa-wallet')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-search-dollar')

    getData();

    $('#date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });

    $('.btnAddEarning').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Nueva Ganancia');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('form')[0].reset();
        $('#modalEarning').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('span').html('Editar Ganancia');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbEarnings.cell($(this).closest('td, li')).index();
        let data = tbEarnings.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="date"]').val(data.date);
        $('textarea[name="concept"]').val(data.concept);
        $('input[name="amount_dl"]').val(data.amount_dl);
        $('#modalEarning').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbEarnings.cell($(this).closest('td, li')).index();
            let data = tbEarnings.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Listado de Ganancias actualizado');
                setTimeout(tbEarnings.ajax.reload(), 5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalEarning').modal('hide');
            alertSweetSuccess('Listado de Ganancias actualizado');
            setTimeout(tbEarnings.ajax.reload(), 5000);
        });
    });
});

