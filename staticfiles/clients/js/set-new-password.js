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