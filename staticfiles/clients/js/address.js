const cityOpt = document.querySelector('.nvs-city');
const stateOpt = document.querySelector('.nvs-state');

stateOpt.addEventListener('change', (e) => {
    const statevalue = e.target.value;

    if(statevalue.length > 0){
        console.log('data',statevalue);
        fetch("/state-dist",{
            body:JSON.stringify({ searchText : statevalue}),method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log('data',data);
            cityOpt.innerHTML = '';
            if (data[0] === 'not_state'){
                console.log('not',data)
                cityOpt.innerHTML = `
                <option selected >Please select state</option>`;
            }else{
                cityOpt.innerHTML = `
                <option selected >Choose...</option>`;
                data.forEach((item) => {
                    cityOpt.innerHTML +=`
                    <option name='city'>${item}</option>`;
                });
            }
    });
}
});