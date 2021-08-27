var tbCompany;
var modal_title;

function getData() {
    tbCompany = $('#data').DataTable({
        ordering: false,
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
            { "data": "rif" },
            { "data": "address" },
            { "data": "postal_zone" },
            { "data": "phone" },
            { "data": "email" },
            { "data": "id" },
        ],
        columnDefs: [{
            targets: [-2, -3, -4],
            class: 'text-center',
        },
        {
            targets: [-1],
            class: 'text-center',
            render: function (type, row) {
                return '<a href="#" rel="edit" data-title="Editar Datos" class="btn btn-warning btn-smp btn-flat"><i class="fas text-dark fa-edit"></i></a> ';
            }
        },
        ]
    })
}

$(function () {

    getData();

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-city')

    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('#i_modal_title').removeClass().addClass('fas text-primary fa-edit');
        let tr = tbCompany.cell($(this).closest('td, li')).index();
        let data = tbCompany.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="rif"]').val(data.rif);
        $('input[name="address"]').val(data.address);
        $('input[name="postal_zone"]').val(data.postal_zone);
        $('input[name="phone"]').val(data.phone);
        $('input[name="email"]').val(data.email);
        $('#modalCompany').modal('show');
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalCompany').modal('hide');
            alertSweetSuccess('Se actualizaron los datos de la empresa');
            setTimeout(tbCompany.ajax.reload(), 5000);
        });
    });
});