(function ($) {
    "use strict";

    /**
     * Removes the spinner element by removing the "show" class.
     */
    const removeSpinner = () => {
        setTimeout(() => {
            const $spinner = $('#spinner');
            if ($spinner.length) {
                $spinner.removeClass('show');
            }
        }, 1);
    };

    removeSpinner();

    // Initialize WOW.js if available
    if (typeof WOW === "function") {
        new WOW().init();
    }

    /**
     * Toggles the sticky navbar and back-to-top button based on scroll position.
     */
    const handleScrollEvents = () => {
        const scrollTop = $(window).scrollTop();

        // Toggle sticky class for navbar
        $('.nav-bar').toggleClass('sticky-top', scrollTop > 45);

        // Toggle the visibility of the back-to-top button
        $('.back-to-top').fadeToggle(scrollTop > 300, 'slow');
    };

    // Attach combined scroll event handler
    $(window).on('scroll', handleScrollEvents);

    // Smooth scroll to top when the back-to-top button is clicked
    $('.back-to-top').on('click', (event) => {
        event.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 100, 'easeInOutExpo');
    });

    // Initialize header carousel with Owl Carousel settings
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
    });

    // Initialize testimonial carousel with Owl Carousel settings
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        autoplayTimeout: 2500,
        smartSpeed: 800,
        margin: 24,
        dots: false,
        loop: true,
        responsive: {
            0: { items: 1 },
            992: { items: 2 }
        }
    });

})(jQuery);

/**
 * Copies the provided email address to the clipboard.
 * Uses the Clipboard API when available, with a fallback for legacy browsers.
 *
 * @param {string} email - The email address to copy. Defaults to "kittim1000@gmail.com".
 */
function copyEmailToClipboard(email = "kittim1000@gmail.com") {
    if (navigator.clipboard && window.isSecureContext) {
        // Modern asynchronous clipboard API
        navigator.clipboard.writeText(email)
            .then(() => {
                alert(`이메일 주소가 클립보드에 복사되었습니다: ${email}`);
            })
            .catch(err => {
                console.error('Failed to copy email:', err);
            });
    } else {
        // Fallback for older browsers
        const tempInput = document.createElement("input");
        tempInput.style.position = "absolute";
        tempInput.style.left = "-9999px";
        tempInput.value = email;
        document.body.appendChild(tempInput);
        tempInput.select();
        try {
            document.execCommand("copy");
            alert(`이메일 주소가 클립보드에 복사되었습니다: ${email}`);
        } catch (err) {
            console.error('Fallback: Unable to copy', err);
        }
        document.body.removeChild(tempInput);
    }
}

/**
 * Displays a confirmation dialog to check if the user has upload permissions.
 * If the user fails to authenticate correctly multiple times, additional restrictions may apply.
 *
 * @returns {boolean} True if the user confirms, false otherwise.
 */
function confirmPresident() {
    const message = "업로드 권한이 있으신가요?\n비밀번호를 7번 틀릴 시 24 시간동안 로그인 접근이 불가능합니다";
    return confirm(message);
}
