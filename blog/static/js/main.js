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

function submitVote (aid) {
    //use cookie to mutex more than once click
    //submit a vote
    alert('vote OK')
}

window.onload=function () {
    var vote = getByClass('zan_article')[0]
    eventUtil.addHandler(vote, 'click', submitVote)
}