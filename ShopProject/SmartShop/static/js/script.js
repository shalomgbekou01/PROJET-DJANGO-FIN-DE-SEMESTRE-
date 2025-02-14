var error = document.querySelector(".error")


// erreur de remplissage des champs
if(error){
    if(error.previousElementSibling.firstElementChild){
        error.previousElementSibling.firstElementChild.nextElementSibling.classList.add("input-error")
    }
    else{
        error.previousElementSibling.classList.add("input-error")
    }
}

// gestion des messages
var message = document.querySelector('.alert')

setTimeout(() => {
    message.style.display = "none";
}, 3000);