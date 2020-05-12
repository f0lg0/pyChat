let clientManager;

// manages the clients connected to the server
class ExternalClientManager{
    constructor(elementToUpdate){
        this.clients = [];
        this.element = elementToUpdate;
    }
    updateClientList(list){
        this.clients = list;  
        document.getElementById(this.element).innerHTML = "* " + list.join("".replace("", "<br />") + "* ");
    }
}
    
