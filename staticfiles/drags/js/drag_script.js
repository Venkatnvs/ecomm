let dragValue = null;
let moveElement = false;
let iniX = 0,iniY = 0;
const WrapperElement=document.getElementById('wrapper');
const ContainerElement = document.getElementById('container');
let events = {
    mouse: {
        down:"mousedown",
        move:"mousemove",
        up:"mouseup",
    },
    touch: {
        down:"touchstart",
        move:"touchmove",
        up:"touchend",
    },
}
let deviceType = "";
const isTouchDevice = () => {
    try{
        document.createEvent("TouchEvent");
        deviceType = "touch";
        return true;
    }
    catch(e){
        deviceType = "mouse"
        return false;
    }
};
isTouchDevice();

WrapperElement.addEventListener(events[deviceType].down,(e)=>{
    e.preventDefault();
    iniX = !isTouchDevice() ? e.clientX : e.changedTouches[0].clientX;
    iniY = !isTouchDevice() ? e.clientY : e.changedTouches[0].clientY;
    moveElement = true;
});

WrapperElement.addEventListener(events[deviceType].move,(e)=>{
    if(moveElement){
        e.preventDefault();
        let newX = !isTouchDevice() ? e.clientX : e.changedTouches[0].clientX;
        let newY = !isTouchDevice() ? e.clientY : e.changedTouches[0].clientY;
        posX = WrapperElement.offsetLeft - (iniX - newX) + "px";
        posY = WrapperElement.offsetTop - (iniY - newY)+ "px";
        iniX = newX;
        iniY = newY;
        setposition(posX, posY)
    }
});
WrapperElement.addEventListener(events[deviceType].up,(e)=>{
    moveElement = false;
});
WrapperElement.addEventListener("mouseleave",stopMovement());

function stopMovement(){
    moveElement = false;
}

// WrapperElement.onmousedown = function(){
//     dragValue = WrapperElement;
//     WrapperElement.addEventListener("mousemove",setposition(pageX,pageY));
// }
// document.onmouseup = function(e){
//     WrapperElement.removeEventListener("mousemove", function(){});
// }
// function onDrag(moveX, moveY){
//     let elementposition = window.getComputedStyle(WrapperElement);
//     let left = parseInt(elementposition.left);
//     let top = parseInt(elementposition.top);
//     setposition(left+moveX, top+moveY);
// }

function setposition(x,y){
    WrapperElement.style.left = `${x}`;
    WrapperElement.style.top = `${y}`;
}