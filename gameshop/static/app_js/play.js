jQuery(function() {

  $(document).ready(function() {

    //Below is the message handler that checks incoming messages from the
    //game iframe and if they have the correct message type & origin, dispatch
    //them to the views via ajax calls and wait for response if needed (which
    // in turn) can be directed back to the game iframe.
    //
    //Basic messagetypes:
    //-SCORE and SCORE_SUCCESS that relay score to database and note success
    //-SETTINGS note game height and width which are used to adjust the game iframe
    //-SAVE and SAVE_SUCCESS that relay gamestate to database and note success
    //-LOAD_REQUEST and LOAD which relay desire for gamestate for the database and
    // return this gamestate to the game iframe
    //-ERROR which sends an error message to the game iframe that contains info
    // about the error that occured.


    $(window).on('message', function(evt) {

      var origin = evt.origin || evt.originalEvent.origin;
      if(origin=="https://staticxx.facebook.com")
        return;

      //function below enables the csrf-token functionality for simple posts
      //There is also the origin-checking below that tries to see that the game
      //messages come from the correct origin host.
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
      var csrftoken = getCookie('{{ csrf_token}}');

      var data = evt.originalEvent.data;
      var parser = document.createElement('a');
      parser.href = game_url_global;

      if (origin === parser.origin){


        //If the incoming data has valid messageType, it's forwarded to views via ajax post-calls.
        //These calls expect a json-format response message that is handled with the functions that
        //take the respond_data below (respond_data variable containing the json respond json information)

        switch (data.messageType){

          //In the first case the game score is send to back-end which updates the player highscore for
          //the current game if it's higher than his previous score (or creates a highscore if it
          //didn't exist before. Returnvalue is of messageType SCORE_SUCCESS and it includes
          //variable 'score', that is the current highscore of the player. The score is
          //displayed in the play-page and is updated with ajax call, if you get better highscore
          //than previous. (Top overall highscores are also displayed and updated on the page).

          //console.logs can be viewed to see the message types that were used.

          case "SCORE":
            $.post( '', { csrfmiddlewaretoken: csrftoken,
                        'messageType' : data.messageType,
                        'score' : data.score
                      },
                      function(response_data) {
                        $('#gameiframe')[0].contentWindow.postMessage(response_data,"*");
                        console.log(JSON.stringify(response_data));

                        var url = window.location.href;
                        url = url.replace('play','highscore');

                        $.get(url, function( data ) {
                              $( "#highscores" ).html( data );
                        });
                      },
                       "json");
          break;


          //The game sends settings at the start for window height and width which are used
          //to adjust the iframe size in the template, if they are within
          //correct value parameters. The values are percentages here as they this FileSystemStorage
          //our layout better, but they could easily be changed to pixel values (strict pixels
          // values work not as well when the whole window size changes, though).

          case "SETTING":
            var temp_width = data.options.width;  //In percentages
            var temp_height = data.options.height; //In percentages

            if((temp_width < 40)||(temp_height < 40)||(temp_width > 100)||(temp_height > 100)) {
              var error_settings = {
                messageType: "ERROR",
                info: "Size parameters are unacceptable, using default size."
                };
              $('#gameiframe')[0].contentWindow.postMessage(error_settings,"*");
              $('#gameiframe').height("100%");
              $('#gameiframe').width("100%");
            }
            else{

              $('#gameiframe').height(temp_height);
              $('#gameiframe').width(temp_width);

              console.log("Adjusting template with the settings");
            }

          break;

          //Below with the save message, gamestate is passed to views to be store into the database.
          //The load request from the game sends a request for the views for the gamestate and that
          //is returned inside a load message that is the relayed back to the game iframe.
          case "SAVE":
          $.post( '', { csrfmiddlewaretoken: csrftoken,
                        'messageType' : data.messageType,
                        'gameState' : JSON.stringify(data.gameState)
                      },
                      function(response_data) {
                        $('#gameiframe')[0].contentWindow.postMessage(response_data,"*");
                        console.log(JSON.stringify(response_data));
                      },
                       "json");
          break;

          case "LOAD_REQUEST":
          $.post( '', { csrfmiddlewaretoken: csrftoken,
                        'messageType' : data.messageType,
                        'gameState' : data.gameState
                      },
                      function(response_data) {
                        if (response_data.messageType === "ERROR"){
                          $('#gameiframe')[0].contentWindow.postMessage(response_data,"*");
                          console.log(JSON.stringify(response_data));
                        }
                        else{
                          var load_resp = {
                            "messageType" : "LOAD",
                            "gameState" : JSON.parse(response_data.gameState)
                          };
                          $('#gameiframe')[0].contentWindow.postMessage(load_resp,"*");
                        }

                      },
                       "json");
          break;

          //This is additional functionality that was not fully implmented. Idea is that
          //game would note the views an achievement for game has been achieved, and
          //the views would return the information about that achievement that would then
          //be updated to screen.
          case "ACHIEVEMENT":
          $.post( '', { csrfmiddlewaretoken: csrftoken,
                        'messageType' : data.messageType
                      },
                      function(response_data) {
                        $('#gameiframe')[0].contentWindow.postMessage(response_data,"*");
                        console.log(JSON.stringify(response_data));


                      },
                       "json");
          break;

          //if messagetype is wrong, error msg is returned to the ifrmae below.
          default:
            var error_messagetype = {
              messageType: "ERROR",
              info: "messageType is missing or incorrect"
              };
            $('#gameiframe')[0].contentWindow.postMessage(error_messagetype,"*");


        }
      }
      else{

        //if message origin is wrong, it's not processed and error is returned.
        var error_origin = {
            messageType: "ERROR",
            info: "Gamepage origin is wrong"
          };
        $('#gameiframe')[0].contentWindow.postMessage(error_origin,"*");
      }

    });

  });

});
