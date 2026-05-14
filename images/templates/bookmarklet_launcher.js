(function () {
    if (!window.bookmarklet) {

        bookmarklet_js = document.body.appendChild(
            document.createElement('script')
        );

        bookmarklet_js.src =
            '//127.0.0.1:8000/static/js/bookmarklet.js';

        window.bookmarklet = true;
    }
    else {
        bookmarkletLaunch();
    }
})();