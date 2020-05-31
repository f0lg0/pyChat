let themeChanger;

class ThemeChanger{
    constructor(){
        this.themes = [];
    }
    //changes GUI theme to the one with 'name' (note: background color is always set to the first in the list)
    changeTheme(name){
        let theme = this.find(name);
        
        document.body.style.backgroundColor = theme.colors[0];
        document.body.style.color = theme.textColor;
        
        for(let i = 0; i < theme.colors.length; i++){
            let themeElements = document.getElementsByClassName("colorTheme" + i);
            
            if(themeElements.length > 0){
                for(let j = 0; j < themeElements.length; j++){
                    themeElements[j].style.backgroundColor = theme.colors[i];
                }    
            }  
        }
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
}

class Theme{
    // colors should be an array with strings of hex values of the colors (dark colors first)
    constructor(name, colors, textColor){
        this.name = name;
        this.colors = colors;
        this.textColor = textColor;
    }
}