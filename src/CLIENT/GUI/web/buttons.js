// This Class handles inputs and their corresponding buttons
class Input{
	constructor(input, btn){
		this.input = document.getElementById(input);
		this.btn = document.getElementById(btn);
		
		this.initEventListeners();
	}
	initEventListeners(){
		let obj = this;
		
		this.btn.onclick = function(){
            //check to make sure the msg is not empty first
			if(obj.input.value != "" && obj.input.value != null){
				console.log(obj.input.value);
                writeMsg(obj.input.value, "local");
                eel.exposeSendMsg(obj.input.value)
                
				obj.clear();
			}
		}
		
		//have the enter button get "clicked" when the user presses enter
		this.input.addEventListener("keyup", function(event) {
			if (event.keyCode === 13) {
				event.preventDefault();
				obj.btn.click();
			}
		});
	}
	clear(){
		this.input.value = '';
	}
}