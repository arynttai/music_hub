document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.querySelector('.menu');
    var menuOverlay = document.getElementById('menuOverlay');

    menuButton.addEventListener('click', function(event) {
        toggleMenuOverlay(event, menuOverlay);
    });

    document.addEventListener('click', function(event) {
        var isClickInsideMenu = menuOverlay.contains(event.target);
        var isMenuVisible = (menuOverlay.style.display === 'block');

        if (!isClickInsideMenu && isMenuVisible) {
            menuOverlay.style.display = 'none';
        }
    });

    menuOverlay.style.display = 'none';
});

function toggleMenuOverlay(event, menuOverlay) {
    menuOverlay.style.display = (menuOverlay.style.display === 'block') ? 'none' : 'block';
    event.stopPropagation();
}



var items = document.querySelectorAll('.accordion-item');
items.forEach(function(item) {
    var title = item.querySelector('.accordion-title');
    title.addEventListener('click', function() {
        var isActive = item.classList.contains('active');
        items.forEach(function(item) {
            item.classList.remove('active');
        });
        if (!isActive) {
            item.classList.add('active');
        }
    });
});



document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.querySelector('.menu');
    var lmenuOverlay = document.getElementById('lmenuOverlay');

    menuButton.addEventListener('click', function(event) {
        togglelmenuOverlay(event, lmenuOverlay);
    });

    document.addEventListener('click', function(event) {
        var isClickInsideMenu = lmenuOverlay.contains(event.target);
        var isMenuVisible = (lmenuOverlay.style.display === 'block');

        if (!isClickInsideMenu && isMenuVisible) {
            lmenuOverlay.style.display = 'none';
        }
    });

    lmenuOverlay.style.display = 'none';
});

function togglelmenuOverlay(event, lmenuOverlay) {
    lmenuOverlay.style.display = (lmenuOverlay.style.display === 'block') ? 'none' : 'block';
    event.stopPropagation();
}


// Для форм(музыканты и др)

const addAsHiddenInput = (name, value, container) => {
    const newInput = document.createElement('input');

    newInput.type = 'hidden';
    newInput.name = name;
    newInput.value = value;

    container.appendChild(newInput);
}

const createPost = (form) => {
    const formData = new FormData(form);
    const arrayKeys = new Set(["image_urls"])

    let body = {};
    for (let key of formData.keys()) {
        if (arrayKeys.has(key)) {
            body[key] = formData.getAll(key);
        } else {
            body[key] = formData.get(key);
        }
    }

    fetch(form.action, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            form.reset();
        })
        .catch(error => console.log(error));
}

const uploadImages = (form) => {
    fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
    })
        .then(response => response.json())
        .then(data => {
            let { urls } = data;

            hiddenInputsContainer = document.createElement('div');
            hiddenInputsContainer.id = "hiddenInputsContainer";

            for (const url of urls)
                addAsHiddenInput('image_urls', url, hiddenInputsContainer)

            oldHiddenInputsContainer = createPostForm.querySelector('#hiddenInputsContainer')

            if (oldHiddenInputsContainer !== null) {
                createPostForm.removeChild(oldHiddenInputsContainer);
            }

            createPostForm.appendChild(hiddenInputsContainer);

            createPost(createPostForm);
        })
        .catch(error => console.log(error));
}

addEventListener('load', (event) => {
    let uploadImagesForm = document.getElementById('uploadImagesForm');
    let createPostForm = document.getElementById('createPostForm');
    let submitFormsBtn = document.getElementById('submitFormsBtn');

    uploadImagesForm.addEventListener('submit', (event) => {
        event.preventDefault();
        uploadImages(event.currentTarget);
    });

    createPostForm.addEventListener('submit', (event) => {
        event.preventDefault();
        createPost(event.currentTarget);
    });

    submitFormsBtn.addEventListener('click', (event) => {
        uploadImages(uploadImagesForm);
    });
});