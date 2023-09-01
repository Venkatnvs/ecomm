document.getElementById("coupon_sbt").addEventListener("click", function (e) {
  e.preventDefault();
  CouponBeforeCheck(document.getElementById("coupon_get").value,"add")
});

function CouponBeforeCheck(value,action){
  if (value == "") {
    alert("Enter coupon code before apply");
    return;
  }
  MakeCouponRequest(value,action)
  document.getElementById("invalid-coupon-feedback").style.display = 'none';
}


function MakeCouponRequest(coupon,action){
  var SendData = {
    coupon: coupon,
    action:action
  };
  var apiUrl = "/order/coupon-code/";
  var xhr = new XMLHttpRequest();
  xhr.open("POST", apiUrl, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      console.log(response);
      UpdateTotal()
      if (response.typestatus) {
        if(response.message.action == "add"){
          CouponApply(response)
        }
        else{
          document.getElementById("coupon_get_form").classList.remove("hidden_c");
          document.getElementById("coupon_code_show").classList.add("hidden_c");
        }
      }
      else{
        document.getElementById("invalid-coupon-feedback").style.display = 'block';
      }
    }
  };
  xhr.send(JSON.stringify(SendData));
}

function CouponApply(response){
  document.getElementById("coupon_get_form").classList.add("hidden_c");
  document.getElementById("coupon_code_show")
    .innerHTML = `<p class="text-900 fw-semi-bold">Coupon:&nbsp;<span class="fw-bold">${response.message.code}</span></p>
            <div class="d-flex align-items-baseline"><p class="text-1100 fw-semi-bold text-danger">-₹${response.message.discount}  </p>
            <input id="temp_coupon_code" type="text" type="hidden" value="${response.message.code}" hidden>
            <a style="cursor: pointer;" id="coupon_rem" herf="#"><i class="bi bi-trash3-fill d-inline-flex mx-1"></i></a></div>`;
  document.getElementById("coupon_code_show").classList.remove("hidden_c");
  document.getElementById("coupon_rem").addEventListener("click",function(e){
    e.preventDefault()
    CouponBeforeCheck(document.getElementById("temp_coupon_code").value,"remove")
  })
}

function UpdateTotal(){
  var apiUrl = "/order/cart-bill-total/";
  var xhr = new XMLHttpRequest();
  xhr.open("GET", apiUrl, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      console.log(response);
      if (response.typestatus) {
        document.getElementById("cart_bill_total").innerText = `₹${response.message.total}`
        document.getElementById("cart_pay_total").innerText = `₹${response.message.total}`
      }
      else{
        alert("some thing went wrong!Try again later")
      }
    }
  };
  xhr.send();
}
window.onload = () =>{
  var apiUrl = "/order/coupon-order-st/";
  var xhr = new XMLHttpRequest();
  xhr.open("GET", apiUrl, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      console.log(response);
      if (response.typestatus) {
        if(response.coupon_st){
          CouponApply(response)
        }
      }
      else{
        alert("some thing went wrong!Try again later")
      }
    }
  };
  xhr.send();
}
document.getElementById("payment_type_check").addEventListener("change",function(e){
  console.log(document.getElementById("payment_type_check").value)
  if(document.getElementById("payment_type_check").value != "cod"){
    document.getElementById("make_pay_btn").classList.add("disabled")
    document.getElementById("invalid-payment-feedback").style.display = "block"
  }else{
    document.getElementById("make_pay_btn").classList.remove("disabled")
    document.getElementById("invalid-payment-feedback").style.display = "none"
  }
})