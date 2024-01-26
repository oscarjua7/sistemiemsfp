$(document).ready(function() {
    // Verificar si el usuario ha elegido ocultar la barra en el pasado
    var isSidebarHidden = localStorage.getItem('sidebarHidden') === 'true';
  
    // Aplicar la clase 'active' y 'show-nav' según la elección del usuario
    if (!isSidebarHidden) {
      $('#sidebar, #content').addClass('active');
      $('.body-overlay').addClass('show-nav');
    }
  
    // Manejar el evento de clic en la barra
    $(".xp-menubar").on('click', function() {
      // Alternar las clases 'active' según el estado actual
      $('#sidebar, #content').toggleClass('active');
      $('.body-overlay').toggleClass('show-nav');
  
      // Actualizar el estado en el almacenamiento local
      var isSidebarHiddenNow = !$('#sidebar').hasClass('active');
      localStorage.setItem('sidebarHidden', isSidebarHiddenNow);
    });
  });