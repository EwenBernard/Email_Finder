document.addEventListener('DOMContentLoaded', function () {
    var formContainer = document.getElementById('emailForm');
    var resultContainer = document.getElementById('resultContainer');
    var resultListComponent = document.querySelector('.result-list-container');

    formContainer.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        var formData = new FormData(formContainer);

        fetch('/add', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Form submitted successfully:', data);

            var bestMatch = data.matched_result;
            var remainingData = data.remaining_data;

            if (bestMatch === null && remainingData.length > 0) {
                // No best match but some related results, display related results
                displayNoContactFoundMessage();
                displayRelatedResults(remainingData);
            } else if (bestMatch === null && remainingData === null) {
                // No contact found, display EPS file and message
                displayNoContactFoundMessage();
            } else {
                // Contact found, update the content of the result container
                displayBestMatch(bestMatch);
                displayRelatedResults(remainingData);
            }

            // Check if the result container is already visible
            if (resultContainer.classList.contains('show')) {
                return; // If visible, do nothing
            }

            // Add the class to initiate the transition
            var formContainer = document.getElementById('formContainer');
            formContainer.classList.add('slide-up');

            // Transition delay 1st container
            setTimeout(function () {
                resultContainer.classList.add('show');
            }, 100);
            // Transition delay 2nd container
            setTimeout(function () {
                resultListComponent.classList.add('show');
            }, 300);
        })
        .catch(error => {
            console.error('Error submitting form:', error);
        });
    });
});


function displayNoContactFoundMessage() {
    // Display EPS file and message for no contact found
    var resultContainer = document.querySelector('.result-container');

    resultContainer.innerHTML = `<p>Ooooops no contact found matching your search, check related results</p>`;

    //var epsImage = new Image();
    //epsImage.src = "http://127.0.0.1:8001/static/images/sad_emote.eps";
    //epsImage.alt = 'EPS File';
    //resultContainer.appendChild(epsImage);
}

function displayBestMatch(bestMatch) {
    // Update the content of the result container with the best match data
    var contactInfo = document.querySelector('.contact-info');
    contactInfo.querySelector('p:nth-child(1)').textContent = bestMatch.name + ' ' + bestMatch.last_name;
    contactInfo.querySelector('p:nth-child(2)').textContent = bestMatch.email;
    contactInfo.querySelector('p:nth-child(3)').textContent = bestMatch.company;

    var contactPhoto = document.querySelector('.contact-photo');
    var initials = bestMatch.name.charAt(0).toUpperCase() + bestMatch.last_name.charAt(0).toUpperCase();
    contactPhoto.textContent = initials;

    // Update the confidence tag
    var confidenceTag = document.querySelector('.confidence-tag');
    confidenceTag.querySelector('.tag_label b').textContent = bestMatch.confidence + '%';

    var sourceList = document.querySelector('.source-list');
    var sourceListItems = sourceList.querySelector('ul');
    var sourceListParagraph = document.querySelector('.source-list p');

    if (bestMatch.source && typeof bestMatch.source === 'string' && bestMatch.source.trim() !== '') {
        // Display the message for sources found
        sourceListParagraph.textContent = 'Sources where we found the email address on the web:';
    
        // Clear existing list items
        sourceListItems.innerHTML = '';
    
        // Add new list item for the source
        var listItem = document.createElement('li');
        listItem.textContent = bestMatch.source;
        sourceListItems.appendChild(listItem);
    } else {
        // Display the message for no sources found
        sourceListParagraph.textContent = 'No sources found for email on the web';
        sourceListItems.innerHTML = '';
    }
}

function displayRelatedResults(remainingData) {
    
    // Create related results list
    var resultListContainer = document.querySelector('.result-list-container');
    var resultList = resultListContainer ? resultListContainer.querySelector('ul') : null;

    console.log('resultListContainer:', resultListContainer);
    console.log('resultList:', resultList);
    resultList.innerHTML = '';

    remainingData.forEach(user => {
        var listItem = document.createElement('li');
        var initials = user.name.charAt(0).toUpperCase() + user.last_name.charAt(0).toUpperCase();
        listItem.innerHTML = `<div class="li-result-wrapper">
                                <div class="related-contact-photo">${initials}</div>
                                <div class="related_result_container">
                                    <p class="result-list-name">${user.name} ${user.last_name}</p>
                                    <p class="result-list-email">${user.email}</p>
                                    <p class="result-list-company">${user.company}</p>
                                </div>
                                <div class="confidence-tag-result-list">
                                    <span class="tag tag--success" data-controller="tooltip" title="Confidence">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" fill="currentColor" class="bi bi-shield-fill-check" viewBox="0 0 16 16" id="tag-icon">
                                            <path fill-rule="evenodd" d="M8 0c-.69 0-1.843.265-2.928.56-1.11.3-2.229.655-2.887.87a1.54 1.54 0 0 0-1.044 1.262c-.596 4.477.787 7.795 2.465 9.99a11.777 11.777 0 0 0 2.517 2.453c.386.273.744.482 1.048.625.28.132.581.24.829.24s.548-.108.829-.24a7.159 7.159 0 0 0 1.048-.625 11.775 11.775 0 0 0 2.517-2.453c1.678-2.195 3.061-5.513 2.465-9.99a1.541 1.541 0 0 0-1.044-1.263 62.467 62.467 0 0 0-2.887-.87C9.843.266 8.69 0 8 0m2.146 5.146a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647z"/>
                                        </svg>
                                        <span class="tag_label"><b>${user.confidence}%</b></span>
                                    </span>
                                </div>
                             </div>`;
        resultList.appendChild(listItem);
    });
}