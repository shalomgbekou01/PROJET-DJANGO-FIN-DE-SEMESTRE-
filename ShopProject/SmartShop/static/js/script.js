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
    message.style.transition = "all 0.3s"
}, 4000);


// datatable avec jquery

// $(document).ready(function(){
//     $('#table').DataTable({
//         "paging": true,
//         "ordering": true,
//         "searching": true,
//         "info": true,
//         "language": {
//             "zeroRecords": "Aucun résultat trouvé",
//             "pageLength":5,
//             "paginate": {
//                 "first": "Premier",
//                 "last": "Dernier",
//                 "next": ">",
//                 "previous": "<"
//             }
//         },
//         "dom": '<"top"l>rt<"bottom"ip><"clear">'
//     });
// });


function ouvrirModale(id, nom) {
    document.getElementById("list-container").classList.add("list-container::before")
    document.getElementById("modalPanier").style.display = "flex";
    document.getElementById("modalPanier").style.justifyContent = "center";
    document.getElementById("modalPanier").style.alignItems = "center";
    document.getElementById("modalPanier").style.minHeight = "100vh";
    document.getElementById("modalPanier").style.transition = "all 0.3s";
    document.getElementById("prod_id").value = id;
    document.getElementById("nom_produit").innerText = nom;
    document.getElementById("formPanier").action = "/ajouter-au-panier/" + id + "/";
}

function fermerModale() {
    document.getElementById("modalPanier").style.display = "none";
}

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

var elmt = document.getElementById("nav");
var togler = document.getElementById("toggle")
function reduire() {
    elmt.classList.toggle("display")
    elmt.style.transition = "all linear 0.3s"
    togler.classList.toggle("rot")
}