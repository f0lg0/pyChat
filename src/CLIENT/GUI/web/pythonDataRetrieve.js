/*
    retreive data from python here
    note all asyn function calls cannot return values, so you need to include a then statement and do something in the then statement,
    if you try and return the value in the then statement it wont work because the data has not arrived yet
*/

async function getUsername(){
    let name = eel.getUsername()();
    return name;
}