var leadid = "",
    ddlval = "",
    enqbtn = "",
    partialsubmit = 0,
    isvalidated = 0,
    alpha = /[a-zA-Z ]+/,
    num = /[0-9.]+/,
    email = /[-a-zA-Z0-9_\.]+@[-a-zA-Z0-9]+\.[-a-zA-Z0-9\.]+/,
    circle = 0;

var d = new Date();
var strDate =  d.getDate() + "/" + (d.getMonth()+1) + "/" +d.getFullYear();

var example = flatpickr('#flatpickr');
flatpickr('#flatpickr',{
// A string of characters which are used to define how the date will be displayed in the input box.
    dateFormat: 'd-m-Y',
    disable: [ { 'from': '2-04-2000', 'to': strDate } ]
})


function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    let x = position.coords.latitude
    $.ajax({
        type: "POST",
        url: "/getlocation",
        data: {lat: position.coords.latitude, long: position.coords.longitude},
        async: !0,
        cache: !1,
        success: function (data) {
                $('#address').val(data.line1) & $('#address').addClass('filled');
                $('#pincode').val(data.pincode).addClass('filled');
                $('#landmark').val(data.landmark).addClass('filled');
            },

    });
}



function lol() {
    return (

        landing_validation()

        &&

        $.ajax({
            type: "POST",
            url: "/contact/userform",
            data:
                {
                name : $("#txtName").val(),
                address : $("#address").val(),
                landmark : $("#landmark").val(),
                    pincode : $("#pincode").val(),
                test_type : $('#test_type').val(),
                no_ofpatients : $('#no_ofpatients').val(),
                date : $('#flatpickr').val()
                  },
            success: function (res) {
                // check redirect
                if (res.redirect) {
                    window.location.href = res.redirect_url;
                }
                else {
                    let login = '/login'
                    window.location.href = login
                    }
            },

            async: !1,
            cache: !1,

        })

    );
}



function resetValues() {
    document.forms[0].reset();
}



function landing_validation() {
    return "" == $.trim($("#txtName").val()) ? ($("#txtName").focus(), $("#errorName").html("Name is required.").show(), !1) :
        "" == $.trim($("#address").val()) ? ($("#address").focus(), $("#errorName").html("Address is required.").show(), !1) :
            "" == $.trim($("#landmark").val()) ? ($("#landmark").focus(), $("#errorName").html("Landmark is required.").show(), !1) :
                "" == $.trim($("#test_type").val()) ? ($("#test_type").focus(), $("#errorName").html("Test type is required.").show(), !1) :
                     "" == $.trim($("#no_ofpatients").val()) ? ($("#no_ofpatients").focus(), $("#errorName").html("No of patients is required.").show(), !1) :
                         "" == $.trim($("#flatpickr").val()) ? ($("#flatpickr").focus(), $("#errorName").html("appointment Date is required.").show(), !1) :
                "" == $("#pincode").val()? ($("#pincode").focus(), $("#errorName").html("Pincode is required.").show(), !1) :

                        6 == $("#pincode").val().length || ($("#pincode").focus(), $("#errorName").html("Enter a Valid Pincode No").show(), !1) ;}





function isCharKey(e) {
    var t = e.which ? e.which : event.keyCode;
    return (t > 31 && (t < 48 || t > 57)) || 8 == t;
}

function isNumberKey(e) {
    var t = e.which ? e.which : event.keyCode;
    return !(t > 31 && (t < 48 || t > 57));
}






$(document).ready(function () {

        $("#txtName, #txtorganization, #txtEmail, #txtmobileno").bind("copy paste cut", function (e) {
            e.preventDefault();
        }),
        $("#resendOTP").click(function () {
            resendcode();
        }),
        $(".rbEnquiry_Comp").prop("checked", !0),
        $(".rbEnquiry_My").click(function () {
            $(this).is(":checked") && ($("#c_form").hide(), $("#Enq_My").show());
        }),
        $(".rbEnquiry_Comp").click(function () {
            $(this).is(":checked") && ($("#Enq_My").hide(), $("#c_form").show());
        })


});


