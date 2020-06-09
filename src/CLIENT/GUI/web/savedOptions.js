class SavedOptions{
    constructor(){
        this.savedTheme = "";    
    }
    save(){
        let options = this;
        localStorage.setItem("savedOptions", JSON.stringify(options))    
    }
    load(){
        let loadedData = JSON.parse(localStorage.getItem("savedOptions"));
        if(loadedData != null){
            this.savedTheme = loadedData.savedTheme;
            
            // actully apply the data
            themeChanger.changeTheme(loadedData.savedTheme);
        }else{
            themeChanger.changeTheme("Nord");
        }        
    }
}