var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action //action=行動
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        if (user === 'AnonymousUser') {
            alert('你沒有註冊，無法通過!') //告訴我說為匿名用戶，是就退出!!!!
            addCookieItem(productId, action) //添加Cookie項目
            // cartNumbers(productId, action)// 說出該用戶為匿名用戶嗎?然後退出該用戶
        } else {
            updateUserOrder(productId, action) //更新用戶訂單//已通過身分用戶
        }
    })
}

function updateUserOrder(productId, action) { //更新用戶訂單
    console.log('User is authenticated, sending data.../ 用戶已通過身份驗證，正在發送數據...')

    var url = '/store/update_item/'    // #https://www.oxxostudio.tw/articles/201908/js-fetch.html

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('data: ', data)
            location.reload()   //#https://dragonspring.pixnet.net/blog/post/33052894
        });
}


// function cartNumbers() {
//     let productNumbers = localStorage.getItem('cartNumbers');
//     productNumbers = parseInt(cartNumbers);
//     if (productNumbers) {
//         localStorage.setItem('cartNumbers', productNumbers + 1);
//         document.querySelector('#cart-total').textContent = productNumbers + 1
//
//     }else{
//         localStorage.setItem('cartNumbers', 1);
//         document.querySelector('#cart-total').textContent = 1
//     }
//
//     console.log('CART:', cart)
//     document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
//
//     location.reload()
// }


function addCookieItem(productId, action) {
    console.log('User is not authenticated/用戶未通過身份驗證')

    if (action === 'add') {
        // if (cart[productId] === undefined) {
        //     cart[productId] = {'quantity': 1}
        // } else {
        cart[productId]['quantity'] += 1
        // }
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted/項目應刪除')
            delete cart[productId];
        }
    }
    console.log('CART:', cart)
    // document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    // location.reload()
}