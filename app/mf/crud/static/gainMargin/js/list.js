var tbGainMargin;
var modal_title;

function getData() {

    $('#i_card_title').removeClass().addClass('text-dark fas fa-boxes')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-th-list')

    tbGainMargin = $('#data').DataTable({
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
            { "data": "code" },
            { "data": "product" },
            { "data": "cost" },
            { "data": "gain" },
            { "data": "price_dl" },
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
                targets: [-5],
                class: 'text-center',
                render: function (data, type, row) {
                    let code = '<span class="badge text-dark fill-available badge-info"><b>' + data + '</b></span>';
                    return code;
                }
            },
            {
                targets: [-4],
                class: 'text-left',
                render: function(data, type, row){
                    let product = row.category.name + '- ' + data + ' (' + row.type_product.name + ') ';
                    return product
                }
            },
            {
                targets: [-1,-2,-3],
                class: 'text-center',
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
        ]
    })
}

$(function (){
    getData();
});