function checkprofile(name) {
    alert(name)
        var sendrequest = {
            "name": name
        }

        $(function () {

            $.ajax({
                type: 'POST',
                url: "api/checkprofile",
                data: JSON.stringify(sendrequest),
                contentType: "application/json",
                dataType: "json",
                success: function (result) {

                    if (result.status == "ok") {
                        alert('oui')
                        window.location = 'otherprofile.html'
                    }
                    else {


                        //alert(result.msg);

                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    alert("Une erreur réseau est survenue");
                }
            });
        });
}




