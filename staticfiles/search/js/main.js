const defSidebar = document.getElementById("dflt_sidebar-div")
const filterSidebar = document.getElementById("filters_search-div")
const filterBackbtn = document.getElementById("back_defside-search")
const defBackbtn = document.getElementById("search_aside_head-tofilter")
const priceGoBtn = document.getElementById("pricerng_gobtn")
const priceMinInp = document.getElementById("rpricemin-inp")
const priceMaxInp = document.getElementById("rpricemax-inp")
const avaStockCheck = document.getElementById("avaliable_stock_inp")
const UserSQuery = JSON.parse(document.getElementById('user_squery').textContent);
defSidebar.style.display = 'none';

avaStockCheck.onchange = (e) => {
    if(avaStockCheck.checked){
        avacheck = 'yes'
    }
    else{
        avacheck = 'no'
    }
    url = `${window.location.pathname}?squery=${UserfilterEr(UserSQuery.squery)}&rpricemax=${UserfilterEr(UserSQuery.rpricemax)}&rpricemin=${UserfilterEr(UserSQuery.rpricemin)}&discountper=${UserfilterEr(UserSQuery.discountper)}&stockava=${avacheck}&sort=${UserfilterEr(UserSQuery.sort)}`
    window.open(url,'_self')
}

filterBackbtn.onclick = (e)=> {
    filterSidebar.style.display = 'none';
    defSidebar.style.display = 'flex';
}
defBackbtn.onclick = (e) => {
    defSidebar.style.display = 'none';
    filterSidebar.style.display = 'flex';
}
priceGoBtn.onclick = (e) => {
    url = `${window.location.pathname}?squery=${UserfilterEr(UserSQuery.squery)}&rpricemax=${priceMaxInp.value}&rpricemin=${priceMinInp.value}&discountper=${UserfilterEr(UserSQuery.discountper)}&stockava=${UserfilterEr(UserSQuery.stockava)}&sort=${UserfilterEr(UserSQuery.sort)}`
    window.open(url,'_self')
}

function UserfilterEr(user_query){
    let filter = user_query
    if(!filter){
        filter = ""
    }
    return filter
}