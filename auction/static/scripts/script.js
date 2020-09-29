$( document ).ready(function() {
  function myFunction(x) {
    if (x.matches) { // If media query matches
      document.getElementById("categories").className="row"
    } else {
      document.getElementById("categories").className="row row-cols-1"
    }
  }
  
  var x = window.matchMedia("(max-width: 991px)")
  myFunction(x) // Call listener function at run time
  x.addListener(myFunction) // Attach listener function on state changes
});

