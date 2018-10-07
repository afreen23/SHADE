// function hello() {
//     alert('hello')
// }

function handleSignin(){
    alert('hhi');
    console.log('hi');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        // Typical action to be performed when the document is ready:
        console.log("fetched")
        }
    };
    xhttp.open("GET", "https://shadeapp.herokuapp.com/twitter", true);
    xhttp.send()
  }