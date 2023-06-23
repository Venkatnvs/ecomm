const PinData = document.querySelector('#inputZip');
// const DistOpt = document.querySelector('.nvs-city');

PinData.addEventListener('keyup', (e) => {
    const zipvalue = e.target.value;

    if(zipvalue.length == 6){
        console.log('data',zipvalue);
        fetch("/auth/state-pin",{
            body:JSON.stringify({ zip : zipvalue}),method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log('data',data);
            let data_check = data.data;
            // let data_n = data.dist;
            // let data_low = data_n.toLowerCase();
            // console.log('data',data_low);

            // if(!data_check=="Error"){
            //     let dist_val = DistOpt.value;
            //     let dist = dist_val.toLowerCase();
            //     if(dist == data.data_d.toLowerCase()){
            //         console.log("Success",data.data_d);
            //     }
            //     else{
            //         console.log("Error",false);
            //     }
            // }
        });
    }
});