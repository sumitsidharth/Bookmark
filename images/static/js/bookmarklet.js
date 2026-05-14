// Dynamic site URL detection
const script = document.currentScript || (function() {
  var scripts = document.getElementsByTagName('script');
  return scripts[scripts.length - 1];
})();
const siteUrl = script.src.split('/static/')[0] + '/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';

const minWidth = 250;
const minHeight = 250;

// load CSS
var head = document.getElementsByTagName('head')[0];

var link = document.createElement('link');

link.rel = 'stylesheet';
link.type = 'text/css';

link.href =
    styleUrl + '?r=' + Math.floor(Math.random() * 999999999);

head.appendChild(link);

// load HTML
var body = document.getElementsByTagName('body')[0];

boxHtml = `
<div id="bookmarklet">
    <a href="#" id="close">&times;</a>

    <h1>Select an image to bookmark:</h1>

    <div class="images"></div>
</div>`;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');

    // clear images found
    imagesFound.innerHTML = '';

    // display bookmarklet
    bookmarklet.style.display = 'block';

    // close event
    bookmarklet.querySelector('#close')
        .addEventListener('click', function () {
            bookmarklet.style.display = 'none'
        });

    // find images in the DOM with the minimum dimensions
    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');

    images.forEach(image => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            var imageFound = document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        }
    })

    // select image event
    imagesFound.addEventListener('click', function (event) {
        if (event.target.tagName === 'IMG') {
            imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)
                + '&title='
                + encodeURIComponent(document.title),
                '_blank');
        }
    }, false);
}

// launch the bookmarklet
bookmarkletLaunch();