/* function toggleMiniBar() {
    var miniBar = document.getElementById("nav-minibar");
    if (miniBar.style.height === "40px") {
      miniBar.style.height = "0";
    } else {
      miniBar.style.height = "40px";
    }
  }
  
   */


  var categoriesButton = document.getElementById("categories-button");
  var miniBar = document.getElementById("nav-minibar");
  

  categoriesButton.addEventListener("mouseenter", function() {
    miniBar.style.height = "50px"; 
  });
  

  miniBar.addEventListener("mouseleave", function(event) {
    if (!isCursorOverElement(event, categoriesButton)) {
      miniBar.style.height = "0"; 
    }
  });
  

  function isCursorOverElement(event, element) {
    var elementRect = element.getBoundingClientRect();
    return (
      event.clientX >= elementRect.left &&
      event.clientX <= elementRect.right &&
      event.clientY >= elementRect.top &&
      event.clientY <= elementRect.bottom
    );
  }
  
  