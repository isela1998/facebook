
function message_error(obj) {
    contentStr = "";
    error = obj;
    alertSweetErrorProducts(error);
}

function submit_with_ajax_msj(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, 
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }else{
                            message_error(data.error);
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function submit_with_ajax(url, parameters, callback) {
    $.ajax({
        url: url, 
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                callback(data);
                return false;
            }else{
                message_error(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                message_error(textStatus + ': ' + errorThrown);
                alert();
            });
}

function alert_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    })
}

// $.getJSON("https://s3.amazonaws.com/dolartoday/data.json",function(data){
//     var dl = data.USD.transferencia;
//     // var dlv = data.USD.sicad2;
//     // var eur = data.EUR.transferencia;
//     // var cop = data.COL.venta;

//     dl = dl.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
//     document.getElementById('dl').innerHTML = dl 
//     document.getElementById('dll').innerHTML = dl

//     // dlv = dlv.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
//     // document.getElementById('dlV').innerHTML = dlv 
//     // document.getElementById('dlVV').innerHTML = dlv 

//     // eur = eur.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
//     // document.getElementById('eur').innerHTML = eur
//     // document.getElementById('eurr').innerHTML = eur

//     // cop = cop.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
//     // document.getElementById('cop').innerHTML = '$' + cop
//     // document.getElementById('copp').innerHTML = '$' + cop
// });

function alertSweetErrorProducts(title) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'botoom-end',
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'warning',
        title: title
    })
}

function alertSweetError(title) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'botoom-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'error',
        title: title
    })
}

function alertSweetSuccess(title) {
    const Toast = Swal.fire({
        position: 'center',
        icon: 'success',
        title: title,
        showConfirmButton: false,
        timerProgressBar: true,
        timer: 2000,

        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    });
}

function alertSuccess(title) {
    Swal.fire({
        position: 'center',
        icon: 'success',
        title: title,
        showConfirmButton: false,
        timer: 1000
      })
}

function numberFormat(number){
    var result = "";
        if(number[0]=="-")
        {
            newNumber=number.replace(/\./g,'').substring(1);
        }else{
            newNumber=number.replace(/\./g,'');
        }
 
        if(number.indexOf(",")>=0)
            newNumber=newNumber.substring(0,newNumber.indexOf(","));
 
        for (var j, i = newNumber.length - 1, j = 0; i >= 0; i--, j++)
            result = newNumber.charAt(i) + ((j > 0) && (j % 3 == 0)? ".": "") + result;
 
        if(number.indexOf(",")>=0)
            result+=number.substring(number.indexOf(","));
 
        if(number[0]=="-")
        {
            return "-"+result;
        }else{
            return result;
        }
}

$(function () {  
    $('.inputNumberFormat').on('click', function() {
        $(this).select();
    }).on('change keyup', function(e) {
        $(this).val($(this).val().replace(/[^0-9-,]/g, ''));
        let inputFormat = numberFormat($(this).val())
        $(this).val(inputFormat);
    }).blur(function () {
        let quantity = $(this).val()
        if(quantity == ''){
            $(this).val('0,00');
        }else if(quantity.includes(',') || quantity == '0.0'){
            //pass
        }else{
            $(this).val(quantity + ',00');
        }
    });
});

$(function () {  
    $('.inputNumbers').on('click', function() {
        $(this).select();
    }).on('change keyup', function(e) {
        $(this).val($(this).val().replace(/[^0-9-,]/g, ''));
    });
});

function convertToNumberInput(){
    $('.inputNumberFormat').each(function(){
        $(this).val($(this).val().replace(/\./g,''))
        $(this).val($(this).val().replace(/\,/g,'.'))
    });
}

function convertToUpperCase(){
    $('.UpperCase').each(function(){
        this.value = this.value.toUpperCase();
    });
}

function convertToNumberInput2(){
    $('.inputNumber').each(function(){
        $(this).val($(this).val().replace(/\./g,''))
        $(this).val($(this).val().replace(/\,/g,'.'))
    });
}

function viewText(){
    $('.text-hide').removeClass('text-hide');
}

$(function(){
    if(document.body.classList.contains('sidebar-collapse')){
        
    }else{
        
    }
});


function display_logo(){
    if(document.body.classList.contains('sidebar-collapse')){
        $('#img-sidebar-collapsed').removeClass().addClass('img-fluid img-hide')
        $('#img-sidebar').removeClass().addClass('img-fluid')
        $('#icon-expand').removeClass().addClass('fas fa-minus text-white')
    }else{
        $('#img-sidebar').removeClass().addClass('img-fluid img-hide')
        $('#img-sidebar-collapsed').removeClass().addClass('img-fluid')
        $('#icon-expand').removeClass().addClass('fas fa-plus text-white')
    }
}