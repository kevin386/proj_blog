function getByClass(clsName,parent){
    var oParent=parent?document.getElementById(parent):document,
        eles=[],
        elements=oParent.getElementsByTagName('*');

    for(var i=0,l=elements.length;i<l;i++){
        if(elements[i].className==clsName){
            eles.push(elements[i]);
        }
    }
    return eles;
}

$(document).ready(function () {
    // body...
    $(".zan_article").click(function () {
        var url = $('#article_vote_url').val();
        $("#vote_article").load(url,function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success"){
                if (responseTxt == 0){
                    $(".prompt_vote").text("您已经赞过了!");
                }
                else{
                    $(".prompt_vote").text("赞成功了!");
                    $(".zan_p2").text(responseTxt);
                }
                var w = ($(window).width() - $(".prompt_vote").width()) / 2;
                //var h = ($(window).height() - $(".prompt_vote").height()) / 2;
                $(".prompt_vote").css("left",w);
                $(".prompt_vote").css("display","block");
                //$(".prompt_vote").css("top",h);
                setTimeout(function(){
                    $(".prompt_vote").fadeOut(3000);
                }, 2000);
            }
            if(statusTxt=="error")
                alert("Error: "+xhr.status+": "+xhr.statusText);
        });
    });
    $("#search_button").mouseenter(function(){
        $("#search_button").css("background-color","#009F00");
    });
    $("#search_button").mouseleave(function(){
        $("#search_button").css("background-color","#5CC26F");
    });
    $(".zan_article").mouseenter(function(){
        $(".zan_article").css("background-color","#009F00");
    });
    $(".zan_article").mouseleave(function(){
        $(".zan_article").css("background-color","#5CC26F");
    });
});

