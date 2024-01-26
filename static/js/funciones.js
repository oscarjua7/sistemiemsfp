$(document).ready(function() {
    // Ocultar la barra por defecto
    $('#sidebar, #content').addClass('active');
  
    // Manejar el evento de clic o toque en la barra
    $(".xp-menubar").on('click touchstart', function() {
      // Alternar las clases 'active' según el estado actual
      $('#sidebar, #content').toggleClass('active');
      $('.body-overlay').toggleClass('show-nav');
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
    document.getElementById('form_alumnos').addEventListener('submit', function() {
      // Almacenar el valor seleccionado en localStorage
      localStorage.setItem('selectedValue', recordsPerPage.value);
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    let recordsPerPageDocentes = document.getElementById('recordsPerPageDocentes');
  
    // Verificar si hay un valor almacenado y establecerlo como valor seleccionado
    if (localStorage.getItem('selectedValueDocentes')) {
      recordsPerPageDocentes.value = localStorage.getItem('selectedValueDocentes');
    }
  
    // Escuchar el evento submit del formulario
    document.getElementById('form_docentes').addEventListener('submit', function() {
      // Almacenar el valor seleccionado en localStorage
      localStorage.setItem('selectedValueDocentes', recordsPerPageDocentes.value);
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let recordsPerPagePersonal = document.getElementById('recordsPerPagePersonal');
  
    // Verificar si hay un valor almacenado y establecerlo como valor seleccionado
    if (localStorage.getItem('selectedValuePersonal')) {
      recordsPerPagePersonal.value = localStorage.getItem('selectedValuePersonal');
    }
  
    // Escuchar el evento submit del formulario
    document.getElementById('form_personal').addEventListener('submit', function() {
      // Almacenar el valor seleccionado en localStorage
      localStorage.setItem('selectedValuePersonal', recordsPerPagePersonal.value);
    });
});

////////////////////////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function() {
    // Función para convertir a mayúsculas
    function convertirMayusculas(inputId) {
        var input = document.getElementById(inputId);

        input.addEventListener("input", function() {
            this.value = this.value.toUpperCase();
        });
    }

    // Validación del nombre
    var nombreInput = document.getElementById("nombre_alumno");
    var mensajeNombre = document.createElement("div");
    mensajeNombre.classList.add("text-danger");
    mensajeNombre.id = "mensajeNombre";
    nombreInput.parentNode.appendChild(mensajeNombre);

    nombreInput.addEventListener("input", function() {
        var valor = this.value;

        if (valor.trim().length === 0) {
            mensajeNombre.innerHTML = "";
        } else if (/^[a-zA-Z\sáéíóúÁÉÍÓÚüÜñÑ]+$/.test(valor)) {
            mensajeNombre.innerHTML = "";
        } else {
            mensajeNombre.innerHTML = "Solo se aceptan letras, espacios y caracteres acentuados en español.";
        }
    });

    // Validación del sexo
    var mensajeSexo = document.getElementById("mensajeSexo");

    document.getElementById("sexo_alumno").addEventListener("change", function() {
        var seleccion = this.value;

        if (seleccion === "") {
            mensajeSexo.innerHTML = "Selecciona un sexo";
        } else {
            mensajeSexo.innerHTML = "";
        }
    });

    // Validación del estatus
    var mensajeEstatus = document.getElementById("mensajeEstatus");

    document.getElementById("estatus_alumno").addEventListener("change", function() {
        var seleccion = this.value;

        if (seleccion === "") {
            mensajeEstatus.innerHTML = "Selecciona un estatus";
        } else {
            mensajeEstatus.innerHTML = "";
        }
    });

    // Validación del CURP
    var curpInput = document.getElementById("curp_alumno");
    var mensajeCurp = document.createElement("div");
    mensajeCurp.classList.add("text-danger");
    mensajeCurp.id = "mensajeCurp";
    curpInput.parentNode.appendChild(mensajeCurp);

    convertirMayusculas("curp_alumno"); // Convertir a mayúsculas

    // Mantener oculto el mensaje hasta clic en el botón de enviar
    mensajeCurp.style.display = "none";

    curpInput.addEventListener("input", function() {
        var curpValue = this.value;

        if (curpValue.trim().length === 0) {
            mensajeCurp.innerHTML = "";
        } else if (curpValue.length <= 18 && /^[A-Z0-9]+$/.test(curpValue)) {
            mensajeCurp.innerHTML = "";
        } else {
            mensajeCurp.innerHTML = "El CURP debe contener como máximo 18 caracteres, solo letras mayúsculas y números.";
        }
    });

    // Validación del folio
    var folioInput = document.getElementById("folio_alumno");
    var mensajeFolio = document.createElement("div");
    mensajeFolio.classList.add("text-danger");
    mensajeFolio.id = "mensajeFolio";
    folioInput.parentNode.appendChild(mensajeFolio);

    folioInput.addEventListener("input", function() {
        var valor = this.value;

        if (valor.trim().length === 0) {
            mensajeFolio.innerHTML = "";
        } else if (/^[0-9]{1,7}$/.test(valor)) {
            mensajeFolio.innerHTML = "";
        } else {
            mensajeFolio.innerHTML = "Solo se aceptan números enteros sin puntos y sin letras.";
        }
    });

    // Validación del teléfono
    var telefonoInput = document.getElementById("telefono_alumno");
    var mensajeTelefono = document.createElement("div");
    mensajeTelefono.classList.add("text-danger");
    mensajeTelefono.id = "mensajeTelefono";
    telefonoInput.parentNode.appendChild(mensajeTelefono);

    // Mantener oculto el mensaje hasta clic en el botón de enviar
    mensajeTelefono.style.display = "none";

    telefonoInput.addEventListener("input", function() {
        var valor = this.value;

        if (valor.trim().length === 0) {
            mensajeTelefono.innerHTML = "";
        } else if (/^[0-9]{10}$/.test(valor)) {
            mensajeTelefono.innerHTML = "";
        } else {
            mensajeTelefono.innerHTML = "Solo se aceptan números enteros sin letras y sin otros caracteres.";
        }
    });

    // Validación antes de enviar el formulario
    document.getElementById("btnGuardar").addEventListener("click", function(event) {
        var seleccionSexo = document.getElementById("sexo_alumno").value;
        var seleccionEstatus = document.getElementById("estatus_alumno").value;
        var folioValue = folioInput.value;

        if (seleccionSexo === "") {
            mensajeSexo.innerHTML = "Selecciona un sexo";
            event.preventDefault();
        } else {
            mensajeSexo.innerHTML = "";
        }

        if (seleccionEstatus === "") {
            mensajeEstatus.innerHTML = "Selecciona un estatus";
            event.preventDefault();
        } else {
            mensajeEstatus.innerHTML = "";
        }

        if (folioValue.trim().length > 0 && !/^[0-9]{1,7}$/.test(folioValue)) {
            mensajeFolio.innerHTML = "Solo se aceptan números enteros sin puntos y sin letras.";
            event.preventDefault();
        } else {
            mensajeFolio.innerHTML = "";
        }

        var curpValue = curpInput.value;

        if (curpValue.trim().length > 0 && (curpValue.length !== 18 || !/^[A-Z0-9]+$/.test(curpValue))) {
            mensajeCurp.innerHTML = "El CURP debe contener como máximo 18 caracteres, solo letras mayúsculas y números.";
            mensajeCurp.style.display = "block";
            event.preventDefault();
        } else {
            mensajeCurp.innerHTML = "";
            mensajeCurp.style.display = "none";
        }

        var telefonoValue = telefonoInput.value;

        if (telefonoValue.trim().length > 0 && !/^[0-9]{10}$/.test(telefonoValue)) {
            mensajeTelefono.innerHTML = "Obligatorio contener 10 números enteros sin letras y sin otros caracteres.";
            mensajeTelefono.style.display = "block";
            event.preventDefault();
        } else {
            mensajeTelefono.innerHTML = "";
            mensajeTelefono.style.display = "none";
        }

        // Puedes agregar más validaciones según tus requisitos para otros campos
    });
});