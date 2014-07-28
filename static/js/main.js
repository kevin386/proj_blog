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
                $(".zan_p2").text(responseTxt)
                alert('vote success');
            }
            if(statusTxt=="error")
                alert("Error: "+xhr.status+": "+xhr.statusText);
        });
    });
});