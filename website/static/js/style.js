window.onload = function() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("content").style.display = "block";
};

var myCarousel = document.querySelector('#mainCarousel')
var carousel = new bootstrap.Carousel(myCarousel, {
    interval: 3000,
    ride: 'carousel'
})