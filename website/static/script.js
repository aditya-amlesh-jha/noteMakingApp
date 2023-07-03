function displayErrorMessage(message) {
    const warningMessage = document.getElementById("warningMessage");
    warningMessage.textContent = message;
    const modal = new bootstrap.Modal(document.getElementById("warningModal"));
    modal.show();
}


validateEmail = (email)=> {
    if (!/\S+@\S+\.\S+/.test(email)) {
        displayErrorMessage("Invalid email format.");
        return false;
    }
    return true;
}

validatePassword = (password) => {
    if (password.length < 8) {
        displayErrorMessage("Invalid password. It should be at least 8 characters long.");
        return false;
    }
    return true;
}

validateName = (name) => {
    if (!/^[A-Za-z ]+$/.test(name)) {
        displayErrorMessage("Invalid name. Only letters are allowed.");
        return false;
    }
    return true;
}

validateLength = (value, length, message) => {
    if (value.length != length) {
        displayErrorMessage(`Invalid ${message} number. It should be ${length} digits.`);
        return false;
    }
    return true;
}

sendData = (api,data)=>{
    return fetch('/'+api,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    })
}


function validateForm(e) {

    e.preventDefault();
  
    const name = document.getElementById("name-input").value;
    const aadhar = document.getElementById("aadhar-input").value;
    const phone = document.getElementById("phone-input").value;
    const email = document.getElementById("email-input").value;
    const password = document.getElementById("password-input").value;

  
    // If all validations pass, send the form data to the Flask API


    if (!validateName(name)) {
        return;
    }

    if (!validateLength(aadhar, 12, "Aadhar") || !validateLength(phone, 10, "Phone")) {
        return;
    }

    if (!validateEmail(email)) {
        return;
    }

    if (!validatePassword(password)) {
        return;
    }


    const formData = {
      name: name,
      email: email,
      phone: phone,
      aadhar: aadhar,
      password: password
    };

    // if sendData is successful, then user is created and redirected to login page
    sendData("signup",formData)
    .then((response) => {
        console.log(response);
        if (response.ok) {
            window.location.href = "/login";
        } else {
            response.text().then((text) => {
                displayErrorMessage(text);
            })
        }
    }).catch((err) => {
        console.log(err);
        displayErrorMessage("Something went wrong.");
    })
}
  
validateLogin = (e) => {
    e.preventDefault();
    const email = document.getElementById("email-input").value;
    const password = document.getElementById("password-input").value;

    if (!validateEmail(email)) {
        return;
    }

    sendData("login",{email:email,password:password}).
    then(response => {
        if (response.ok) {
            window.location.href = "/";
        } else {
            response.text().then((errorMessage) => {
                displayErrorMessage(errorMessage);
            });
        }
    }
    ).catch(err => {
        displayErrorMessage("Something went wrong.");
    }
    )
}

validateNote = (e) => {
    e.preventDefault();
    const title = document.getElementById("note-title").value;
    const content = document.getElementById("note-text").value;

    if(title.length==0 || content.length==0){
        displayErrorMessage("Title and content cannot be empty.");
        return;
    }

    const formData = {
        title: title,
        content: content
    };

    sendData("add-notes",formData)
    .then(response => {
        if (response.ok) {
            window.location.href = "/";
        } else {
            response.text().then((errorMessage) => {
                displayErrorMessage(errorMessage);
            });
        }
    }
    ).catch(err => {
        displayErrorMessage("Something went wrong.");
    }
    )
}

handleDelete = (note_id) => {
    sendData("delete-note",{note_id:note_id})
    .then(response => {
        if (response.ok) {
            window.location.href = "/";
        } else {
            response.text().then((errorMessage) => {
                displayErrorMessage(errorMessage);
            });
        }
    }
    ).catch(err => {
        displayErrorMessage("Something went wrong.");
    }
    )
}