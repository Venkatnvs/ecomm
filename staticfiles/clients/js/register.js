const usernameField=document.querySelector('#inputname');
const emailField=document.querySelector('#inputemail');
const userfeedback=document.querySelector('.invalid-username-feedback');
const emailfeedback=document.querySelector('.invalid-email-feedback');
const usernamesuccess=document.querySelector('.username-success');
const emailsuccess=document.querySelector('.email-success');
const submitbtn=document.querySelector('.submit-btn');
const password1 = document.querySelector('#inputpassword');
const password2 = document.querySelector('#inputpassword2');
const showpassword1=document.querySelector('.password-toggle');
const showpassword2=document.querySelector('.password-toggle-2');



const handleToggle1 = (e) => {
    if (showpassword1.textContent === 'SHOW') {
        showpassword1.textContent = 'HIDE';
        password1.setAttribute("type","text");
    }else {
        showpassword1.textContent = 'SHOW';
        password1.setAttribute("type","password");

    }
};

const handleToggle2 = (e) => {
    if (showpassword2.textContent === 'SHOW') {
        showpassword2.textContent = 'HIDE';
        password2.setAttribute("type","text");
    }else {
        showpassword2.textContent = 'SHOW';
        password2.setAttribute("type","password");

    }
};



showpassword1.addEventListener("click", handleToggle1);
showpassword2.addEventListener("click", handleToggle2);

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    emailsuccess.textContent=`Checking ${emailVal}`;

    emailField.classList.remove("is-invalid");
    emailfeedback.style.display='none';

    if (emailVal.length > 0) {
        emailsuccess.style.display='block';
        fetch("/auth/validate-email",{
            body:JSON.stringify({ email : emailVal}),method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log('data',data);
            emailsuccess.style.display='none';
            if (data.email_error){
                submitbtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailfeedback.style.display='block';
                emailfeedback.innerHTML=`<p>${data.email_error}</p>`
            }else{
                submitbtn.removeAttribute('disabled');
            }
        });
    }

});



usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    usernamesuccess.textContent=`Checking ${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    userfeedback.style.display='none';

    if (usernameVal.length > 0) {
        usernamesuccess.style.display='block';
        fetch("/auth/validate-username",{
            body:JSON.stringify({ username : usernameVal}),method:"POST",
        }).then(res=>res.json()).then(data=>{
            console.log('data',data);
            usernamesuccess.style.display='none';
            if (data.username_error){
                submitbtn.disabled = true;
                usernameField.classList.add("is-invalid");
                userfeedback.style.display='block';
                userfeedback.innerHTML=`<p>${data.username_error}</p>`
            }else{
                submitbtn.removeAttribute('disabled');
            }
        });
    }
});