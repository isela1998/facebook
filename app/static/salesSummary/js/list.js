var tableTypeSales;
var tablePayMethod;
var tableDiscount;
var tableDetails;
var tableSalesReturn;
var tableGainsDetails;
var day;

function format(d) {
    html = '<table class="table" id="format_table" class="display nowrap" style="width: 100%;">'
    html += '<thead><tr class="text-left">'
    html += '<th class="th_details" scope="col" style="width: 30%;">Producto</th>'
    html += '<th class="th_details" scope="col" style="width: 5%;">Cantidad</th>'
    html += '<th class="th_details text-center" scope="col" style="width: 15%;">Precio($)</th>'
    html += '<th class="th_details text-center" scope="col" style="width: 15%;">Precio(Bs)</th>'
    html += '<th class="th_details text-center" scope="col" style="width: 15%;">Subtotal($)</th>'
    html += '<th class="th_details text-center" scope="col" style="width: 20%;">Subtotal(Bs)</th>'
    html += '</tr></thead>'
    html += '<tbody>'
    $.each(d.det, function (key, value) {
        let sub_dl = (parseFloat(value.quantity) * parseFloat(value.prod.price_dl)).toFixed(2);
        html += '<tr>'
        html += '<td class="td_details">' + value.prod.product + ' (' + value.prod.type_product.name + ') ' + '</td>'
        html += '<td class="td_details text-center">' + value.quantity + '</td>'
        html += '<td class="td_details text-center">' + value.prod.price_dl.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '$. </td>'
        html += '<td class="td_details text-center">' + value.prod.price_bs.replace(/\d(?=(\d{3})+\.)/g, '$&,') + 'Bs. </td>'
        html += '<td class="td_details text-center">' + sub_dl.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '$. </td>'
        html += '<td class="td_details text-center">' + value.sub.replace(/\d(?=(\d{3})+\.)/g, '$&,') + 'Bs. </td>'
        html += '</tr>'
    });
    html += '</tbody>'
    html += '</table>'
    html += '<div class="d_details" style="margin: 15px!important;">'
    html += '<span class="span_details"><b>Venta Nº: ' + d.invoice_number + '</b></span>'
    html += '<span class="span_details">Descuento: ' + d.discount.replace(/\d(?=(\d{3})+\.)/g, '$&,') + '</span>'
    html += '<span class="span_details">Descripción del Descuento: ' + d.desc_discount + '</span>'
    html += '<span class="span_details">Método Nº 1 | Entrada: ' + d.received.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.abrev_method + '</span>'
    html += '<span class="span_details">Método Nº 1 | Cambio: ' + d.exchange.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.abrev_method + '</span>'
    html += '<span class="span_details">Método Nº 2 | Entrada: ' + d.received1.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.abrev_method1 + '</span>'
    html += '<span class="span_details">Método Nº 2 | Cambio: ' + d.exchange1.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.abrev_method1 + '</span>'
    html += '<span class="span_details">Método Nº 3 | Entrada: ' + d.received2.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.abrev_method2 + '</span>'
    html += '<span class="span_details">Método Nº 3 | Cambio: ' + d.exchange2.replace(/\d(?=(\d{3})+\.)/g, '$&,') + d.abrev_method2 + '</span>'
    html += '<span class="span_details">Notas y/o Descripción: ' + d.description + '</span>'
    html += '</div>'
    return html
}

function getGainTotals(){
    getDay();
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'day': day,
            'action': 'search_totals'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            let d = data[0]
            document.getElementById('tdQuantity').innerHTML = d.quantity;
            document.getElementById('tdTotalDl').innerHTML = d.totalDl;            
            document.getElementById('tdTotalGains').innerHTML = d.totalGains;            
        } else {
            message_error(data.error);
        }
    });
}

function getGainsDetails() {
    getDay();
    tableGainsDetails = $('#data6').DataTable({
        ordering: true,
        searching: false,
        paging: false,
        info: false,
        pagingType: 'simple_numbers',
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'searchdata6';
                d.day = day;
            },
            dataSrc: ""
        },
        columns: [
            { "data": "product" },
            { "data": "quantity" },
            { "data": "total" },
            { "data": "gain" },

        ],
        columnDefs: [
        {
            targets: [-4],
            class: 'tdLarger',
            orderable: true,
        },    
        {
            targets: [-3],
            class: 'text-center tdLarger',
            orderable: true,
        },
        {
            targets: [-1,-2],
            class: 'text-center tdLarger',
            orderable: true,
            render: $.fn.dataTable.render.number(',', '.', 2)
        },
        ]
    });
}

