//autocomplete function while typing
console.log("website running");
$('input').on('input', function() {
  $.ajax({
    method: 'post',
    url: '/query',
    contentType: 'application/json',
    data: JSON.stringify({
      query: $(this).val(),
      submitted:false
    })
  })
    .success(function(results) {
      $('.results').empty();

      results.forEach(function(result) {
        var li = $('<p>').text(result.name + " " + result.score);
        $('.results').append(li);
      });
    });
});

//search function after pressing 'enter'
$('input').on("keyup", function(e) {
  if (e.keyCode == 13) {
    $.ajax({
      method: 'post',
      url: '/query',
      contentType: 'application/json',
      data: JSON.stringify({
        query: $(this).val(),
        submitted:true
      })
    })
      .success(function(results) {
        $('.results').empty();


        results.forEach(function(results) {
          var li = $('<p>').text(results.name + " " + results.score);
          $('.results').append(li);
        });
      });
  }
});
