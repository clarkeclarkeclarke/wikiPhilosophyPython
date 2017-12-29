$(document).ready(function() {

  var jobCount = $('#list .in').length;
  $('.list-count').text(jobCount + ' items');

  $('#btn_run').click(function() {
    /*console.log($('#userinput').val());
    var output = document.getElementById('userinput').value;
    console.log(output);
    console.log("HIII");*/
    $.ajax(
      {
        type: "GET",
        url: "http://127.0.0.1:8080/wikiPhilosophy.py" ,
        data: {param: output},
        success: function(response)
          {
            console.log('Python script executed...');
            alert(response);
          },
        error: function(data)
        {
          console.log('Error...');
         alert(data.responseText);
       },
     });
  });

  /* $("#search-text").keyup(function () {
     //$(this).addClass('hidden');

    var searchTerm = $("#search-text").val();
    var listItem = $('#list').children('li');


    var searchSplit = searchTerm.replace(/ /g, "'):containsi('")

      //extends :contains to be case insensitive
  $.extend($.expr[':'], {
  'containsi': function(elem, i, match, array)
  {
    return (elem.textContent || elem.innerText || '').toLowerCase()
    .indexOf((match[3] || "").toLowerCase()) >= 0;
  }
});


    $("#list li").not(":containsi('" + searchSplit + "')").each(function(e)   {
      $(this).addClass('hiding out').removeClass('in');
      setTimeout(function() {
          $('.out').addClass('hidden');
        }, 300);
    });

    $("#list li:containsi('" + searchSplit + "')").each(function(e) {
      $(this).removeClass('hidden out').addClass('in');
      setTimeout(function() {
          $('.in').removeClass('hiding');
        }, 1);
    });


      var jobCount = $('#list .in').length;
    $('.list-count').text(jobCount + ' items');

    //shows empty state text when no jobs found
    if(jobCount == '0') {
      $('#list').addClass('empty');
    }
    else {
      $('#list').removeClass('empty');
    }

  });



     /*
     An extra! This function implements
     jQuery autocomplete in the searchbox.
     Uncomment to use :)


 function searchList() {
    //array of list items
    var listArray = [];

     $("#list li").each(function() {
    var listText = $(this).text().trim();
      listArray.push(listText);
    });

    $('#search-text').autocomplete({
        source: listArray
    });


  }

  searchList();
*/


});
