
var Libro = Backbone.Model.extend({});

var Libros = Backbone.Collection.extend({
  model: Libro,
  url: "data/libros.json"//
});

var libros = new Libros();
//cargamos modelo
libros.fetch();

//Inicializamos Datagrid
var datagrid = new Backgrid.Grid({
  columns: columns,
  collection: libros
});



