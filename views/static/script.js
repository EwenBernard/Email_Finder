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
            
            if (bestMatch === null && remainingData === null) {
                // No best match but some related results, display related results
                displayNoContactFoundMessage();
            } else if (bestMatch === null && remainingData.length > 0) {
                // No contact found, display EPS file and message
                displayNoContactFoundMessage();
                displayRelatedResults(remainingData);
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

    var resultContainer = document.querySelector('.result-container');

    // Clear the content of resultContainer
    resultContainer.innerHTML = '';

    // Create the main contact div
    var contactDiv = document.createElement('div');
    contactDiv.classList.add('contact');

    // Create the contact photo div
    var contactPhotoDiv = document.createElement('div');
    contactPhotoDiv.classList.add('contact-photo');
    var initials = bestMatch.name.charAt(0).toUpperCase() + bestMatch.last_name.charAt(0).toUpperCase();
    contactPhotoDiv.textContent = initials;

    // Create the contact info div
    var contactInfoDiv = document.createElement('div');
    contactInfoDiv.classList.add('contact-info');

    // Create and append the <p> elements for name, email, and company
    var nameParagraph = document.createElement('p');
    nameParagraph.textContent = bestMatch.name + ' ' + bestMatch.last_name;
    contactInfoDiv.appendChild(nameParagraph);

    var emailParagraph = document.createElement('p');
    emailParagraph.textContent = bestMatch.email;
    contactInfoDiv.appendChild(emailParagraph);

    var companyParagraph = document.createElement('p');
    companyParagraph.textContent = bestMatch.company;
    contactInfoDiv.appendChild(companyParagraph);

    // Create the confidence tag div
    var confidenceTagDiv = document.createElement('div');
    confidenceTagDiv.classList.add('confidence-tag');

    // Create and append the confidence tag content
    var tagSpan = document.createElement('span');
    tagSpan.classList.add('tag', 'tag--success');
    tagSpan.dataset.controller = 'tooltip';
    tagSpan.title = 'Confidence';

    var svgIcon = document.createElement('svg');
    svgIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svgIcon.setAttribute('width', '11');
    svgIcon.setAttribute('height', '11');
    svgIcon.setAttribute('fill', 'currentColor');
    svgIcon.setAttribute('class', 'bi bi-shield-fill-check');
    svgIcon.setAttribute('viewBox', '0 0 16 16');
    svgIcon.setAttribute('id', 'tag-icon');

    var path = document.createElement('path');
    path.setAttribute('fill-rule', 'evenodd');
    path.setAttribute('d', "M8 0c-.69 0-1.843.265-2.928.56-1.11.3-2.229.655-2.887.87a1.54 1.54 0 0 0-1.044 1.262c-.596 4.477.787 7.795 2.465 9.99a11.777 11.777 0 0 0 2.517 2.453c.386.273.744.482 1.048.625.28.132.581.24.829.24s.548-.108.829-.24a7.159 7.159 0 0 0 1.048-.625 11.775 11.775 0 0 0 2.517-2.453c1.678-2.195 3.061-5.513 2.465-9.99a1.541 1.541 0 0 0-1.044-1.263 62.467 62.467 0 0 0-2.887-.87C9.843.266 8.69 0 8 0m2.146 5.146a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647z");

    svgIcon.appendChild(path);
    tagSpan.appendChild(svgIcon);

    var tagLabelSpan = document.createElement('span');
    tagLabelSpan.classList.add('tag_label');
    var confidenceValue = document.createElement('b');
    confidenceValue.textContent = bestMatch.confidence + '%';
    tagLabelSpan.appendChild(confidenceValue);

    tagSpan.appendChild(tagLabelSpan);
    confidenceTagDiv.appendChild(tagSpan);

    // Create the source list div
    var sourceListDiv = document.createElement('div');
    sourceListDiv.classList.add('source-list');

    // Create and append the <p> element for sources
    var sourceListParagraph = document.createElement('p');
    if (bestMatch.source && typeof bestMatch.source === 'string' && bestMatch.source.trim() !== '') {
        sourceListParagraph.textContent = 'Sources where we found the email address on the web:';

        // Create and append the <ul> element
        var sourceListUl = document.createElement('ul');

        // Create and append the <li> element for the source
        var listItem = document.createElement('li');
        listItem.textContent = bestMatch.source;
        sourceListUl.appendChild(listItem);

        sourceListDiv.appendChild(sourceListParagraph);
        sourceListDiv.appendChild(sourceListUl);
    } else {
        sourceListParagraph.textContent = 'No sources found for email on the web';
        sourceListDiv.appendChild(sourceListParagraph);
    }

    // Append all the created elements to the main contact div
    contactDiv.appendChild(contactPhotoDiv);
    contactDiv.appendChild(contactInfoDiv);
    contactDiv.appendChild(confidenceTagDiv);
    console.log("contactDiv", contactDiv)

    // Append the main contact div to the document body or a specific container
    resultContainer.appendChild(contactDiv);

    var resultDividerHr = document.createElement('hr');
    resultDividerHr.classList.add('result-divider');
    resultContainer.appendChild(resultDividerHr);

    // Append the source list div to the document body or a specific container
    resultContainer.appendChild(sourceListDiv);
    console.log(resultContainer)
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