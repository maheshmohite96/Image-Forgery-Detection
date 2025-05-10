const form = document.getElementById("uploadForm");
const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const resultBox = document.getElementById("resultBox");

imageInput.addEventListener("change", function () {
  const file = imageInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const file = imageInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  resultBox.innerText = "Analyzing...";

  try {
    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    resultBox.innerText = data.result || "Analysis failed.";
  } catch (error) {
    console.error("Error:", error);
    resultBox.innerText = "Server error.";
  }
});

// login page start
// document.getElementById('loginForm').addEventListener('submit', function (e) {
//   e.preventDefault();

//   const inputEmail = document.getElementById('email').value;
//   const inputPassword = document.getElementById('password').value;

//   const storedEmail = localStorage.getItem('userEmail');
//   const storedPassword = localStorage.getItem('userPassword');

//   if (inputEmail === storedEmail && inputPassword === storedPassword) {
//     // Show success notification
//     const msg = document.createElement('div');
//     msg.textContent = 'Login Successfully!';
//     msg.style.position = 'fixed';
//     msg.style.top = '20px';
//     msg.style.left = '50%';
//     msg.style.transform = 'translateX(-50%)';
//     msg.style.backgroundColor = '#28a745';
//     msg.style.color = 'white';
//     msg.style.padding = '10px 20px';
//     msg.style.borderRadius = '5px';
//     msg.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
//     document.body.appendChild(msg);

//     // Redirect to home after 2 seconds
//     setTimeout(() => {
//       window.location.href = 'home.html';
//     }, 2000);
//   } else {
//     alert('Invalid email or password');
//   }
// });


// document.getElementById("loginForm").addEventListener("submit", function (e) {
//   e.preventDefault();

//   const loginEmail = document.getElementById("loginEmail").value;
//   const loginPassword = document.getElementById("loginPassword").value;

//   const storedEmail = localStorage.getItem("userEmail");
//   const storedPassword = localStorage.getItem("userPassword");

//   if (loginEmail === storedEmail && loginPassword === storedPassword) {
//     // Show notification
//     const msg = document.createElement('div');
//     msg.textContent = 'Login Successfully!';
//     msg.style.position = 'fixed';
//     msg.style.top = '20px';
//     msg.style.left = '50%';
//     msg.style.transform = 'translateX(-50%)';
//     msg.style.backgroundColor = '#28a745';
//     msg.style.color = 'white';
//     msg.style.padding = '10px 20px';
//     msg.style.borderRadius = '5px';
//     msg.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
//     document.body.appendChild(msg);

//     setTimeout(() => {
//       window.location.href = 'index.html';
//     }, 2000);
//   } else {
//     alert("Invalid email or password.");
//   }
// });



// login page end


// register page start
// document.getElementById("registerForm").addEventListener("submit", function (e) {
//   e.preventDefault();

//   const email = document.getElementById("email").value;
//   const password = document.getElementById("password").value;
//   const confirmPassword = document.getElementById("confirmPassword").value;

//   if (password !== confirmPassword) {
//     alert("Passwords do not match!");
//     return;
//   }

//   // Save to localStorage
//   localStorage.setItem("userEmail", email);
//   localStorage.setItem("userPassword", password);

//   // Show notification
//   const msg = document.createElement('div');
//   msg.textContent = 'Registered Successfully!';
//   msg.style.position = 'fixed';
//   msg.style.top = '20px';
//   msg.style.left = '50%';
//   msg.style.transform = 'translateX(-50%)';
//   msg.style.backgroundColor = '#28a745';
//   msg.style.color = 'white';
//   msg.style.padding = '10px 20px';
//   msg.style.borderRadius = '5px';
//   msg.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
//   document.body.appendChild(msg);

//   // Redirect after 2s
//   setTimeout(() => {
//     window.location.href = 'index.html';
//   }, 2000);
// });
// // register page end

import React, { useState } from 'react';
import axios from 'axios';

function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData);
      setResult(response.data);
    } catch (error) {
      console.error("API Error:", error);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Check Forgery</button>
      {result && (
        <div>
          <p>Result: {result.is_fake ? "Fake" : "Real"}</p>
          <p>Confidence: {result.confidence.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}

export default Upload;