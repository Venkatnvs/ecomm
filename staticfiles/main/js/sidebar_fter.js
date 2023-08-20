const cateElement = document.getElementsByClassName("nav_item_cate")
console.log(cateElement)

for(var i=0; i<cateElement.length;i++){
    cateElement[i].addEventListener('dblclick',function(){
        let CategoreUrl = this.dataset.cateurl
        let UrlAction = this.dataset.urlaction
        console.log(CategoreUrl,UrlAction,requestUser)
        if(UrlAction==='new'){
            window.open(CategoreUrl,'_blank')
        }
        else{
            window.open(CategoreUrl,'_self')
        }
    });
}