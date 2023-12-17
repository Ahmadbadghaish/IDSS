document.addEventListener('DOMContentLoaded', function () {
  const addBtn = document.querySelector('#addBtn');
  const container = document.querySelector('#container');

  function createSubpage() {
    const subpage = document.createElement('div');
    subpage.classList.add('subpage');

    const title = document.createElement('h2');
    title.textContent = `Subpage ${container.children.length + 1}`;

    const content = document.createElement('p');
    content.textContent = 'Content for the subpage. You can put any information here.';

    const redirectBtn = document.createElement('a');
    redirectBtn.textContent = 'Go to page';
    redirectBtn.href = 'upload.html'; // Update the URL
    redirectBtn.classList.add('redirectBtn');
    redirectBtn.target = '_blank';

    subpage.appendChild(title);
    subpage.appendChild(content);
    subpage.appendChild(redirectBtn);

    title.addEventListener('click', function () {
      content.style.display = content.style.display === 'block' ? 'none' : 'block';
    });

    container.appendChild(subpage);
  }

  addBtn.addEventListener('click', createSubpage);
});
