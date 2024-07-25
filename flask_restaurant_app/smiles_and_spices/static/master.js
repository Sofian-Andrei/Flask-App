const debounce = (fn) => {
  let frame;
  return (...params) => {
    if (frame) {
      cancelAnimationFrame(frame);
    }
    frame = requestAnimationFrame(() => {
      fn(...params);
    });
  }
};
const storeScroll = () => {
  document.documentElement.dataset.scroll = window.scrollY;
}
document.addEventListener('scroll', debounce(storeScroll), { passive: true });
storeScroll();

setTimeout(function() {
var alertList = document.querySelectorAll('.alert');
alertList.forEach(function (alertNode) {
bootstrap.Alert.getOrCreateInstance(alertNode).close();
})
}, 500)


$( document ).ready(function() {

    $('#form input[type=radio]').on('change', function(event) {
            var result = $(this).val();
            $('#form').submit();
        });
});

$( document ).ready(function() {

    $('#checkout-form input[type=radio]').on('change', function(event) {
            var result = $(this).val();
            $('#checkout-form').submit();
        });
});


// Get the modal
var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById('myImg');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    modalImg.alt = this.alt;
    captionText.innerHTML = this.alt;
}


// When the user clicks on <span> (x), close the modal
modal.onclick = function() {
    img01.className += " out";
    setTimeout(function() {
       modal.style.display = "none";
       img01.className = "modal-content";
     }, 400);

 }


//$(document).ready(function() {
//    $("#CloseAll").on('click', function() {
//        $(".collapse").removeClass("show");
//    });
//});
//$( document ).ready(function() {
//
//    $('#check-form input[type=checkbox]').on('change', function(event) {
//            var result = $(this).val();
//            $('#check-form').submit();
//        });
//});


//function submitForm() {
//    document.getElementById("checkout-form").submit();
//}
//
//if (document.getElementById("checkout-form")) {
//    setTimeout("submitForm()", 2000);
//}