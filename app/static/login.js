function sendotp(token) {

    if (token != null) {
        emailvalidate() &&
        mobilevalidation() &&
        $.ajax({
            type: "POST",
            url: "/getotp",
            data: {
                email: $("#email").val().replace("'", ""),
                mobile: $("#phone").val(),
                token: token,

            },
            async: false,
            cache: !1,

            success: function (e) {
                if (1 == e) {
                    $('#getotp').hide()
                    $("#errorName").hide()
                    $('#otpcontainer').show()
                    /*$('#phone').hide()*/
                    $('#phone').attr('disabled', 'disabled');
                    $('#email').attr('disabled', 'disabled');
                    $('#submitform').show()
                    $("#resendotp").delay(30000).fadeIn();
                    $("#errorName").html("OTP has been successfuly sent to your Email ID & Mobile Number").show();
                    $("#errorName").delay(12000).fadeOut()
                } else {
                    $("#errorName").html("There is somthing wrong at the moment,").show();
                }


            },
            timeout: 15000,
        }).fail(function (jqXHR, textStatus, errorThrown) {
            $("#errorName").html("There is somthing wrong at the moment").show();


            console.log(errorThrown);
        });
    }

}


function resendotp() {
    emailvalidate() && mobilevalidation() &&
    $.ajax({
        type: "POST",
        url: "/resendotp",
        data: {email: $("#email").val().replace("'", ""), mobile: $("#phone").val()},
        async: false,
        cache: !1,
        success: function (e) {
            if (1 == e) {
                $('#getotp').hide()
                $("#errorName").hide()
                $('#otpcontainer').show()
                /*$('#phone').hide()*/
                $('#phone').attr('disabled', 'disabled');
                $('#resendotp').hide()
                $('#email').attr('disabled', 'disabled');
                $('#submitform').show()
                $("#errorName").html("OTP has been successfuly sent to your Email ID & Mobile Number").show();
                $("#resendotp").delay(12000).fadeIn();
            } else {
                $("#errorName").html("There is somthing wrong at the moment,").show();
            }


        },
        timeout: 15000,
    }).fail(function (jqXHR, textStatus, errorThrown) {
        $("#errorName").html("There is somthing wrong at the moment").show();


        console.log(errorThrown);
    });
}

function submit() {
    emailvalidate() &&
    mobilevalidation() &&
    otpvalidation() &&
    $.ajax({
        type: "POST",
        url: "/confirmotp",
        data: {
            email: $("#email").val().replace("'", ""), mobile: $("#phone").val(),
            otp: $('#otpcontainer').val()
        },
        async: !0,
        cache: !1,
        success: function (res) {
            if (res.redirect) {
                window.location.href = res.redirect_url;
            } else {
                $("#errorName").html("Enter a correct OTP").show();
            }


        },
        timeout: 15000,
    }).fail(function (jqXHR, textStatus, errorThrown) {
        $("#errorName").html("There is something wrong at the moment, please try after some time").show();


        console.log(errorThrown);
    });

}

function isNumberKey(e) {
    var t = e.which ? e.which : event.keyCode;
    $('#errorName').hide();
    return !(t > 31 && (t < 48 || t > 57));
}


function mobilevalidation() {
    if ("" == $("#phone").val()) {
        $("#phone").focus();
        $("#errorName").html("Please a enter a Mobile Number to procceed").show();
    } else if (10 !== $("#phone").val().length) {
        $("#phone").focus();
        $("#errorName").html("Please enter a vaild Mobile Number to procceed").show();
    } else
        return true;
}

function emailvalidate() {
    let email = /[-a-zA-Z0-9_\.]+@[-a-zA-Z0-9]+\.[-a-zA-Z0-9\.]+/


    if ($('#email').val().trim().match(email)) {
        return true
    } else if ("" == $("#email").val()) {
        $("#email").focus();
        $("#errorName").html("Please a enter a Email ID to procceed").show();
    } else
        $("#email").focus();
    $("#errorName").html("Please enter a valid Email ID to procceed").show();
}

function otpvalidation() {
    if ("" == $("#otpContainer").val()) {
        $("#otpContainer").focus();
        $("#errorName").html("Please a enter a otp which has been sent mobile number").show();
    } else if (6 !== $("#otpcontainer").val().length) {
        $("#otpcontainer").focus();
        $("#errorName").html("Please enter a vaild OTP to procceed").show();
    } else
        return true;


}
