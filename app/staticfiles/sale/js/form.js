var tableProducts;

// Process for calculating invoice totals
var sales = {
    items: {
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        discount: 0.00,
        dolars: 0.00,
        dolar1: 0.00,
        products: []
    },
    calculate_invoice: function () {
        let subtotal = 0.00;
        let iva = 0.16;
        let iva2 = 1.16;
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.quantity * parseFloat(dict.price);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal * iva2;

        this.items.total = this.items.total - this.items.discount;
        this.items.dolars = this.items.total / parseFloat(this.items.dolar1);

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
        $('input[name="calculated_iva"]').val(this.items.iva.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
        $('input[name="total"]').val(this.items.total.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
        $('input[name="quantity_dolars"]').val(this.items.dolars.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tableProducts = $('#tableProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                { "data": "code" },
                { "data": "product" },
                { "data": "price" },
                { "data": "quantity" },
                { "data": "subtotal" },
            ],
            searching: false,
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center tdLarger',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-left tdLarger',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        let product = row.category.name + ' ' + row.product + ' ' + '(' + row.type_product.name + ')';
                        return product;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center tdLarger',
                    orderable: false,
                    render: $.fn.dataTable.render.number(',', '.', 2)
                },
                {
                    targets: [-2],
                    class: 'text-center tdLarger',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="quantity" style="width: 30px;" class="form-control form-control-sm input-sm text-center" autocomplete="off" value="' + row.quantity + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-right tdLarger',
                    orderable: false,
                    render: $.fn.dataTable.render.number(',', '.', 2)
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="quantity"]').TouchSpin({
                    min: 1,
                    max: data.qinitial,
                    step: 1
                });
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

// Auxiliary functions
function calculateDiscount() {
    if (document.getElementById("check").checked == true) {
        document.getElementById("box").style.display = "block";
        $('input[name="desc_discount"]').val('');
        sales.items.discount = 0;
        sales.calculate_invoice();
    } else {
        document.getElementById("box").style.display = "none";
        $(function () {
            $('input[name="discount"]').val(0);
            $('input[name="desc_discount"]').val('No aplica');
            sales.items.discount = 0;
            sales.calculate_invoice();
        });
    }
}

function optionsTypeSale() {
    if (document.getElementById("cash_payment").checked == true) {
        cash_payment();
        $('#description').val('Sin observaciones...').attr('placeholder', 'Agregue un comentario o nota de la venta...');

    } else if (document.getElementById("credit_payment").checked == true) {
        credit_payment();
        $('#description').val('Sin observaciones...').attr('placeholder', 'Indique detalles del crédito ó presupuesto...');
    }
}

function cash_payment() {
    $('select[name="method_pay"]').val(2);
    document.querySelectorAll("#box1,#box2,#box4, #box5, #box6, #box7, #box8").
        forEach(function (box) {
            box.style.display = 'block';
        });
}

function credit_payment() {
    $('select[name="method_pay"]').val(1);
    $('select[name="method_pay_1"]').val(1);
    $('select[name="method_pay_2"]').val(1);
    document.querySelectorAll("#box1,#box2, #box7, #box8").
        forEach(function (box) {
            box.style.display = 'none';
        });
    document.querySelectorAll("#box4, #box5, #box6").forEach(function (box) {
        box.style.display = 'block';
    });
}

// Default values
$(function () {

    document.getElementById('searchClient').style.fontSize = "large";

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#datejoined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });
});

// Button to delete invoice data
$(function () {
    $('.btnTrash').on('click', function () {
        if (sales.items.products.length === 0) return false;
        alert_action('Notificación', '¿Desea borrar todo el detalle de factura?', function () {
            sales.items.products = [];
            sales.list();
        }, function () {
            // The process is canceled.
        });
    });
});

// Delete or increase a product on the invoice
$(function () {
    $('#tableProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            let tr = tableProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Desea borrar este producto?', function () {
                sales.items.products.splice(tr.row, 1);
                sales.list();
            }, function () {
                // The process is canceled.
            });
        }).on('change keyup', 'input[name="quantity"]', function (e) {
            let quantity = parseInt($(this).val());
            let tr = tableProducts.cell($(this).closest('td, li')).index();
            if (e.target.value == '' || e.target.value == 0) {
                e.target.value = 1
                quantity = 1
            }

            sales.items.products[tr.row].quantity = quantity;
            sales.calculate_invoice();
            $('td:eq(4)', tableProducts.row(tr.row).node()).html(sales.items.products[tr.row].subtotal.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
        });
});

// Search Products to Sale
$(function () {
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        ajax: {
            delay: 150,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Búsqueda...',
        minimunInputLength: 1,
    }).on('select2:select', function (e) {
        let result;
        let data = e.params.data;

        data.quantity = 1;
        data.subtotal = 0.00;

        sales.items.products.forEach(element => {
            if (element.text == data.text) {
                result = true;
            }
        })

        if (result != true) {
            sales.add(data);
            $(this).val('').trigger('change.select2');
            return false;
        } else {
            alertSweetErrorProducts('El producto ya existe en la factura');
            $(this).val('').trigger('change.select2');
            return false;
        }
    });
});

