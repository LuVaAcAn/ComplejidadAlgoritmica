function generarGrafo() {
  var cantidadNodos = document.getElementById('cantidad-nodos').value;
   var nombrePadre = document.getElementById('nombre-padre').value;
   var nombreEvitar = document.getElementById('nombre-evitar').value;
   var genero = document.getElementById('genero').value

  // Realizar una solicitud POST a la ruta '/grafo' del servidor
  $.ajax({
    url: '/grafo',
    type: 'POST',
    data: { 'cantidad-nodos': cantidadNodos, 'nombre-padre': nombrePadre, 'nombre-evitar': nombreEvitar, 'genero': genero },
    success: function (response) {
      // Actualizar la imagen del grafo
      var imagenGrafo = document.getElementById('imagen-grafo');
      imagenGrafo.src = response.imagen_grafo + '?' + new Date().getTime();

      // Actualizar los nombres populares
      var nombresPopulares = document.getElementById('nombres-populares');
      nombresPopulares.innerHTML = '';
      response.nombres_populares.forEach(function (nombre) {
        nombresPopulares.innerHTML += '<li>' + nombre[0] + ' (Apariciones: ' + nombre[1] + ')</li>';
      });

      // Actualizar los nombres menos populares
      var nombresMenosPopulares = document.getElementById('nombres-menos-populares');
      nombresMenosPopulares.innerHTML = '';
      response.nombres_menos_populares.forEach(function (nombre) {
      nombresMenosPopulares.innerHTML += '<li>' + nombre[0] + ' (Apariciones: ' + nombre[1] + ')</li>';
      });
    },
    error: function (error) {
      console.log(error);
    }
  });
}

// Asignar el evento de clic al botón 'Generar Grafo'
document.getElementById('generar-btn').addEventListener('click', generarGrafo);
