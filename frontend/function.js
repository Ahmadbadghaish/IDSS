document.addEventListener('DOMContentLoaded', function () {
    var addBtn = document.getElementById('addBtn');
    var container = document.getElementById('container');
  
    function createSubpage() {
      var subpage = document.createElement('div');
      subpage.classList.add('subpage');
  
      var title = document.createElement('div');
      title.textContent = 'Subpage ' + (container.children.length + 1);
  
      var content = document.createElement('div');
      content.classList.add('content');
      content.textContent = 'Content for the subpage. You can put any information here.';
  
      // New button creation starts here
      var redirectBtn = document.createElement('a'); // Creating an 'a' element for proper semantics
      redirectBtn.textContent = 'Go to page';
      redirectBtn.href = 'http://www.example.com'; // Replace with your URL
      redirectBtn.classList.add('redirectBtn');
      redirectBtn.target = '_blank'; // Optional: Open the link in a new tab
  
      subpage.appendChild(title);
      subpage.appendChild(content);
      subpage.appendChild(redirectBtn); // Append the button to the subpage
  
      title.addEventListener('click', function() {
        // A check to prevent the content box from toggling when the redirect button is clicked
        if (event.target !== redirectBtn) {
          content.style.display = content.style.display === 'block' ? 'none' : 'block';
        }
      });
  
      container.appendChild(subpage);
    }
  
    addBtn.addEventListener('click', createSubpage);
  });
  