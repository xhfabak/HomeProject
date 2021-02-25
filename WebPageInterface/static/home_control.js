"use strict;"
$(document).ready(function () {
        $("button_away").click(run_away);
        }
}

function run_away()
{
    $.post({
                url: "./rekuperatorius/control/away",
                data: "",
                success: function( data ) {
                    alert( "Load was performed." );
                    console.log(data);
                },
            });
}