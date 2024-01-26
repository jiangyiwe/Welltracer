<template>

  <div class="navbar">

    <div class="navbar-container">

      <button type="button" class="collapsible" label-for="login">
        <img class="navbar-icon" src="@/assets/icons/right-to-bracket-solid.svg" alt="Login"/>
      </button>
      <button type="button" class="collapsible" label-for="menu">
        <img class="navbar-icon" src="@/assets/icons/bars-solid.svg" alt="Menu"/>
      </button>
      <button type="button" class="collapsible" label-for="physical">
        <img class="navbar-icon" src="@/assets/icons/user-solid.svg" alt="Physical Information"/>
      </button>
    </div>
    <div class="content-container">

      <div class="content" id="login">

        <Login  class="component"/>
      </div>

      <div class="content" id="menu">

        <div style="padding: 1em; padding-right: 12em">

          <a href="/HomePage" style="white-space: nowrap">Menu principal</a> <br>
          <a href="/features/home_fitness" style="white-space: nowrap">Exercices à la maison</a> <br>
          <a href="/features/scan_a_meal" style="white-space: nowrap">Scan de nourriture</a> <br>
          <a href="/features/prescription_scan" style="white-space: nowrap">Scan de prescription</a> <br>
          <a href="/features/diets" style="white-space: nowrap">Analyse de votre alimentation</a>
        </div>

      </div>
      <div class="content" id="physical">
        <PhysicalInfo class="component" />
      </div>
    </div>
  </div>







</template>

<script>
import Login from '@/components/Login.vue'
import PhysicalInfo from "@/components/navbar/PhysicalInfo.vue";

export default {
  name: "NavBar",
  data() {
    return {
      Login
    }
  },
  methods: {

  },
  components: {
    PhysicalInfo,
    Login
  },
  mounted() {

    let coll = document.getElementsByClassName("collapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        let content = document.getElementById(this.getAttribute("label-for"));
        if (content.style.maxHeight){
          content.style.maxHeight = null;
          content.style.maxWidth = '30px';
        } else {
          content.style.maxHeight = content.scrollHeight + 40 + "px";
          content.style.maxWidth = content.scrollWidth + "px";
          //content.style.paddingTop = '1em';
          //content.style.paddingBottom = '1em';
        }
      });
    }
  }
}



</script>

<style scoped>
/* Style the button that is used to open and close the collapsible content */
.collapsible {
  background-color: #eee;
  color: #444;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: center;
  outline: none;
  font-size: 15px;
}

/* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
.active, .collapsible:hover {
  background-color: #ccc;
}

/* Style the collapsible content. Note: hidden by default */
.content {
  overflow: hidden;
  background-color: #f1f1f1;
  max-height: 0;
  max-width: 30px;
  transition: all 0.2s ease-out;
}

.navbar-icon {
  width: 16px;
}

.navbar-container {
  display: flex;
  flex-direction: row;



}

.navbar {
  z-index: 1;
  position: absolute;
  right: 0;
  top: 0;


  border: 2px outset hsla(160, 100%, 37%, 1);
  /*border-radius: 2.5em;*/
  /*background-color: hsla(160, 100%, 37%, 0.2);*/

  background-color: #eee;

}
.content-container {
}

.component {
  padding: 1em
}





</style>