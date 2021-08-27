var tbInvoices;
var modal_title;

function getData() {
    tbInvoices = $('#data').DataTable({
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
            { "data": "provider" },
            { "data": "facilitator" },
            { "data": "total" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    let provider = data.names + ' (' + data.ci + ') ';
                    return provider;
                }
            },
            {
                targets: [-3],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    let facilitator = data.names + ' (' + data.ci + ') ';
                    return facilitator;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: true,
                render: $.fn.dataTable.render.number('.', ',', 2)
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/panel/invoices/report/pdf/' + data + '/" target="_blank" data-title="Nota" class="btn btn-primary btn-smp btn-flat"><i class="fas text-dark fa-file-alt"></i></a> ';
                    buttons += '<a href="#" rel="delete" data-title="Eliminar" type="button" class="btn btn-danger btn-smp btn-flat"><i class="fas text-dark fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ]
    })
}

$(function () {

    modal_title = $('.modal-title')
    $('#i_card_title').removeClass().addClass('text-dark fas fa-file-invoice-dollar')
    $('#i_card_title2').removeClass().addClass('text-dark fas fa-dollar-sign')

    getData();

    $('#datejoined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });

    $('.btnAddInvoice').on('click', function () {
        $('form')[0].reset();
        $('#modalInvoices').modal('show');
    });

    $('.btnAddProvider').on('click', function () {
        $('form')[1].reset();
        $('#modalProviders').modal('show');
    });

    $('.btnAddFacilitator').on('click', function () {
        $('form')[2].reset();
        $('#modalFacilitator').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="delete"]', function () {
            let tr = tbInvoices.cell($(this).closest('td, li')).index();
            let data = tbInvoices.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax_msj(window.location.pathname, 'Notificación', '¿Está seguro de eliminar el siguiente registro?', parameters, function () {
                alertSweetSuccess('Listado de Facturas actualizado');
                setTimeout(tbInvoices.ajax.reload(), 5000);
            });
        });

    $('.formProviders').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalProviders').modal('hide');
            alertSweetSuccess('Nuevo Proveedor registrado con éxito');
            setTimeout(window.location.reload(), 5000);
        });
    });

    $('.formFacilitator').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalFacilitator').modal('hide');
            alertSweetSuccess('Nuevo Facilitador registrado con éxito');
            setTimeout(window.location.reload(), 5000);
        });
    });

    $('.formInvoices').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        getArrayProducts();
        let totalInvoice = $('input[name="totalInvoice"]').val();
        let parameters = new FormData(this)
        parameters.append('totalInvoice', totalInvoice);
        parameters.append('dict', JSON.stringify(dict.items));
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalInvoices').modal('hide');
            alertSweetSuccess('Factura registrada con éxito');
            setTimeout(tbInvoices.ajax.reload(), 5000);
        });
    });
});

function buttons_group() {
    let td_group = ''
    let number = $('input[name="buttons"]').val()
    let total_buttons = parseInt(number) + 1;
    let group = 'new-group' + number;
    td_group += '<td class="pd-40" scope="col"><input class="form-control text-center UpperCase selectThis" name="code" type="text" autocomplete="off" placeholder="Código" required></td>'
    td_group += '<td scope="col" class="pd-40 selectCategory"></td>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control UpperCase text-center selectThis inputProduct" name="product" type="text" placeholder="Producto" autocomplete="off" required></td>'
    td_group += '<td scope="col" class="pd-40 selectTypes"></td>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control text-center inputNumber selectThis" value="0.00" name="total" type="text" autocomplete="off" placeholder="Total" required></td>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control inputNumber text-center selectThis" type="text" autocomplete="off" name="quantity" value="1" placeholder="Cant" required></td>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control inputNumber text-center selectThis" value="0.00" name="unit_price" type="text" autocomplete="off" placeholder="P.U." required></td>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control inputNumber text-center selectThis" type="text" autocomplete="off" name="shipment" placeholder="%" required readonly>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control inputNumber text-center selectThis" type="text" autocomplete="off"  name="gain" placeholder="%" required></td>'
    td_group += '<td class="pd-40" scope="col"><input class="form-control inputNumber text-center selectThis" type="text" autocomplete="off" name="final_price" placeholder="%" required></td>'
    td_group += '<td class="pd-40" scope="col"><h2> <a href="#" class="mx-auto p-2" id="new-group' + number + '" onclick="removeGroup(this.id)"><i class="fas text-dark fa-trash-alt" required></i></a><h2>'
    td_group += '</td>'
    
    document.getElementById(group).innerHTML = td_group;
    document.getElementById(group).insertAdjacentHTML('afterend', '<tr id="new-group' + total_buttons + '" class="group-buttons"></tr>');
    $('input[name="buttons"]').val(total_buttons);
}

