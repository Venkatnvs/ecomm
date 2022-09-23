const usernameField=document.querySelector('#inputname');
const emailField=document.querySelector('#inputemail');
const passwordField=document.querySelector('#inputpassword');
const userfeedback=document.querySelector('.invalid-username-feedback');
const emailfeedback=document.querySelector('.invalid-email-feedback');
const usernamesuccess=document.querySelector('.username-success');
const emailsuccess=document.querySelector('.email-success');
const showpassword=document.querySelector('.password-toggle');
const submitbtn=document.querySelector('.submit-btn');

const handleToggle = (e) => {
    if (showpassword.textContent === 'SHOW') {
        showpassword.textContent = 'HIDE';
        passwordField.setAttribute("type","text");
    }else {
        showpassword.textContent = 'SHOW';
        passwordField.setAttribute("type","password");

    }
};

showpassword.addEventListener("click", handleToggle);


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