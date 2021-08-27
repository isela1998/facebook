var tableSale;

function details_vents(d) {
    let html = '';
    html += '<span><b>Cliente:</b></span><br>'
    html += '<span>' + d.cli.names + ' ' + ' ' + d.cli.identity.identity + d.cli.ci + ' ' + d.cli.contact + '</span><hr>'
    html += '<span><b>Factura|Nº:</b></span><br>'
    html += '<span class="badge badge-info">' + d.invoice_number + '</span><hr>'
    html += '<span><b>PRODUCTOS:</b></span><hr>'
    $.each(d.det, function (key, value) {
        html += '<span> -' + value.prod.product + ' (' + value.prod.type_product.name + ')</span><br>'
        html += '<span>Cantidad: ' + value.quantity + '</span><br>'
        html += '<span>Precio: ' + value.price.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '</span><br>'
        html += '<span>Subtotal : ' + value.subtotal.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '</span><hr>'
    });
    html += '<span><b>Subtotal:</b></span><br>'
    html += '<span>' + d.subtotal.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '</span><br>'
    html += '<span><b>IVA:</b></span><br>'
    html += '<span>' + d.iva.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '</span><br>'
    html += '<span><b>Descuento:</b></span><br>'
    html += '<span>Cantidad: ' + d.discount + '<br>'
    html += '<span>Descripción: ' + d.desc_discount + '</span><br>'
    html += '<span><b>Total (Bs.):</b></span><br>'
    html += '<span>' + d.total.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '</span><br>'
    html += '<span><b>Total ($.):</b></span><br>'
    html += '<span>' + d.total_dl.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '$</span><hr>'
    html += '<span><b>Método de Pago Nº 1:</b></span><br>'
    html += '<span>' + d.method_pay.name + '</span><br>'
    html += '<span>Entrada: </span>'
    html += '<span>' + d.received.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.method_pay.type_symbol + '</span><br>'
    html += '<span>Cambio: </span>'
    html += '<span>' + d.exchange.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.method_pay.type_symbol + '</span><hr>'
    html += '<span><b>Método de Pago Nº 2:</b></span><br>'
    html += '<span>' + d.method_pay1.name + '</span><br>'
    html += '<span>Entrada: </span>'
    html += '<span>' + d.received1.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.method_pay1.type_symbol + '</span><br>'
    html += '<span>Cambio: </span>'
    html += '<span>' + d.exchange1.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.method_pay1.type_symbol + '</span><hr>'
    html += '<span><b>Método de Pago Nº 3:</b></span><br>'
    html += '<span>' + d.method_pay2.name + '</span><br>'
    html += '<span>Entrada: </span>'
    html += '<span>' + d.received2.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.method_pay2.type_symbol + '</span><br>'
    html += '<span>Cambio: </span>'
    html += '<span>' + d.exchange2.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.method_pay2.type_symbol + '</span><hr>'
    html += '<span><b>Notas y/o Descripción:</b></span><br>'
    html += '<span>' + d.description + '</span>'


    document.getElementById('detailsVent').innerHTML = html;
    $('#modalDetails').show();
}

$(function () {

    $('#i_card_title').removeClass().addClass('text-dark fas fa-city')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-shopping-cart')

    $('#datejoined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('#date_end').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

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
        columns: [
            { "data": "datejoined" },
            { "data": "invoice_number" },
            { "data": "cli" },
            { "data": "type_sale" },
            { "data": "total" },
            { "data": "total_dl" },
            { "data": "method_pay.name" },
            { "data": "id" },
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
                targets: [-7],
                orderable: true,
                render: function (data, type, row) {
                    let invoice_number = '<span class="pointer-1" data-title="' + row.statusName + '">00'+ data + '</span>'
                    return invoice_number;
                }
            },
            {
                targets: [-6],
                orderable: true,
                render: function (data, type, row) {
                    let client = '<i>' + data.names + ' (' + data.identity.identity + data.ci + ')' + ' ' + data.contact + '</i>';
                    return client;
                }
            },
            {
                targets: [-3, -4],
                class: 'text-center',
                orderable: false,
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a data-title="Detalles" rel="details" class="btn btn-success btn-smp btn-flat"><i class="fas text-dark fa-search"></i></a> ';
                    buttons += '<a data-title="Duplicar" href="/panel/sale/add/' + row.id + '/" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-clone"></i></a> ';
                    buttons += '<a data-title="Factura" href="/panel/sale/invoice/pdf/' + data + '/" target="_blank" class="btn btn-primary btn-smp btn-flat"><i class="fas text-dark fa-file-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});

$(function () {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        let tr = tableSale.cell($(this).closest('td, li')).index();
        let data = tableSale.row(tr.row).data();
        details_vents(data);
        $('#modalDetails').modal('show');
    });
});




