$(document).ready(function () {
    $('.toll_free_content').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: false,
        dots: true
    });
    (function () {
        $('.input_container').find('.floatlabel').each(function () {
            $(this).on('change', function () {
                $this = $(this);
                if (this.value !== "") {
                    $this.addClass('filled');
                } else {
                    $this.removeClass('filled');
                }
            });
        });
    })();
});
if (window.matchMedia("(min-width: 767px)").matches) {
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        if (scroll >= 400) {
            $(".sticky").addClass("orangeForm");
        } else {
            $(".sticky").removeClass("orangeForm");
        }
    });
}

