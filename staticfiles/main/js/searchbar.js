const searchReDiv = document.getElementById("search-nvsdiv");
const searchHmInp = document.getElementById("search_inp_hm");
const searchRsUl = document.getElementById("search-rs-ul");
const searchForm = document.getElementById("search-form-hm");
searchReDiv.style.display = "none";

searchHmInp.addEventListener("keyup", (e) => {
  const searchvalue = e.target.value;

  if (searchvalue != "") {
    console.log("data", searchvalue);
    var SendData = {
      stext: searchvalue,
    };
    var apiUrl = "/search/s/";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", apiUrl, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);
        searchReDiv.style.display = "flex";
        AddSearchli(response.data);
      }
    };
    xhr.send(JSON.stringify(SendData));
  }
  else{
    searchRsUl.innerHTML = "";
    searchReDiv.style.display = "none";
  }
});


function AddSearchli(data){
  searchRsUl.innerHTML = "";
  current_url = `${window.location.protocol}//${window.location.host}`
  data.forEach(cnt=> {
    let s_slug;
    if(cnt.type == "cate"){
      s_slug = `sd/c/${cnt.slug}`
    }
    else if(cnt.type == "prod"){
      s_slug = `product/${cnt.slug}`
    }
    else if(cnt.type == 'subcate'){
      s_slug = `sd/s/${cnt.slug}`
    }
    searchRsUl.innerHTML += `<li class="search-rs-li list-group-item">
          <a href="${current_url}/${s_slug}">
            <div class="search-rs-div">
              <img src="${cnt.image}"
              alt="productimg">
              <div class="search-rs-div-cnt">
                <span>${cnt.name}</span>
              </div>
            </div>
          </a>
        </li>`;
  });
}

window.addEventListener('mouseup',function(event){
  if(event.target != searchReDiv && event.target.parentNode != searchReDiv){
    searchReDiv.style.display = 'none';
    // try {
    //   adddlert("Welcome guest!");
    // }
    // catch(err) {
    //   document.getElementById("demo").innerHTML = err.message;
    // }
    // const UserSQuery = JSON.parse(document.getElementById('user_squery').textContent);
    // if(UserSQuery != searchHmInp.value){
    //   searchHmInp.value="";
    // }
  }
}) 

searchForm.onsubmit = (e) => {
  searchForm.submit();
}