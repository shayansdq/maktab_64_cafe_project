$('#ms-side-nav > a').click(function(){
    let link = $(this).attr('link')
    console.log(link)
    $.get({
        url: link,
        success: function(data){
            $('.ms-content-wrapper').html(data)
        }
    })
})