var tbProduct;
var modal_title;

function getData() {

    $('#i_card_title').removeClass().addClass('text-dark fas fa-boxes')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-th-list')

    tbProduct = $('#data').DataTable({
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
        columns: [
            // { "data": "id" },
            { "data": "code" },
            { "data": "category.name" },
            { "data": "type_product.name" },
            { "data": "product" },
            { "data": "quantity" },
            { "data": "price_dl" },
            { "data": "price_bs" },
            { "data": "price_bs" },
        ],
        dom: '<"myCustomClass"f>rt<"bottom"lp><"clear">',
        fnDrawCallback: function () {
            $("input[type='search']").attr("id", "searchBox");
            $("input[type='search']").attr("autocomplete", "off");
            $("select[name='data_length'], #searchBox").removeClass("input-sm");
            $('#searchBox').css("width", "350px").focus();
            $('#data').removeClass('dataTables_filter');
        },
        columnDefs: [
            {
                targets: [-8],
                orderable: false,
                render: function (data, type, row) {
                    let code = '<span class="badge text-dark fill-available badge-info"><b>' + data + '</b></span>';
                    return code;
                }
            },
            {
                targets: [-5],
                orderable: true,
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let quantity = '<span class="' + row.css + '">' + data + '</span>';
                    return quantity;
                }
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
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="view_product" data-title="Ver producto" type="button" class="btn btn-success btn-smp btn-flat"><i class="fas text-dark fa-search"></i></a> ';
                    buttons += '<a href="#" rel="edit" data-title="Editar datos" type="button" class="btn btn-info btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="up" data-title="A Stock2" type="button" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-arrow-up"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" type="button" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a> ';
                    return buttons;
                }
            },
        ]
    })
}

$(function () {
    let btn = '<a href="/panel/inventary/report/pdf/2/" target="_blank" class="btn btn-primary btn-flat"><i class="fas fa-arrow-circle-down"></i> <i class="fas fa-file-pdf"></i> Descargar Reporte</a>'
    document.getElementById('btn-report').innerHTML = btn;

    modal_title = $('.modal-title')
    getData();

    $('.btnAdd').on('click', function () {
        $('form')[0].reset();
        modal_title.find('#span_modal_title').html('Agregar Producto');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-plus');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-save"></i> Guardar'
        $('input[name="action"]').val('add');
        $('#modalProduct').modal('show');
    });

    $('.btnAddCategory').on('click', function () {
        $('form')[1].reset();
        $('input[name="action"]').val('addCategory');
        $('#modalCategory').modal('show');
    });

    $('.btnAddType').on('click', function () {
        $('form')[2].reset();
        $('input[name="action"]').val('addType');
        $('#modalType').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="edit"]', function () { 
        $('form')[0].reset();
        modal_title.find('#span_modal_title').html('Editar Producto');
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        document.getElementById('btn_submit').innerHTML = '<i class="fas fa-sync"></i> Actualizar'
        let tr = tbProduct.cell($(this).closest('td, li')).index();
        let data = tbProduct.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="code"]').val(data.code);
        $('select[name="category"]').val(data.category.id);
        $('select[name="type_product"]').val(data.type_product.id);
        $('input[name="product"]').val(data.product);
        $('input[name="brand"]').val(data.brand);
        $('input[name="quantity"]').val(data.quantity);
        $('input[name="price_dl"]').val(data.price_dl);
        $('input[name="price_bs"]').val(data.price_bs);
        $('input[name="cost"]').val(data.cost);
        $('#modalProduct').modal('show');
    })
        .on('click', 'a[rel="view_product"]', function () {
            let tr = tbProduct.cell($(this).closest('td, li')).index();
            let data = tbProduct.row(tr.row).data();
            let image = '<img src="../../../media/'+data.image+'" alt="Producto" class="img-fluid"></img>'
            document.getElementById('modal-view-product').innerHTML = image
            $('#modalViewProduct').modal('show');
        }).on('click', 'a[rel="up"]', function () {
            let tr = tbProduct.cell($(this).closest('td, li')).index();
            let data = tbProduct.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'up-stock');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de subir a Stock 1?', parameters, function () {
                alertSweetSuccess('Realizado con éxito');
                setTimeout(tbProduct.ajax.reload(), 4000);
            });
        }).on('click', 'a[rel="delete"]', function () {
            let tr = tbProduct.cell($(this).closest('td, li')).index();
            let data = tbProduct.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Estas seguro de realizar eliminar el siguiente registro?', parameters, function () {
                alertSweetSuccess('Listado de Productos actualizado');
                setTimeout(tbProduct.ajax.reload(), 5000);
            });
        });

    $('.formProduct').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalProduct').modal('hide');
            alertSweetSuccess('Listado de Productos actualizado');
            setTimeout(tbProduct.ajax.reload(), 5000);
        });
    });

    $('.formCategory').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalCategory').modal('hide');
            alertSweetSuccess('Nueva categoría registrada');
            setTimeout(window.location.reload(), 5000);
        });
    });

    $('.formType').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalType').modal('hide');
            alertSweetSuccess('Nuevo tipo de producto registrado');
            setTimeout(window.location.reload(), 5000);
        });
    });
});



