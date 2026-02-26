// When the 'Select Your Daily Mood' button is clicked
document.getElementById('mood-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Stop the page from jumping
    document.getElementById('mood-picker').classList.remove('d-none'); // Show the mood picker
    document.getElementById('mood-picker').scrollIntoView({ behavior: 'smooth' }); // Scroll smoothly to the mood picker
});

// When the 'Skip for Now' button is clicked
document.getElementById('skip-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Stop the page from jumping
    document.getElementById('mood-picker').classList.add('d-none'); // Hide the mood picker
    document.getElementById('skip-section').classList.remove('d-none'); // Show the skip section
    document.getElementById('skip-section').scrollIntoView({ behavior: 'smooth' }); // Scroll smoothlyto the skip section
});