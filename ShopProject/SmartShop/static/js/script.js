var error = document.querySelector(".error");


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
var message = document.getElementById("alert");

setTimeout(() => {
    message.style.opacity = "0"
    message.style.transition = "all 0.3s ease"
    setTimeout(() => {
        message.style.display = "none"
    }, 300);
}, 4000);





// génération de la facture en pdf
function imprimer(name) {
    const element = document.getElementById("facture");

    html2pdf(element, {
        margin:10,
        filename: name + ".pdf",
        image:{type: 'png', quality:0.98},
        html2canvas : {scale: 2},
        jsPDF : {format: 'a4', orientation: 'portrait' }
    });
}

/* responsivité bar de navigation*/

var elmt = document.getElementById("nav");
var togler = document.getElementById("toggle")
function reduire() {
    elmt.classList.toggle("display")
    elmt.style.transition = "all 0.3s ease"
    togler.classList.toggle("rot")
}

 /* vérifier panier */
 function verifier(statut) {
    if(statut == "validé"){
        return confirm("êtes-vous sûr de vouloir valider ce panier ?")
    }else{
        return confirm("Attention ! ce panier n'est pas encore validé. voulez-vous le supprimer ?")
    }
 }



