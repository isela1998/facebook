var tableBudgets;

$(function() {

    $('#i_card_title').removeClass().addClass('text-dark fas fa-file-alt')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-clipboard-list')

    tableBudgets = $('#data').DataTable({
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
            { "data": "cli" },
            { "data": "total_dl" },
            { "data": "id" },
        ],
        dom: '<"myCustomClass"f>rt<"bottom"lp><"clear">',
        fnDrawCallback: function() {
            $("input[type='search']").attr("id", "searchBox");
            $("input[type='search']").attr("autocomplete", "off");
            $("select[name='data_length'], #searchBox").removeClass("input-sm");
            $('#searchBox').css("width", "350px").focus();
            $('#data').removeClass('dataTables_filter');
        },
        columnDefs: [
            {
                targets: [-3],
                render: function(data, type, row){
                    let client = '<i>' + data.names + ' (' + data.identity.identity + data.ci + ')' + ' ' + data.contact + '</i>';
                    return client;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: $.fn.dataTable.render.number(',', '.', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a href="/panel/sale/budget/pdf/' + data + '/" target="_blank" class="btn btn-success btn-smp btn-flat"><i class="fas text-dark fa-search"></i></a> ';
                }
            },
        ],
    });
});