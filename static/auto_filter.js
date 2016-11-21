    $(document).ready(function(){
    $("#auto").autocomplete({
      source: "/autocomplete",
      minLength: 1,
      select: function( event, ui ) { 
      		var code = ui.item.value.split(":")[0];
          var title = ui.item.value.split(":")[1];
          $("#auto").val(code);
      		event.preventDefault();
          location.href = "/similarity?code=" + code + "&title=" + title;
      		return false;}
     });
    });

function insert_code(caller,code,position) {
  alert(code);
  $("#auto").val(code);
}

// $('.typeahead').typeahead({
//   hint: true,
//   highlight: true,
//   minLength: 1
// },
// {
//   name: 'term',
//   source: jQuery.getJSON('/autocomplete?term=' + term)
// });