const defSidebar = document.getElementById("dflt_sidebar-div")
const filterSidebar = document.getElementById("filters_search-div")
const filterBackbtn = document.getElementById("back_defside-search")
const defBackbtn = document.getElementById("search_aside_head-tofilter")
defSidebar.style.display = 'none';

filterBackbtn.onclick = (e)=> {
    filterSidebar.style.display = 'none';
    defSidebar.style.display = 'flex';
}
defBackbtn.onclick = (e) => {
    defSidebar.style.display = 'none';
    filterSidebar.style.display = 'flex';
}