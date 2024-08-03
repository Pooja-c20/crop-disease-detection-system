
  //learn more button in about us
  var learnMore = document.getElementById('learnMore');
  var learnMoreContent = document.getElementById("showHide")
  var hero = document.querySelector('.hero')
  var aboutCon = document.querySelector('.about-con') 
  var nav = document.querySelector('nav')

  learnMore.addEventListener("click", function(){
    learnMoreContent.classList.toggle('hideShow')

    if (learnMore.innerHTML === "Learn More") {
      learnMore.innerHTML = "Hide It!";
    } else {
      learnMore.innerHTML = "Learn More";
    }

    hero.classList.toggle('about-us2')
    aboutCon.classList.toggle('about-con2')
    nav.classList.toggle('filter')
  })


function previewImage() {
    var input = document.getElementById('imageInput');
    var preview = document.getElementById('imagePreview');
  
    // Ensure that a file is selected
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        // Create an image element
        var img = document.createElement('img');
        img.src = e.target.result;
  
        // Append the image to the preview div
        preview.innerHTML = '';
        preview.appendChild(img);
      };
  
      // Read the selected file as a data URL
      reader.readAsDataURL(input.files[0]);

      document.querySelector('.upload-box').style.padding = "2rem 4rem";
      document.querySelector('.box1').style.margin = "4rem 0 0 0";

    } else {
      // Handle the case when no file is selected
      preview.innerHTML = 'No image selected';
    }
  }

const formdata = new FormData();
formdata.append("file", fileInput.files[0], "/C:/Users/Pooja Ghadge/Downloads/potato_late-blight_07_zoom-Photo-OMAFRA.jpg");

const requestOptions = {
  method: "POST",
  body: formdata,
  redirect: "follow"
};

fetch("http://127.0.0.1:5000/api/prediction", requestOptions)
  .then((response) => response.text())
  .then((result) => console.log(result))
  .catch((error) => console.error(error));
