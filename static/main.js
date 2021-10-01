const showCam = document.getElementById("show-cam");
const hideCam = document.getElementById("hide-cam");
const captureImg = document.getElementById("capture-image");
const library = document.getElementById("library");
const library2 = document.getElementById("library2");
const stream = document.getElementById("stream");

const streamFile = document.getElementById("streamFile");
const submitFile = document.getElementById("submitFile");
const show = document.getElementById("show");

const input = document.querySelector("input");

const video = document.getElementById("video");
const image = document.getElementById("image");

showCam.addEventListener("click", async () => {
  stream.style.display = "initial";
});

hideCam.addEventListener("click", async () => {
  stream.style.display = "none";
});

captureImg.addEventListener("click", async () => {
  var xhttp = new XMLHttpRequest();
  xhttp.open("post", "http://localhost:3456/saveimg", true);
  xhttp.send("saveimg");
});


// library.addEventListener("click", function (e) {
//   clickButton(streamFile, function () {
//     submitFile.click();
//   });
// }, false);

// async function clickButton(button, callback) {
//   button.click();
//   await input.addEventListener("change", function () {
//     callback();
//   })
// }

// submitFile.addEventListener("click", function (e) {
//   var oFReader = new FileReader();
//   oFReader.readAsDataURL(streamFile.files[0]);

//   oFReader.onload = function (oFREvent) {
//     document.getElementById("img-from-lib").src = oFREvent.target.result;
//   };
// });

library.addEventListener("click", async () => {
  var xhttp = new XMLHttpRequest();
  xhttp.open("post", "http://localhost:3456/getlib", true);
  xhttp.send("getlib");

  var result = document.getElementById('result');

  while (result.firstChild) {
    result.removeChild(result.lastChild);
  }

  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      recvData = this.responseText;
      const recvArr = recvData.split(",");
      for (const element of recvArr) {
        var newDiv = document.createElement("div");
        var newline = document.createElement('br');
        var newlabel = document.createElement('label');
        newlabel.innerHTML = element;
        var newinput = document.createElement('input');
        newinput.className = "abcdef";
        newinput.type = "radio";
        newinput.name = "lib";
        newinput.id = element;
        newinput.value = element;
        newDiv.appendChild(newinput);
        newDiv.appendChild(newlabel);
        newDiv.appendChild(newline);
        document.getElementById("result").appendChild(newDiv);
      }
    } else {
      console.log("error while receiving data");
    }
  }
});

show.addEventListener("click", function (e) {
  var abcdef = document.getElementsByClassName('abcdef');
  var value;
  for (var i = 0; i < abcdef.length; i++) {
    if (abcdef[i].type === 'radio' && abcdef[i].checked) {
      value = abcdef[i].value.toString();         
    }
  }
  console.log(value);
  var xhttp2 = new XMLHttpRequest();
  xhttp2.open("post", "http://localhost:3456/getimg", true);
  xhttp2.send(value);
});

var eventSource = new EventSource('/getflag');
var alertFlag = true;
eventSource.onmessage = function(e) {
  alertFlag = true;
  console.log(e.data);
    if (e.data == "False" && alertFlag == true) {
      alert("Tracking failure detected"); 
      alertFlag = false;
    }
};

