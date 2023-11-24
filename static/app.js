console.log("JS Init");

// Event delegation for dynamically added elements
$(document).on('click', '.del-fb', deleteFb);
$(document).on('click', '.edit-fb', editFb);
$(document).on('click', '.submit-fb', submitFb);

async function deleteFb() {
    const id = $(this).data('id');
    await axios.delete(`/feedback/${id}/update`);
    alert("DELETED");
}

async function editFb(event) {
    event.preventDefault();

    const id = $(this).data('id');
    const user = $(this).data('user');
    if(!user){
        console.log("NO USER FOUND");
    }
    var feedbackContainer = $(this).closest('.feedback-container');

    // Find the h6 and p elements within the feedback container
    var titleElement = feedbackContainer.find('h6');
    var contentElement = feedbackContainer.find('p');

    // Retrieve the original title and content from data attributes
    var originalTitle = titleElement.html();
    var originalContent = contentElement.html();
    console.log("Retrieved all elements");
    // Replace the h4 and p elements with input fields and pre-fill with original data
    titleElement.replaceWith('<input type="text" class="edit-title" value="' + originalTitle + '">');
    contentElement.replaceWith('<textarea class="edit-content">' + originalContent + '</textarea>');
    console.log("Replaced elements");
    // Toggle visibility of buttons
    feedbackContainer.find('.edit-fb').hide();
    feedbackContainer.find('.submit-fb').show();
    console.log("Toggled Visibility");
}

async function submitFb() {
    const id = $(this).data('id');
    const user = $(this).data('user');
    console.log("log ", $(this).data('user'));
    var feedbackContainer = $(this).closest('.feedback-container');

    // Find the input and textarea elements within the feedback container
    var titleInput = feedbackContainer.find('.edit-title');
    var contentTextarea = feedbackContainer.find('.edit-content');

    // Retrieve the edited title and content from the input fields
    var editedTitle = titleInput.val();
    var editedContent = contentTextarea.val();

    // Make an Axios request to delete the current feedback
    await axios.delete(`/feedback/${id}/update`);

    // Make an Axios request to add the updated feedback
    console.log(`/users/${user}/feedback/add`);
    await axios.post(`/users/${user}/feedback/add`, {
        title: editedTitle,
        content: editedContent
    });

    // Replace the input fields with h6 and p elements and update data attributes
    titleInput.replaceWith('<h6 data-original-title="' + editedTitle + '">' + editedTitle + '</h6>');
    contentTextarea.replaceWith('<p data-original-content="' + editedContent + '">' + editedContent + '</p>');

    // Toggle visibility of buttons
    feedbackContainer.find('.edit-fb').show();
    feedbackContainer.find('.submit-fb').hide();

    alert("FEEDBACK UPDATED");
}
