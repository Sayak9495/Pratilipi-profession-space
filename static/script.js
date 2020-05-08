// function()
// {
//     $.ajax({
//         type: "get",
//         url: "/active_user?company_name="+company_name+"&email="+email,
//         success:function(data)
//         {
//             //console.log the response
//             console.log(company_name);
//         }
//     });
// }

// Set a ttl email in table which gets deleted after 30 seconds, and if the user is still active update ttl to 30

setInterval(function()
{
    $.ajax({
        type: "get",
        url: "/active_user?company_name="+company_name,
        success:function(data)
        {
            //console.log the response
            console.log(company_name);
        }
    });
}, 5000); //5 seconds