// Search Client
$(function () {
    $('select[name="searchClient"]').select2({
        theme: "bootstrap4",
        language: 'es',
        ajax: {
            delay: 150,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                let queryParameters = {
                    term: params.term,
                    action: 'search_client'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Búsqueda por Nombre/Cédula/RIF',
        minimunInputLength: 1,
    }).on('select2:select', function (e) {
        let data = e.params.data;
        $('select[name="searchClient"]').val(data.id);
    });
});

// Button to Add New Client
$(function () {
    $('.btnAddClient').on('click', function () {
        $('#formClient')[0].reset();
        $('#modalClient').modal('show');
    });
});

// Add new Client
$(function () {
    $('#formClient').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        let parameters = new FormData(this);
        parameters.append('action', 'addClient');
        submit_with_ajax(window.location.pathname, parameters, function () {
            $('#modalClient').modal('hide');
            alertSweetSuccess('Cliente registrado con Éxito');
        });
    });
});

// Calculate Discount
$(function () {
    $('input[name="discount"]').on('change keyup', function (e) {
        let discount = $(this).val().replace(/\./g, '');
        discount = parseFloat(discount);
        if (e.target.value == '') {
            e.target.value = 0
            discount = 0
        }
        sales.items.discount = discount;
        sales.calculate_invoice();
    });
});

// Event Data Submit
$(function () {
    $('#budget').on('click', function (e) {
        e.preventDefault();
        // Validations in the form
        $('input[name="type_request"]').val(1);
        let check1 = document.getElementById("cash_payment").checked;
        let check2 = document.getElementById("credit_payment").checked;
        let select_cli = $('select[name="searchClient"]').val();
        $('select[name="method_pay"]').val(1);
        $('select[name="method_pay1"]').val(1);
        $('select[name="method_pay2"]').val(1);
        if (sales.items.products.length == 0) {
            alertSweetErrorProducts('Debe agregar un producto');
            return false;
        } else if (select_cli == '') {
            alertSweetErrorProducts('Faltan los datos del Cliente');
            return false;
        } else if (check1 != true && check2 != true) {
            alertSweetErrorProducts('Seleccione el Método de Pago');
            return false;
        } else {
            // Send Data
            let form = document.getElementById('formSale');
            let parameters = new FormData(form);
            parameters.append('sales', JSON.stringify(sales.items));
            parameters.append('action', 'addBudget');
            submit_with_ajax(window.location.pathname, parameters, function (response) {
                window.open('/panel/sale/budget/pdf/' + response.id + '/', '_blank');
                window.location.reload();
                location.href = "#top";
            });
        }
    });
});
// 
$(function () {
    $('#formSale').on('submit', function (e) {
        e.preventDefault();
        convertToUpperCase();
        // Validations in the form
        let check1 = document.getElementById("cash_payment").checked;
        let check2 = document.getElementById("credit_payment").checked;
        let select_cli = $('select[name="searchClient"]').val();
        if (sales.items.products.length == 0) {
            alertSweetErrorProducts('Debe agregar un producto');
            return false;
        } else if (select_cli == '') {
            alertSweetErrorProducts('Faltan los datos del Cliente');
            return false;
        } else if (check1 != true && check2 != true) {
            alertSweetErrorProducts('Seleccione el Método de Pago');
            return false;
        } else {
            // Send Data
            let parameters = new FormData(this);
            parameters.append('sales', JSON.stringify(sales.items));
            parameters.append('action', 'add');
            submit_with_ajax(window.location.pathname, parameters, function (response) {
                alertSweetSuccess('Venta registrada con Éxito');
                window.location.reload();
                // setTimeout(location.href = response.location, 4000);
                location.href = "#top";
            });
        }
    });
});

// $(function () {
//     document.body.style.zoom="90%"
// });