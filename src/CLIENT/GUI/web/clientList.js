let clientManager;

// manages the clients connected to the server
class ExternalClientManager{
    constructor(elementToUpdate){
        this.clients = [];
        this.element = elementToUpdate;
    }
    updateClientList(list){
        //clear the list div first
        removeAllChildren(this.element);
        
        //update the list
        this.clients = list;
        
        //add through textnodes so that you can asign a class to the individual elements
        for(let i = 0; i < this.clients.length; i++){
            let client = document.createElement("p");
            let textNode = document.createTextNode(this.clients[i]);
            
            client.className = "blockListItem";
            client.appendChild(textNode);
            document.getElementById(this.element).appendChild(client);
        }
        this.updateClientNumberLabel();
    }
    updateClientNumberLabel(){
        document.getElementById("clientNumber").innerHTML = "Online (" + (this.clients.length+1) + ")";    
    }
}
    
