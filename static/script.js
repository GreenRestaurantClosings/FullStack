// Just a bit of code to get you started. Feel free to modify!

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
        var li = $('<li>').text(result);
        $('.results').append(li);
      });
    });
});

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

        results.forEach(function(result) {
          var li = $('<li>').text(result);
          $('.results').append(li);
        });
      });
  }
});
