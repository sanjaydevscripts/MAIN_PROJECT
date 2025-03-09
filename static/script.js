const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');
let uploadedFileName = ''; // Store the uploaded filename

selectImage.addEventListener('click', function () {
    inputFile.click();
});

inputFile.addEventListener('change', function () {
    const image = this.files[0];

    if (image && image.size < 2000000) { // 2MB limit
        const reader = new FileReader();
        reader.onload = () => {
            // Remove previous images
            const allImg = imgArea.querySelectorAll('img');
            allImg.forEach(item => item.remove());

            // Display selected image
            const imgUrl = reader.result;
            const img = document.createElement('img');
            img.src = imgUrl;
            imgArea.appendChild(img);
            imgArea.classList.add('active');
            imgArea.dataset.img = image.name;
            
            uploadedFileName = image.name; // Save filename for deletion

            // Upload image
            uploadImage(image);
        };
        reader.readAsDataURL(image);
    } else {
        alert("Image size must be less than 2MB");
    }
});
//Analyse function
function analyseImage() {
    const imageDiv = document.getElementById("image"); // Select the div
    const imgValue = imageDiv.getAttribute("data-img")
    console.log("Sending image src:", imgValue); // Debugging

    fetch("http://127.0.0.1:5000/analyse", {  
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ img_src: imgValue }),
    })
    .then(response => {
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => 
        {
            console.log("------------",data.path)
            console.log("Received image path:", data.path);

            const resultImg = document.getElementById("resultImage");
            resultImg.src = data.path;  // Set the new image source
            resultImg.style.display = "block"; // Make it visible
        })
    .catch(error => console.error("Fetch Error:", error));
}

//enhance
function enhanceImage() {
    const imageDiv = document.getElementById("image"); // Select the div
    const imgValue = imageDiv.getAttribute("data-img")
    console.log("Sending image src:", imgValue); // Debugging

    fetch("http://127.0.0.1:5000/enhance", {  
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ img_src: imgValue }),
    })
    .then(response => {
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => 
        {
            console.log("------------",data.path)
            console.log("Received image path:", data.path);

            const resultImg = document.getElementById("enhancetImage");
            resultImg.src = data.path;  // Set the new image source
            resultImg.style.display = "block"; // Make it visible
        })
    .catch(error => console.error("Fetch Error:", error));
}

// Upload function
function uploadImage(image) {
    const formData = new FormData();
    formData.append('file', image);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert(data.message);
    })
    .catch(error => console.error('Upload Error:', error));
}


// Delete all images when Cancel is clicked
function cancelAction() {
    fetch("http://127.0.0.1:5000/delete_all", {
        method: "POST",
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Show success message
        console.log("All images deleted!");

        // Clear images from frontend
        document.getElementById("image").innerHTML = `
            <i class='bx bxs-cloud-upload icon'></i>
            <p>Image size must be less than <span>2MB</span></p>
        `;
        document.getElementById("enhancetImage").style.display = "none";
        document.getElementById("resultImage").style.display = "none";
    })
    .catch(error => console.error("Error deleting images:", error));
}