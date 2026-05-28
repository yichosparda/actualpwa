// //this for saving things locally
// document.addEventListener('DOMContentLoaded', () => {

//     // Load notes from localStorage

//     document.querySelectorAll('.day').forEach(day => {

//         const dayTitle = day.querySelector('.daytitle').textContent;

//         const notesField = day.querySelector('.notes');

//         const savedNotes = localStorage.getItem(`notes_${dayTitle}`);

//         if (savedNotes) {

//             notesField.value = savedNotes;

//         }

//     });



//     // Add event listener to the Save Notes button

//     const saveNotesButton = document.querySelector('#save-notes-btn');

//     saveNotesButton.addEventListener('click', () => {

//         document.querySelectorAll('.day').forEach(day => {

//             const dayTitle = day.querySelector('.daytitle').textContent;

//             const notesField = day.querySelector('.notes');

//             localStorage.setItem(`notes_${dayTitle}`, notesField.value);

//         });

//         alert('All notes have been saved!');

//     });



//     console.log('Notes loaded successfully on page load.');

// });

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}
