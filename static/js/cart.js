var UpdateBtns = document.getElementsByClassName('update-cart')

for (var i=0; i < UpdateBtns.length; i++){
	UpdateBtns[i].addEventListener('click',function(){
		var productId = this.dataset.product
		var action= this.dataset.action
		console.log('productid:',productId, 'action:', action)

		console.log('user:',user)
		if(user === AnonymousUser){
			console.log('not logged in')
		}
		else{
			UpdateUserOrder(productId,action)
		}
	})
}

function UpdateUserOrder(productId,action){
    console.log('logged in')

    var url = 'update_item/'
    fetch(url, {
        method:POST,
        headers:{
            'Content-Type':'application/json'     
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json();
     })

     .then((data) => {
        console.log('Data:', data)
    });
}