 function like() {

      let num = document.querySelector("#bar").innerHTML
      let heart = document.querySelector("#foo");

      if (heart.classList.contains("btn-secondary")) {
         this.className = "btn btn-danger float-left";
         num++;
         document.querySelector("#bar").innerHTML = num;
      } else {
         this.className = "btn btn-secondary float-left";
         num--;
         document.querySelector("#bar").innerHTML = num;
      }
   }

   document.addEventListener('DOMContentLoaded', function() {
      document.querySelector("#foo").onclick = like;
  });

    // TEMP alert dataset-id of each Tweet
 // foo = document.getElementsByClassName('ms-2 card')
 // for (const element of foo) {
    alert(element.dataset.id)
 // }
  
  // TEMP alert dataset-id of clicked Tweet - super hacky
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.booboo').onclick = function() {
      alert(event.target.parentElement.parentElement.dataset.id)
    }})