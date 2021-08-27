function getData() {

    $('#i_card_title').removeClass().addClass('text-dark fas fa-boxes')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-arrow-alt-circle-down')

    $('#data').DataTable({
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
        fnDrawCallback:function(){
            $("input[type='search']").attr("id", "searchBox");
            $("input[type='search']").attr("autocomplete", "off");
            $("select[name='data_length'], #searchBox").removeClass("input-sm");
            $('#searchBox').css("width", "350px").focus();
            $('#data').removeClass('dataTables_filter');
        },
        columns: [
            { "data": "category.name" },
            { "data": "product" },
            { "data": "type_product.name" },
            { "data": "quantity" },
        ],
        columnDefs: [
            {
                targets: [-2,-3,-4],
                class: 'text-center, table-secondary',
                orderable: false,
            },
            {
                targets: [-1],
                class: 'text-center, bg-red',
                orderable: false,
            },
        ],
        initComplete: function (settings, json) {

        }
    })
}

$(function () {
    getData();
});

