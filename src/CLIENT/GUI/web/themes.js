let themeChanger;

class ThemeChanger{
    constructor(){
        this.themes = [];
    }
    saveTheme(name){
        savedOptions.savedTheme = name;
        savedOptions.save();
    }
    //changes GUI theme to the one with 'name' (note: background color is always set to the first in the list)
    changeTheme(name){
        let theme = this.find(name);

        document.body.style.backgroundColor = theme.colors[0];
        document.body.style.color = theme.textColor;
        
        //change themes button dropdown   
        document.getElementById("dropDownTab").style.color = theme.textColor;
        
        //change the button name for dropdown
        document.getElementById("dropDownTab").innerHTML = theme.name + " ▼";

        for(let i = 0; i < theme.colors.length; i++){
            let themeElements = document.getElementsByClassName("colorTheme" + i);

            if(themeElements.length > 0){
                for(let j = 0; j < themeElements.length; j++){
                    themeElements[j].style.backgroundColor = theme.colors[i];
                }
            }
        }

        this.saveTheme(name);
    }
    //returns theme based on name
    find(name){
        for(let i = 0; i < this.themes.length; i++){
            if(this.themes[i].name == name){
                return this.themes[i];
            }
        }
    }
    //add new theme to array
    add(theme){
        this.themes.push(theme);
    }
    
    //adds the html buttons for each theme, so we dont have to keep manually adding them (also fetches any local data)
    initButtons(){     
        for(let i = 0; i < this.themes.length; i++){
            let element = document.createElement("button");
            let themeName = document.createTextNode(this.themes[i].name);
            element.appendChild(themeName);
            element.className = "dropdownButton";
            element.onclick = function(){ themeChanger.changeTheme( themeChanger.themes[i].name ) };
            document.getElementById("themeButtons").appendChild(element);
        }
    }
}

class Theme{
    // colors should be an array with strings of hex values of the colors (dark colors first)
    constructor(name, colors, textColor){
        this.name = name;
        this.colors = colors;
        this.textColor = textColor;
    }
}