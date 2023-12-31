<script setup>
  import { ref } from 'vue';


  import menu_structure from '@/assets/menu_structure.json';

  let urlParams = new URLSearchParams(window.location.search);
  let menu_depth = urlParams.get('depth');
  if (!menu_depth) {
    menu_depth = ''
  }
  console.log(menu_depth)

  function extractStructure(depth = "") {
    console.log(depth)
    let path_in = depth.split('/');
    console.log(path_in)
    if (depth === '') {
      path_in = [];
    }

    let ret = menu_structure;
    for(const el of path_in) {
      ret = ret[el].children;
    }
    console.log(ret)
    return ret;
  }



</script>

<style scoped>

template {
  color: black;
  background-color: grey;
}

table {
  width: 960px;
}
tr {
}
.container {
  display: flex;
  flex-flow: row wrap;
  padding-top: 2em;
  padding-bottom: 2em;
}
th, td, .cell{
  width: 50%;
  border-bottom: 1px dashed;
  padding: 10px;

  border-right: 1px dashed;
  /*text-align: center;*/
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.tab {
  display: block;
}
.tab-empty-elem {

}
.tab-pic {
  width: 40%;
  display:flex;
  align-items: center;
  justify-content: center;


}


.bottom-section {

}

.title {
  font-weight: bold;
  font-size: 16px;
  font-family: MD Primer Bold,Rubik,Lato,Lucida Grande,Lucida Sans Unicode,Tahoma,Sans-Serif;
}

#phone {
  width: 600px;
  /*background-color: lightgray;
  color: darkgreen;*/

}

</style>

<template>




    <div id="phone">
      <div class="container">
        <div class="cell" v-for="element in extractStructure(menu_depth)">
          <div class="tab-empty-elem"></div>

          <img class="tab-pic" :src="`src/assets/icons/${element.logo}`" :alt="element.label"/>

          <a class="title" v-if="element.children" :href="`?depth=${element.cat}`">{{ element.label }}</a>
          <a class="title" v-if="element.feature" :href="`feature/${element.feature}`">{{ element.label }}</a>

        </div>
      </div>
      <div class="bottom-section">
        <a class="title" v-if="menu_depth" :href="`?depth=`">Retour au menu</a>
        <div v-else >
          <p class="title"> Souvent visités </p>
          <div class="container">

          </div>
        </div>
      </div>

    </div>







</template>