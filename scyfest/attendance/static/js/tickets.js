

const nameLabel = document.getElementById("nameLabel");
const nameInput = document.getElementById("nameInput");
const nameLabelText = document.getElementById("nameLabelText");

const editNameIcon = document.getElementById("editNameIcon");

const apiURL = JSON.parse(document.getElementById('js-data').textContent).api_url;
const csrfToken = JSON.parse(document.getElementById('js-data').textContent).csrf;

function initNameChange(e){
    nameInput.value = nameLabelText.textContent;
    nameLabel.style.display = "none";
    nameInput.style.display = "block";
    nameInput.addEventListener("focusout", onNameChanged);
}

function onNameChanged(e){
    nameLabelText.textContent = nameInput.value;
    nameLabel.style.display = "block";
    nameInput.style.display = "none";
    console.log("Ponte que aquí axios hace una petición para cambiar el nombre");
    axios.get(apiURL+nameInput.value).then(function (response) {
        // handle success
        console.log(response);
      })
}

editNameIcon.addEventListener("click", initNameChange);
nameInput.style.display = "none";