function removeGroup(group) {
    document.getElementById(group).remove();
    refresh();
}

$(function () {
    for (let step = 0; step < 4; step++) {
        buttons_group();
    }

    get_selects();
    refresh();

    $('#add-group-buttons').on('click', function () {
        buttons_group();
        get_selects();
        refresh();
    });

    $('#add-categories').on('click', function () {
        newCategory();
    });

    $('#add-product-types').on('click', function () {
        newProductType();
    });
});

function newCategory() {
    fixBootstrapModal();
    
    (async () => {

        const { value: category } = await Swal.fire({
          title: 'Nueva Categoría',
          input: 'text',
          inputPlaceholder: 'Indique el nombre de la categoría',
          showCancelButton: true,
          confirmButtonText: 'Registrar',
          cancelButtonText: "Cancelar",
          onClose: () => {
            restoreBootstrapModal();
          }
        })
        
        if (category) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'add-category',
                    'name': category.toUpperCase(),
                },
                dataType: 'json',
            }).done(function (data) {
                get_selects();
                alertSuccess('Categoría Registrada');
            });
        }
        })()

}

function newProductType() {
    fixBootstrapModal();
    (async () => {
        const { value: productType } = await Swal.fire({
          title: 'Nuevo tipo de producto',
          input: 'text',
          inputPlaceholder: 'Indique el tipo de producto',
          showCancelButton: true,
          confirmButtonText: 'Registrar',
          cancelButtonText: "Cancelar",
          onClose: () => {
            restoreBootstrapModal();
          }
        })
        
        if (productType) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'add-product-type',
                    'name': productType.toUpperCase(),
                },
                dataType: 'json',
            }).done(function (data) {
                get_selects();
                alertSuccess('Tipo de producto registrado');
            });
        }
        })()

}

function fixBootstrapModal() {
    var modalNode = document.querySelector('#modalInvoices[tabindex="-1"]');
    if (!modalNode) return;
  
    modalNode.removeAttribute('tabindex');
    modalNode.classList.add('js-swal-fixed');
}

function restoreBootstrapModal() {
    var modalNode = document.querySelector('.modal.js-swal-fixed');
    if (!modalNode) return;
  
    modalNode.setAttribute('tabindex', '-1');
    modalNode.classList.remove('js-swal-fixed');
  }



function refresh(){
    let total = 0
    $('input[name="total"]').each(function () {
        total = total + parseFloat(this.value)
    });

    $('input[name="totalInvoice"]').val(total);

    $('.selectThis').on('click', function () {
        $(this).select();
    });

    $('input[name="quantity"]').on('change keyup', function(){
        let total = parseFloat($(this).closest('tr').find('input[name="total"]').val());
        let unit_price = total / this.value;
        $(this).closest('tr').find('input[name="unit_price"]').val(unit_price.toFixed(2));
        getTotals();
    });
    $('input[name="total"]').on('change keyup', function(){
        let quantity = parseFloat($(this).closest('tr').find('input[name="quantity"]').val());
        let unit_price = parseFloat(this.value) / quantity;
        $(this).closest('tr').find('input[name="unit_price"]').val(unit_price.toFixed(2));
        getTotals();
    });
    $('input[name="unit_price"]').on('change keyup', function(){
        let quantity = parseFloat($(this).closest('tr').find('input[name="quantity"]').val());
        let total = parseFloat(this.value) * quantity;
        $(this).closest('tr').find('input[name="total"]').val(total.toFixed(2));
        getTotals();
    });
    $('input[name="unit_price"]').on('change keyup', function(){
        let quantity = parseFloat($(this).closest('tr').find('input[name="quantity"]').val());
        let total = parseFloat(this.value) * quantity;
        $(this).closest('tr').find('input[name="total"]').val(total.toFixed(2));
        getTotals();
    });
    $('input[name="gain"]').on('change keyup', function(){
        let unit_price = parseFloat($(this).closest('tr').find('input[name="unit_price"]').val());
        let shipment = parseFloat($(this).closest('tr').find('input[name="shipment"]').val());
        let final_price = parseFloat(this.value) + unit_price + shipment;

        $(this).closest('tr').find('input[name="final_price"]').val(final_price.toFixed(2));
    });
    $('input[name="final_price"]').on('change keyup', function(){
        let unit_price = parseFloat($(this).closest('tr').find('input[name="unit_price"]').val());
        let shipment = parseFloat($(this).closest('tr').find('input[name="shipment"]').val());
        let gain = parseFloat(this.value) - unit_price - shipment;

        $(this).closest('tr').find('input[name="gain"]').val(gain.toFixed(2));
    });
    $('input[name="aditionalExpenses"]').on('change keyup', function(){
        calculatePrices();
        getTotals();
    });
}

