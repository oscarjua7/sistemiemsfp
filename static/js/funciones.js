$(document).ready(function(){
    $(".xp-menubar").on('click',function(){
      $('#sidebar').toggleClass('active');
      $('#content').toggleClass('active');
    });
  
    $(".xp-menubar,.body-overlay").on('click',function(){
      $('#sidebar,.body-overlay').toggleClass('show-nav');
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

  document.addEventListener("DOMContentLoaded", function() {
    let recordsPerPage = document.getElementById('recordsPerPage');
  
    // Verificar si hay un valor almacenado y establecerlo como valor seleccionado
    if (localStorage.getItem('selectedValue')) {
      recordsPerPage.value = localStorage.getItem('selectedValue');
    }
  
    // Escuchar el evento submit del formulario
    document.getElementById('myForm').addEventListener('submit', function() {
      // Almacenar el valor seleccionado en localStorage
      localStorage.setItem('selectedValue', recordsPerPage.value);
    });
  });
  