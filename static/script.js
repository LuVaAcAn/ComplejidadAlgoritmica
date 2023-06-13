function generarGrafo() {
  var cantidadNodos = document.getElementById('cantidad-nodos').value;

  // Realizar una solicitud POST a la ruta '/grafo' del servidor
  $.ajax({
    url: '/grafo',
    type: 'POST',
    data: { 'cantidad-nodos': cantidadNodos },
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

      // Actualizar los nombres afines
      var nombresAfines = document.getElementById('nombres-afines');
      nombresAfines.innerHTML = '';
      response.nombres_afines.forEach(function (afin) {
        nombresAfines.innerHTML += '<li>' + afin[0] + ' : ' + ' (Afinidad: ' + afin[1] + '%)</li>';
      });
    },
    error: function (error) {
      console.log(error);
    }
  });
}

// Asignar el evento de clic al botón 'Generar Grafo'
document.getElementById('generar-btn').addEventListener('click', generarGrafo);