const cartElement = document.getElementsByClassName('nvs_addcart_card-button_js')

for(var i=0; i<cartElement.length;i++){
    cartElement[i].addEventListener('click',function(){
        let productid = this.dataset.product
        let action = this.dataset.action
        console.log(productid,action,requestUser)
        if(requestUser==='AnonymousUser'){
            console.log("not logined")
            addOrderCookie(productid,action)
        }
        else{
            UpdateCart(productid,action)
        }
    });
}

function UpdateCart(productid,action){
    var SendData = {
        productid : productid,
        action:action
    }
    var apiUrl = '/order/update-cart';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response.message)
        location.reload()
        }
    };
    xhr.send(JSON.stringify(SendData));
}

function addOrderCookie(productid,action){
    if (action == 'add'){
		if (cart[productid] == undefined){
		cart[productid] = {'quantity':1}

		}else{
			cart[productid]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productid]['quantity'] -= 1

		if (cart[productid]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productid];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}