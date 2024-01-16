$(document).ready(function(){
    $(".xp-menubar").on('click',function(){
      $('#sidebar').toggleClass('active');
      $('#content').toggleClass('active');
    });
  
    $(".xp-menubar,.body-overlay").on('click',function(){
      $('#sidebar,.body-overlay').toggleClass('show-nav');
    });
  });

  $(document).ready(function() {
    var secciones = $('.seccion');
    var botonAnterior = $('.anterior');
    var botonSiguiente = $('.siguiente');
  
    var indexActual = 0;
  
    function mostrarSeccion(index) {
      secciones.hide();
      $(secciones[index]).show();
  
      // Control de visibilidad de botones
      if (index === 0) {
        botonAnterior.hide();
      } else {
        botonAnterior.show();
      }
      if (index === secciones.length - 1) {
        botonSiguiente.hide();
      } else {
        botonSiguiente.show();
      }
    }
  
    // Ocultar los botones cuando se abre el modal
    $('#miModal').on('show.bs.modal', function() {
      mostrarSeccion(indexActual);
    });
  
    botonAnterior.click(function() {
      if (indexActual > 0) {
        indexActual--;
        mostrarSeccion(indexActual);
      }
    });
  
    botonSiguiente.click(function() {
      if (indexActual < secciones.length - 1) {
        indexActual++;
        mostrarSeccion(indexActual);
      }
    });
  });

  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  
  setTimeout(function() {
      const alertList = document.querySelectorAll('.alert');
      const alerts = [...alertList].map((element) =>
      {
          const alert = new bootstrap.Alert(element);
          alert.close();
      })
  }, 5000);
  
  const hash = window.location.hash.split('/');
  const hash_route = hash[0];
  const hash_arg = hash[1];
  
  switch (hash_route) {
      case "#popup":
          const modal = new bootstrap.Modal('#' + hash_arg);
          setTimeout(function() {
              modal.show();
          }, 1000);
      break;
  
      default:
          break;
  }