function get_selects() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'get_selects'
        },
        dataType: 'json',
    }).done(function (data) {
        let selectCategory = '<select name="selectCategory" class="form-control">'
        $.each(data[0].categories, function (post, value) {
            selectCategory += '<option value="' + value.id + '">' + value.name + '</option>'
        });
        selectCategory += '</select>'

        let selectTypes = '<select name="selectTypes" class="form-control">'
        $.each(data[0].types, function (post, value) {
            selectTypes += '<option value="' + value.id + '">' + value.name + '</option>'
        });
        selectTypes += '</select>'

        $('.selectCategory').each(function () {
            let value = $(this).closest('tr').find('select[name="selectCategory"]').val()
            if (value === null || value === undefined) {
                value = 1
            }
            console.log('Category is', value)
            this.innerHTML = selectCategory;
            $(this).closest('tr').find('select[name="selectCategory"]').val(value)
        });

        $('.selectTypes').each(function () {
            let value = $(this).closest('tr').find('select[name="selectTypes"]').val()
            if (value === null || value === undefined) {
                value = 1
            }
            console.log('Category is', value)
            this.innerHTML = selectTypes;
            $(this).closest('tr').find('select[name="selectTypes"]').val(value)
        });
    });
}

function getTotals(){
    let total = 0
    $('input[name="total"]').each(function () {
        total = total + parseFloat(this.value)
    });
    $('input[name="totalInvoice"]').val(total.toFixed(2));
}

function getGlobalTotal(){
    let expenses = $('input[name="aditionalExpenses"]').val();
    $('input[name="total"]').each(function () {
        total = total + parseFloat(this.value)
    });
    $('input[name="totalInvoice"]').val(total + parseFloat(expenses));  
}

function calculatePrices() {
    let aditional = 0
    let totalInvoice = parseFloat($('input[name="totalInvoice"]').val());
    console.log(totalInvoice)
    let expenses = parseFloat($('input[name="aditionalExpenses"]').val());
    console.log(expenses)
    if(expenses <= 10){
        aditional = '0.0'
    }else{
        aditional = '0.'
    }
    let percent = parseFloat(aditional + (((expenses + 0.5) * 100) / totalInvoice).toString());
    console.log(percent)

    $('input[name="shipment"]').each(function () {
        let total = parseFloat($(this).closest('tr').find('input[name="total"]').val());
        let quantity = parseFloat($(this).closest('tr').find('input[name="quantity"]').val());
        let resul = ((total * percent) / quantity);
        this.value = resul.toFixed(2);
    });

    $('input[name="gain"]').each(function () {
        let unit_price = parseFloat($(this).closest('tr').find('input[name="unit_price"]').val());
        let shipment = parseFloat($(this).closest('tr').find('input[name="shipment"]').val());
        let resul = ((unit_price + shipment) * 0.35)
        this.value = resul.toFixed(2);
        let final_price = (unit_price + shipment) * 1.35
        $(this).closest('tr').find('input[name="final_price"]').val(final_price.toFixed(2));
    });
}

var dict = {
    items: {
        products: []
    },
    add: function (item) {
        this.items.products.push(item);
    }
}

function getArrayProducts(){
    dict.items.products = [];
    $('input[name="code"]').each(function () {
        product = {
            'code': this.value,
            'category': $(this).closest('tr').find('select[name="selectCategory"]').val(),
            'product': $(this).closest('tr').find('input[name="product"]').val(),
            'type_product': $(this).closest('tr').find('select[name="selectTypes"]').val(),
            'total': parseFloat($(this).closest('tr').find('input[name="total"]').val()),
            'quantity': parseFloat($(this).closest('tr').find('input[name="quantity"]').val()),
            'unit_price': parseFloat($(this).closest('tr').find('input[name="unit_price"]').val()),
            'shipment': parseFloat($(this).closest('tr').find('input[name="shipment"]').val()),
            'gain': parseFloat($(this).closest('tr').find('input[name="gain"]').val()),
            'final_price': parseFloat($(this).closest('tr').find('input[name="final_price"]').val()),
        }
        dict.add(product);
    });
}
