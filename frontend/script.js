// ==========================================
// GET HTML ELEMENTS
// ==========================================

const resumeFile = document.getElementById("resumeFile");

const uploadArea = document.getElementById("uploadArea");

const fileName = document.getElementById("fileName");

const parseBtn = document.getElementById("parseBtn");

const loading = document.getElementById("loading");

const errorMessage = document.getElementById("errorMessage");

const results = document.getElementById("results");


// ==========================================
// FILE SELECTION
// ==========================================

resumeFile.addEventListener("change", function () {

    if (resumeFile.files.length > 0) {

        const file = resumeFile.files[0];

        fileName.textContent = file.name;

    }

});


// ==========================================
// CLICK UPLOAD AREA
// ==========================================

uploadArea.addEventListener("click", function (event) {

    // Don't trigger twice when clicking the button
    if (event.target.tagName !== "LABEL") {

        resumeFile.click();

    }

});


// ==========================================
// DRAG AND DROP
// ==========================================

uploadArea.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        uploadArea.style.borderColor = "#4f46e5";

    }
);


uploadArea.addEventListener(
    "dragleave",
    function () {

        uploadArea.style.borderColor = "#a5b4fc";

    }
);


uploadArea.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        uploadArea.style.borderColor = "#a5b4fc";

        const files = event.dataTransfer.files;

        if (files.length > 0) {

            resumeFile.files = files;

            fileName.textContent = files[0].name;

        }

    }
);


// ==========================================
// PARSE RESUME
// ==========================================

parseBtn.addEventListener("click", async function () {

    hideError();

    results.classList.add("hidden");


    // Check file
    if (resumeFile.files.length === 0) {

        showError(
            "Please select a PDF resume first."
        );

        return;
    }


    const file = resumeFile.files[0];


    // Check PDF
    if (
        !file.name.toLowerCase().endsWith(".pdf")
    ) {

        showError(
            "Only PDF files are supported."
        );

        return;
    }


    // Create FormData
    const formData = new FormData();

    formData.append(
        "resume",
        file
    );


    // Show loading
    loading.classList.remove("hidden");

    parseBtn.disabled = true;


    try {

        // Send request to Flask backend

        const response = await fetch(
            "http://127.0.0.1:5000/parse-resume",
            {
                method: "POST",
                body: formData
            }
        );


        // Check server response

        if (!response.ok) {

            throw new Error(
                "Server error: " + response.status
            );

        }


        const result = await response.json();


        console.log(
            "Backend response:",
            result
        );


        // Display parsed data

        displayResults(
            result.data
        );


    } catch (error) {

        console.error(error);

        showError(
            "Unable to connect to the backend. Make sure Flask is running on port 5000."
        );

    } finally {

        loading.classList.add("hidden");

        parseBtn.disabled = false;

    }

});


// ==========================================
// DISPLAY RESULTS
// ==========================================

function displayResults(data) {

    // --------------------------------------
    // Name
    // --------------------------------------

    document.getElementById("name").textContent =
        data.name || "Not found";


    // --------------------------------------
    // Email
    // --------------------------------------

    document.getElementById("email").textContent =
        data.email || "Not found";


    // --------------------------------------
    // Phone
    // --------------------------------------

    document.getElementById("phone").textContent =
        data.phone || "Not found";


    // --------------------------------------
    // Skills
    // --------------------------------------

    const skillsContainer =
        document.getElementById("skills");


    skillsContainer.innerHTML = "";


    if (
        data.skills &&
        data.skills.length > 0
    ) {

        data.skills.forEach(
            function (skill) {

                const span =
                    document.createElement("span");

                span.className = "skill";

                span.textContent = skill;

                skillsContainer.appendChild(span);

            }
        );

    } else {

        skillsContainer.innerHTML =
            '<span class="empty">No skills detected</span>';

    }


    // --------------------------------------
    // Education
    // --------------------------------------

    const educationList =
        document.getElementById("education");


    educationList.innerHTML = "";


    if (
        data.education &&
        data.education.length > 0
    ) {

        data.education.forEach(
            function (education) {

                const li =
                    document.createElement("li");

                li.textContent = education;

                educationList.appendChild(li);

            }
        );

    } else {

        educationList.innerHTML =
            "<li>No education information detected</li>";

    }


    // --------------------------------------
    // Experience
    // --------------------------------------

    const experienceList =
        document.getElementById("experience");


    experienceList.innerHTML = "";


    if (
        data.experience &&
        data.experience.length > 0
    ) {

        data.experience.forEach(
            function (experience) {

                const li =
                    document.createElement("li");

                li.textContent = experience;

                experienceList.appendChild(li);

            }
        );

    } else {

        experienceList.innerHTML =
            "<li>No experience information detected</li>";

    }


    // --------------------------------------
    // Show results
    // --------------------------------------

    results.classList.remove("hidden");

    results.scrollIntoView({
        behavior: "smooth"
    });

}


// ==========================================
// SHOW ERROR
// ==========================================

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

}


// ==========================================
// HIDE ERROR
// ==========================================

function hideError() {

    errorMessage.textContent = "";

    errorMessage.classList.add("hidden");

}
