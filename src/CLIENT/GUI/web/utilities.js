//removes all children from the container parameter
function removeAllChildren(container){
    let element = document.querySelector("#" + container);
    
    let child = element.lastElementChild;
    while(child){
        element.removeChild(child);
        child = element.lastElementChild;
    }
}
