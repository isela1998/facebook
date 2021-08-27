var tbServices;
var modal_title;
var dolar;

function getData() {
    tbServices = $('#data').DataTable({
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
            { "data": "type_service.name" },
            { "data": "description" },
            { "data": "quantity" },
            { "data": "amount_dl" },
            { "data": "amount_bs" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: true,
            },
            {
                targets: [-2,-3],
                class: 'text-center',
                orderable: true,
                render: $.fn.dataTable.render.number('.', ',', 2)
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

    console.log(dolar)

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-funnel-dollar')

    $('#datejoined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });

    getData();

    $('.btnAddServices').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Nuevo Servicio');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('form')[0].reset();
        $('#modalServices').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('span').html('Editar Servicio');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbServices.cell($(this).closest('td, li')).index();
        let data = tbServices.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="datejoined"]').val(data.datejoined);
        $('input[name="quantity"]').val(data.quantity);
        $('select[name="type_service"]').val(data.type_service_id);
        $('textarea[name="description"]').val(data.description);
        $('input[name="amount_bs"]').val(data.amount_bs);
        $('input[name="amount_dl"]').val(data.amount_dl);
        $('#modalServices').modal('show');
    })
        .on('click', 'a[rel="delete"]', function () {
            let tr = tbServices.cell($(this).closest('td, li')).index();
            let data = tbServices.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar este registro?', parameters, function () {
                alertSweetSuccess('Listado de Servicios actualizado');
                setTimeout(tbServices.ajax.reload(), 5000);
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalServices').modal('hide');
            alertSweetSuccess('Listado de Servicios actualizado');
            setTimeout(tbServices.ajax.reload(), 5000);
        });
    });

    $('input[name="amount_bs"]').on('change keyup', function (){
        let amount_bs = $(this).val().replace(/\./g, '');
        let amount_dl = parseFloat(amount_bs) / parseFloat(dolar);
        $('input[name="amount_dl"').val(amount_dl.toFixed(6));
    });

    $('input[name="amount_dl"]').on('change keyup', function (){
        let amount_bs = parseFloat(this.value) * parseFloat(dolar);
        $('input[name="amount_bs"').val(amount_bs);
    });

});

