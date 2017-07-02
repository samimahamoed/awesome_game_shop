jQuery(function($) {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    function update_profile() {
      $.ajax({
          url : "/profile/",
          type : "POST",
          data : { username : $('#profile_username').val(),
                   first_name : $('#profile_firstname').val(),
                   last_name : $('#profile_lastname').val(),
                   email : $('#profile_email').val() },
          success : function(response) {

              $('#results').html("<div class='alert alert-success alert-dismissable'><a href='#'"+
               " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
                "<strong>Success!</strong> "+ response.message+ " </div>");
                
          },

          error : function(response) {
            $('#results').html("<div class='alert alert-danger alert-dismissable'><a href='#'"+
             " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
              "<strong>Error!</strong>"+ response.responseText + "</div>");
          }
      });
    }

     $('#profile_user_info').on('submit', function(event){
         event.preventDefault();
         update_profile();
     });


     function regenerate_token() {

       $.ajax({
           url : "/api/regenerate_token/",
           type : "POST",
           data : { sid : $('#sid').val(),
                    },
           success : function(response) {

               $('#key_result').html("<div class='alert alert-success alert-dismissable'><a href='#'"+
                " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
                 "<strong>Success!</strong> "+ response.message.result+ " </div>");
                 $('#sid').val(response.message.sid);
                 $('#skey').val(response.message.skey);


           },

           error : function(response) {
             $('#key_result').html("<div class='alert alert-danger alert-dismissable'><a href='#'"+
              " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
               "<strong>Error!</strong>"+ response.responseText + "</div>");
           }
       });
     }

      $('#access_keys').on('submit', function(event){

          event.preventDefault();
          regenerate_token();
      });

     function upload_img() {
       formdata = new FormData();
       var file = document.getElementById('id_profile_img_path').files[0];
       if (formdata) {
       formdata.append("profile_img_path", file);
       $.ajax({
           url : "/profile_img_upload/",
           type : "POST",
           data : formdata,
           processData: false,
           contentType: false,
           success : function(response) {
               //$('#profile_img').html("<img src="+response.path +" class='center-block img-responsive img-thumbnail' id = 'profile_img'>");
               //$('#profile_img').html("<img src="+response.path +" class='center-block img-responsive img-thumbnail' id = 'profile_img_modal'>");
               $("#profile_img_uploader").modal('toggle');
               location.reload();

           },

           error : function(response) {
             $('#results').html("<div class='alert alert-danger alert-dismissable'><a href='#'"+
              " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
               "<strong>Error!</strong>"+ response.responseText + "</div>");
           }
       });
      }
     }


      $('#profile_img_upload').on('submit', function(event){
          event.preventDefault();

          upload_img();
      });




      function update_rating() {
        $.ajax({
            url : "/storefront/games/play/"+$('#game_id').val()+"/",
            type : "POST",
            data : { rating : $('#rating').val()},
            success : function(response) {

                $('#results').html("<div class='alert alert-success alert-dismissable'><a href='#'"+
                 " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
                  "<strong>Success!</strong> "+ response.message+ " </div>");

            },

            error : function(response) {
              $('#results').html("<div class='alert alert-danger alert-dismissable'><a href='#'"+
               " class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+
                "<strong>Error!</strong>"+ response.message + "</div>");
            }
        });
      }

       $('#rating_submitX').on('submit', function(event){
           event.preventDefault();
           update_rating();
       });





});