function details_vents(search, params) {
    getDay();
    tableDetails = $('#details').DataTable({
        info: false,
        ordering: true,
        pagingType: 'simple_numbers',
        responsive: false,
        scrollX: true,
        autoWidth: true,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'search_details';
                d.search = search;
                d.params = params;
                d.day = day;
            },
            dataSrc: ""
        },
        columns: [{
            "className": 'details-control',
            "orderable": false,
            "data": null,
            "defaultContent": '',
        },
        { "data": "date" },
        { "data": "client" },
        { "data": "total" },
        { "data": "total_dl" },
        { "data": "method" },
        { "data": "method1" },
        { "data": "method2" }
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
                class: 'text-left tdLarger capitalize',
            },
            {
                targets: [-6, -7],
                class: 'text-center tdLarger capitalize',
                orderable: false,
            },
            {
                targets: [-4, -5],
                class: 'text-center tdLarger capitalize',
                orderable: false,
                render: $.fn.dataTable.render.number(',', '.', 2)
            },
            {
                targets: [-1, -2, -3],
                class: 'text-center tdLarger capitalize',
                orderable: true,
            },
        ],
        initComplete: function (settings, json) {
            $(window).resize();
            $(window).trigger('resize');
        }
    });

    // Add event listener for opening and closing details
    $('#details tbody').on('click', 'td.details-control', function () {

        var tr = $(this).closest('tr');
        var row = tableDetails.row(tr);

        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
            td.removeClass('s');
        } else {
            row.child(format(row.data())).show();
            tr.addClass('shown');
            td.addClass('s');
        }
    });

    $('#modalDetails').modal('show');
}

function getDay() {
    day = $('#btn-date').val();
    if (day == null) {
        day = 'null';
    }
}

function getTypeSales() {
    getDay();
    tableTypeSales = $('#data').DataTable({
        ordering: true,
        searching: false,
        paging: false,
        info: false,
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'searchdata';
                d.day = day;
            },
            dataSrc: ""
        },
        columns: [
            { "data": "type_sale" },
            { "data": "quantity" },
            { "data": "quantity" },
        ],
        columnDefs: [
        {
            targets: [-3],
            class: 'tdLarger',
        },
        {
            targets: [-2],
            class: 'text-center tdLarger',
        },
        {
            targets: [-1],
            class: 'text-center tdLarger',
            orderable: false,
            render: function (data, type, row) {
                return '<a rel="details" class="btn medium btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
            }
        },
        ],
    });
}

function getPayMethod() {
    getDay();
    tablePayMethod = $('#data2').DataTable({
        ordering: true,
        searching: false,
        paging: false,
        info: false,
        pagingType: 'simple_numbers',
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'searchdata2';
                d.day = day;
            },
            dataSrc: ""
        },
        columns: [
            { "data": "method" },
            { "data": "quantity" },
            { "data": "total" },
            { "data": "total" },

        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'tdLarger',
                render: function (data, type, row) {
                    return data + ' (' + row.type_total + ')';
                }
            },
            {
                targets: [-3],
                class: 'text-center tdLarger',
            },
            {
                targets: [-2],
                class: 'text-center tdLarger',
                orderable: false,
                // render: $.fn.dataTable.render.number(',', '.', 2)
                render: function (data, type, row) {
                    return data.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,') + ' ' + row.type_total;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a rel="details" class="btn btn-success medium btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

function getDiscount() {
    getDay();
    tableDiscount = $('#data3').DataTable({
        ordering: true,
        searching: false,
        paging: false,
        info: false,
        pagingType: 'simple_numbers',
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'searchdata3';
                d.day = day;
            },
            dataSrc: ""
        },
        columns: [
            { "data": "name" },
            { "data": "quantity" },
            { "data": "quantity" },

        ],
        columnDefs: [{
            targets: [-2, -3],
            class: 'text-center tdLarger',
            orderable: false,
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                return '<a rel="details" class="btn btn-success medium btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
            }
        },
        ],
        initComplete: function (settings, json) {

        }
    });
}

function clearTables() {
    tableTypeSales.clear();
    tableTypeSales.clear();
    tablePayMethod.clear();
    tableDiscount.clear();
    tableGainsDetails.clear();
}

function InitTables() {
    getTypeSales();
    getPayMethod();
    getDiscount();
    getGainsDetails();
    getGainTotals();
}

$(function () {
    getTypeSales();
    getPayMethod();
    getDiscount();
    getGainsDetails();
    getGainTotals();
});

$(function () {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        var tr = tableTypeSales.cell($(this).closest('td, li')).index();
        var data = tableTypeSales.row(tr.row).data();

        details_vents('TypeSales', data.type_sale);
    });
    $('#data2 tbody').on('click', 'a[rel="details"]', function () {
        var tr = tablePayMethod.cell($(this).closest('td, li')).index();
        var data = tablePayMethod.row(tr.row).data();

        details_vents('PayMethod', data.id);
    });
    $('#data3 tbody').on('click', 'a[rel="details"]', function () {
        var tr = tableDiscount.cell($(this).closest('td, li')).index();
        var data = tableDiscount.row(tr.row).data();

        details_vents('SDiscount', data.quantity);
    });

    $("#modalDetails").on("hidden.bs.modal", function () {
    });
});

$(function () {
    $('#btn-date').on('change', function () {
        clearTables();
        InitTables();
    });
});