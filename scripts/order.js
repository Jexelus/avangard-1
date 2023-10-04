var modal = document.querySelector(".modal");
var trigger = document.querySelector(".trigger");
var closeButton = document.querySelector(".close-button");

function toggleModal() {
    modal.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modal) {
        toggleModal();
    }
}

trigger.addEventListener("click", toggleModal);
closeButton.addEventListener("click", toggleModal);
window.addEventListener("click", windowOnClick);

// async function send_messege_to_handler(){
//     let formData = new FormData(document.getElementById('data-to-send'));
//     let response = await fetch('http://localhost:9999/send_message', {
//         mode: 'no-cors',
//         method: 'POST',
//         body: formData
//       });

//     let result = await response
// }

function send_message(){
    let formData = new FormData(document.getElementById('data-to-send'));
    fetch('http://localhost:9999/send_message', {
        mode: 'no-cors',
        method: 'POST',
        body: formData
    }).then ((response)=>{
        window.location.href = 'thanks.html';
    });
}