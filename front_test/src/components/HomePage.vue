<script setup>
  import { ref } from 'vue';


  let myValue = "<p>horse :)</p>";
  let bool1 = false;
  let bool2 = true;

  const loggedIn = ref(false);
  //let loggedIn = false;

  let logobar = "sample value for logo";
  let sitelink = "https://banhammer.net"



  let navMenu = "<div>GAY BACON STRIPS</div>";

  function toggleLogIn() {
    loggedIn.value = !loggedIn.value;
  }


  import menu_structure from '@/assets/menu_structure.json';
  //let menu_structure = new Map(menu_structure_obj.entries)
  //let menu_structure_json = require('@/assets/menu_structure.json')
  //let menu_structure = JSON.parse(menu_structure_json)

  function extractStructure(depth = '') {
    let path_in = depth.split('/');
    if (depth === '') {
      path_in = [];
    }
    let ret = menu_structure;
    console.log(menu_structure);
    console.log(path_in)
    for(const el of path_in) {
      ret = ret[el];
    }
    return ret;
  }
  function buildMenu(depth = '') {
    let new_structure = extractStructure(depth);
    let result = '<table><tr>'
    let isSecondRowEl = false;
    console.log('owo')
    console.log(new_structure)
    for(const el in new_structure) {
      console.log(el)
      result += `<td class="cell"> element ${new_structure[el].label}</td>`
      if (isSecondRowEl) {
        result += "</tr><tr>"
        isSecondRowEl = false;
      } else {
        isSecondRowEl = true;
      }
    }
    if (isSecondRowEl) {
      result += "</tr>"
    }
    result += "</table>"
    return result
  }


</script>

<style scoped>

table {
  width: 960px;
}
tr {
}
.container {
  display: flex; flex-flow: row wrap
}
th, td, .cell{
  width: 50%;
  border-bottom: 1px dashed white;
  padding: 10px;

  border-right: 1px dashed white;
  text-align: center
}

.tab {
  display: block;
}
.tab-pic {
  width: 80%
}

</style>

<template>






  <div class="container">
    <div class="cell" v-for="element in extractStructure()">
      <img class="tab-pic" src="../assets/icons/protection.png"/>

      <p></p>
      <a href="feature/{{element.feature}}">{{ element.label }}</a>

    </div>

  </div>




</template>
<!--
  <div>
    <a :href="sitelink">Site Link</a>
  </div>
  <div>
    <table>
      <tr>
        <td><a class="tab" href="banhammer.net">ee</a></td>
        <td>dd</td>
      </tr>
      <tr>
        <td>aa</td>
        <td>zz</td>
      </tr>
    </table>

  </div>
    <div>
    <p>huuzehhiuzhiuzehiu</p>
  </div>
  <div>
    <div v-if="loggedIn">You are logged in!</div>
    <div v-else>You are not logged in!</div>
    <button @click="toggleLogIn">Log in or out</button>
  </div>
  <div :id="logobar">

  </div>

  <div>empty text</div>
  <div v-html="myValue"></div>

  <div v-if="bool1">this shouldn't display</div>

  <nav :id="navMenu" style="">

    <div v-for="">
      <div>Item</div>
    </div>

    <table v-html="buildMenu('')">

    </table>

  </nav>
-->