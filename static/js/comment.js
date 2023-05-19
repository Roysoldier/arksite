function denum(id) {



      var sendrequest = {
          "id": id
      }

      $(function () {
          $.ajax({
              type: 'POST',
              url: "api/denum",
              data: JSON.stringify(sendrequest),
              contentType: "application/json",
              dataType: "json",
              success: function (result) {
                  if (result.status == "ok") {
                      var ncomment = '<div class="comment"> <a class="pp-profile"> <img src="./static/data/'+ cpp +'" alt="mdo" width="50" height="50" class="rounded-circle"> </a> <p class="name-comment">' + pseudo + '</p> <p class="text-comment">' + comment.replace("¤", "'") + '</p> <br /></div>'
                      $('#box-chat').append(ncomment);
                      var chatBox = $('#myModal').find('.box-chat');
                      
                      document.getElementById('newcomment').value = ''
                      chatBox.scrollTop(chatBox[0].scrollHeight);
                      

                  }
                  else if (result.status == "final") {
                    window.location = "dino.html"
                  }
                  else {
                      alert(result.msg);
                  }
              },
              error: function (xhr, ajaxOptions, thrownError) {
                  alert("Une erreur réseau est survenue");
              }
          });
      });
  }


  function renum(id) {



    var sendrequest = {
        "id": id
    }

    $(function () {
        $.ajax({
            type: 'POST',
            url: "api/renum",
            data: JSON.stringify(sendrequest),
            contentType: "application/json",
            dataType: "json",
            success: function (result) {
                if (result.status == "ok") {
                    var ncomment = '<div class="comment"> <a class="pp-profile"> <img src="./static/data/'+ cpp +'" alt="mdo" width="50" height="50" class="rounded-circle"> </a> <p class="name-comment">' + pseudo + '</p> <p class="text-comment">' + comment.replace("¤", "'") + '</p> <br /></div>'
                    $('#box-chat').append(ncomment);
                    var chatBox = $('#myModal').find('.box-chat');
                    
                    document.getElementById('newcomment').value = ''
                    chatBox.scrollTop(chatBox[0].scrollHeight);
                    

                }
                else {
                    alert(result.msg);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Une erreur réseau est survenue");
            }
        });
    });
}

function denumobj(id) {



  var sendrequest = {
      "id": id
  }

  $(function () {
      $.ajax({
          type: 'POST',
          url: "api/denumobj",
          data: JSON.stringify(sendrequest),
          contentType: "application/json",
          dataType: "json",
          success: function (result) {
              if (result.status == "ok") {
                  var ncomment = '<div class="comment"> <a class="pp-profile"> <img src="./static/data/'+ cpp +'" alt="mdo" width="50" height="50" class="rounded-circle"> </a> <p class="name-comment">' + pseudo + '</p> <p class="text-comment">' + comment.replace("¤", "'") + '</p> <br /></div>'
                  $('#box-chat').append(ncomment);
                  var chatBox = $('#myModal').find('.box-chat');
                  
                  document.getElementById('newcomment').value = ''
                  chatBox.scrollTop(chatBox[0].scrollHeight);
                  

              }
              else if (result.status == "final") {
                window.location = "objet.html"
              }
              else {
                  alert(result.msg);
              }
          },
          error: function (xhr, ajaxOptions, thrownError) {
              alert("Une erreur réseau est survenue");
          }
      });
  });
}


function renumobj(id) {



var sendrequest = {
    "id": id
}

$(function () {
    $.ajax({
        type: 'POST',
        url: "api/renumobj",
        data: JSON.stringify(sendrequest),
        contentType: "application/json",
        dataType: "json",
        success: function (result) {
            if (result.status == "ok") {
                var ncomment = '<div class="comment"> <a class="pp-profile"> <img src="./static/data/'+ cpp +'" alt="mdo" width="50" height="50" class="rounded-circle"> </a> <p class="name-comment">' + pseudo + '</p> <p class="text-comment">' + comment.replace("¤", "'") + '</p> <br /></div>'
                $('#box-chat').append(ncomment);
                var chatBox = $('#myModal').find('.box-chat');
                
                document.getElementById('newcomment').value = ''
                chatBox.scrollTop(chatBox[0].scrollHeight);
                

            }
            else {
                alert(result.msg);
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Une erreur réseau est survenue");
        }
    });
});
}

function denumsch(id) {



  var sendrequest = {
      "id": id
  }

  $(function () {
      $.ajax({
          type: 'POST',
          url: "api/denumsch",
          data: JSON.stringify(sendrequest),
          contentType: "application/json",
          dataType: "json",
          success: function (result) {
              if (result.status == "ok") {
                  var ncomment = '<div class="comment"> <a class="pp-profile"> <img src="./static/data/'+ cpp +'" alt="mdo" width="50" height="50" class="rounded-circle"> </a> <p class="name-comment">' + pseudo + '</p> <p class="text-comment">' + comment.replace("¤", "'") + '</p> <br /></div>'
                  $('#box-chat').append(ncomment);
                  var chatBox = $('#myModal').find('.box-chat');
                  
                  document.getElementById('newcomment').value = ''
                  chatBox.scrollTop(chatBox[0].scrollHeight);
                  

              }
              else if (result.status == "final") {
                window.location = "schema.html"
              }
              else {
                  alert(result.msg);
              }
          },
          error: function (xhr, ajaxOptions, thrownError) {
              alert("Une erreur réseau est survenue");
          }
      });
  });
}


function renumsch(id) {



var sendrequest = {
    "id": id
}

$(function () {
    $.ajax({
        type: 'POST',
        url: "api/renumsch",
        data: JSON.stringify(sendrequest),
        contentType: "application/json",
        dataType: "json",
        success: function (result) {
            if (result.status == "ok") {
                var ncomment = '<div class="comment"> <a class="pp-profile"> <img src="./static/data/'+ cpp +'" alt="mdo" width="50" height="50" class="rounded-circle"> </a> <p class="name-comment">' + pseudo + '</p> <p class="text-comment">' + comment.replace("¤", "'") + '</p> <br /></div>'
                $('#box-chat').append(ncomment);
                var chatBox = $('#myModal').find('.box-chat');
                
                document.getElementById('newcomment').value = ''
                chatBox.scrollTop(chatBox[0].scrollHeight);
                

            }
            else {
                alert(result.msg);
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Une erreur réseau est survenue");
        }
    });
});
}
