// When the 'Select Your Daily Mood' button is clicked
document.getElementById('mood-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Stop the page from jumping
    document.getElementById('skip-section').classList.add('d-none'); // Hide the skip section
    document.getElementById('mood-picker').classList.remove('d-none'); // Show the mood picker
    document.getElementById('mood-picker').scrollIntoView({ behavior: 'smooth' }); // Scroll smoothly to the mood picker
});

// When the 'Skip for Now' button is clicked
document.getElementById('skip-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Stop the page from jumping
    document.getElementById('mood-picker').classList.add('d-none'); // Hide the mood picker
    document.getElementById('recommendation').classList.add('d-none'); // Hide the recommendation if open
    document.getElementById('skip-section').classList.remove('d-none'); // Show the skip section
    document.getElementById('skip-section').scrollIntoView({ behavior: 'smooth' }); // Scroll smoothly to the skip section
});

//Keep track of selected mood words
let selectedMoods = [];

// When a mood word button is clicked
document.querySelectorAll('.mood-word').forEach(button => {
    button.addEventListener('click', function() {

        //If already selected, deselect it
        if (this.classList.contains('selected')) {
            this.classList.remove('selected');
            selectedMoods = selectedMoods.filter(mood => mood !== this.dataset.town);
        } else {
            // Only allow up to 3 selections
            if (selectedMoods.length < 3) {
                this.classList.add('selected');
                selectedMoods.push(this.dataset.town);
            }
        }
        // Show or hide the submit button based on whether we have 1-3 mood words selected
        const submitButton = document.getElementById('submit-mood');
        if (selectedMoods.length >= 1 && selectedMoods.length <= 3) {
            submitButton.classList.remove('d-none');
        } else {
            submitButton.classList.add('d-none');
        }
    });
});


// When the submit button is clicked
document.getElementById('submit-mood').addEventListener('click', function() {

    // Count how many times each town was selected
    let townCount = { happy: 0, calm: 0, sad: 0 };
    selectedMoods.forEach(town => townCount[town]++);

    // Find the town with the highest count
    let recommendedTown = Object.keys(townCount).reduce((a, b) => townCount[a] > townCount[b] ? a : b);

    // Set the town name, message and link based on the recommendation
    const towns = {
        happy: { name: '🌞 The Happy Place', url: 'happiness-town.html' },
        calm: { name: '🌸 The Calm-down Corner', url: 'calm-town.html' },
        sad: { name: '🌧 The UP-SAD Down', url: 'sadness-town.html' }
    };

    // Update the recommendation message and button
    const town = towns[recommendedTown];
    document.getElementById('recommendation-message').textContent = `Based on how you're feeling, I think you should visit ${town.name}`;
    document.getElementById('recommended-town-btn').href = town.url;

    // Hide the mood picker and show the recommendation
    document.getElementById('mood-picker').classList.add('d-none');
    document.getElementById('recommendation').classList.remove('d-none');
    document.getElementById('recommendation').scrollIntoView({ behavior: 'smooth' });
});
