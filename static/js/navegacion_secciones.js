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