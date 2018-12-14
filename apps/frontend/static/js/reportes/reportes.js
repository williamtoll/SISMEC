function mostrarPDF(){



var pdfData=$("#reporte-base64").val();

if(!pdfData)
  return;
  
var el_pdf=pdfData;

pdfData=atob(el_pdf.trim());

 // Loaded via <script> tag, create shortcut to access PDF.js exports.
var pdfjsLib = window['pdfjs-dist/build/pdf'];

// The workerSrc property shall be specified.
pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

// Using DocumentInitParameters object to load binary data.
var loadingTask = pdfjsLib.getDocument({data: pdfData});
loadingTask.promise.then(function(pdf) {
  console.log('PDF loaded');
  
  // Fetch the first page
  var pageNumber = 1;
  pdf.getPage(pageNumber).then(function(page) {
    console.log('Page loaded');
    
    var scale = 1.5;
    var viewport = page.getViewport(scale);

    // Prepare canvas using PDF page dimensions
    var canvas = document.getElementById('the-canvas');
    var context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: context,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);
    renderTask.then(function () {
      console.log('Page rendered');
    });
  });
}, function (reason) {
  // PDF loading error
  console.error(reason);
});

}



$(document).ready(function() {
  var select_cliente = $('#id_cliente_select');
  inicializarSelectGenerales();
  function inicializarSelectGenerales() {
      select_cliente.select2({
        tags: true,
        multiple: false,
        tokenSeparators: [','],
        allowClear: true,
        placeholder: "Seleccione el nombre del cliente",
        ajax: {
            url: '/sismec/ajax/getClienteAutocomplete/',
            dataType: "json",
            type: "GET",
            data: function (params) {
                var queryParameters = {
                    nombres: params.term
                };
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.nombres,
                            id: item.id
                        };
                    })
                };
            }
        }
    })
    .on('select2:unselect ', function () {
        select_cliente.find('option').remove().end();
        select_cliente.val('').trigger('change');
    });
  }
});
