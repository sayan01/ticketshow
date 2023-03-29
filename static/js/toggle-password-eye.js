showpass = document.querySelector('#showpass');
password = document.querySelector('#password');
eye = document.querySelector('#eye')
showpass.addEventListener('change', ()=>{
    eye.classList.toggle('fa-eye-slash')
    eye.classList.toggle('fa-eye')
    if(showpass.checked)
        password.type = "text"
    else
        password.type = "password"
});