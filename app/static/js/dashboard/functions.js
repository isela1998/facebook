var sede = localStorage.getItem('sede');

function get_graph_sales() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'sede': sede,
            'action': 'get_graph_sales'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            graphcolumn.addSeries(data);
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

function get_graph_products() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'sede': sede,
            'action': 'get_graph_products'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            graphpie.addSeries(data);
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

$(function () {
    get_graph_sales();
    get_graph_products();
});

function alertSweet() {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 1000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'success',
        title: 'Precios actualizados!'
    })
}

function up_dolar() {
    var dolar = document.getElementById('dolar').value;
    var sede = localStorage.getItem('sede');
    var parameters = new FormData();
    parameters.append('dolar', dolar);
    parameters.append('sede', sede);
    parameters.append('action', 'upDolar');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            alertSweet();
            window.setTimeout(function () {
                window.location.reload();
            }, 1500);
        } else {
            alert('Ocurrió un error')
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
    });
}

function get_sales_today() {
    var sede = localStorage.getItem('sede');
    var parameters = new FormData();
    parameters.append('sede', sede);
    parameters.append('action', 'get_sales_today');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var sales_today = data.toString();
            document.getElementById('sales_today').innerHTML = sales_today;
        } else {
            //
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    });
}

function get_few_products() {
    var sede = localStorage.getItem('sede');
    var parameters = new FormData();
    parameters.append('sede', sede);
    parameters.append('action', 'get_few_products');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var few_products = data.toString();
            document.getElementById('few_products').innerHTML = few_products;
        } else {
            //
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

$(function () {
    get_sales_today();
    get_few_products();
});