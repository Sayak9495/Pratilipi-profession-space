document.addEventListener('DOMContentLoaded', function() 
{
    const Http = new XMLHttpRequest();
    const url="/active_user?company_name="+company_name;
    Http.open("GET", url);
    Http.send();
});

// In comany db, every 10 second older data(older than 10sec) will be deleted (ttl simulation, aersopike bettwe option).
// and this function keeps the timestamp updated, if user is active. 

setInterval(function()
{
    $.ajax({
        type: "get",
        url: "/active_user?company_name="+company_name,
        success:function(data)
        {
            console.log(company_name);
        }
    });
}, 5000); //5 seconds