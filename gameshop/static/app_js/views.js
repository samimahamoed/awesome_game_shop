jQuery(function($) {

    $('#my_games').on('click', function(event){
        event.preventDefault();
         window.location.hash = '#my_games_tb';
    });

    $('#sales').on('click', function(event){
        event.preventDefault();
         window.location.hash = '#sales_tb';
    });

    $('#contributions').on('click', function(event){
      event.preventDefault();
       window.location.hash = '#contributions_tb';
    });



        $('#star_1').on('click', function(event){
            event.preventDefault();
            if($(this.children[0]).hasClass( "active" )){
                 $("#rating_value").val(0);

                 $(this).html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_2').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_3').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_4').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");

            }else{
                  $("#rating_value").val(1);

                  $(this).html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_2').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                  $('#star_3').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                  $('#star_4').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                  $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
            }
        });


        $('#star_2').on('click', function(event){
            event.preventDefault();
            if($(this.children[0]).hasClass( "active" )){

                 $("#rating_value").val(1);

                 $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $(this).html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_3').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_4').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");

            }else{
                  $("#rating_value").val(2);
                  $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $(this).html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_3').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                  $('#star_4').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                  $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
            }
        });

        $('#star_3').on('click', function(event){
            event.preventDefault();
            if($(this.children[0]).hasClass( "active" )){
                 $("#rating_value").val(2);
                 $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $('#star_2').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $(this).html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_4').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");

            }else{
                  $("#rating_value").val(3);
                  $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_2').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $(this).html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_4').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                  $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
            }
        });


        $('#star_4').on('click', function(event){
            event.preventDefault();
            if($(this.children[0]).hasClass( "active" )){
                 $("#rating_value").val(3);
                 $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $('#star_2').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $('#star_3').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $(this).html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
                 $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");

            }else{
                  $("#rating_value").val(4);

                  $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_2').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_3').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $(this).html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_5').html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");
            }
        });

        $('#star_5').on('click', function(event){
            event.preventDefault();
            if($(this.children[0]).hasClass( "active" )){
                 $("#rating_value").val(4);
                 $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $('#star_2').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $('#star_3').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $('#star_4').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                 $(this).html("<span  class='glyphicon glyphicon-star' aria-hidden='true'></span>");

            }else{
                  $("#rating_value").val(5);
                  $('#star_1').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_2').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_3').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $('#star_4').html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
                  $(this).html("<span  class='glyphicon glyphicon-star active' aria-hidden='true'></span>");
            }

        });


});
