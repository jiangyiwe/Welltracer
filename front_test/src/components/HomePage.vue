<script setup>
  import menu_structure from '@/assets/menu_structure.json';

  let urlParams = new URLSearchParams(window.location.search);
  let menu_depth = urlParams.get('depth');
  if (!menu_depth) {
    menu_depth = ''
  }

  function extractStructure(depth = "") {
    let path_in = depth.split('/');
    if (depth === '') {
      path_in = [];
    }

    let ret = menu_structure;
    for(const el of path_in) {
      ret = ret[el].children;
    }
    return ret;
  }
  //const structure = extractStructure(menu_depth)

  function cell_link(element) {
    if (element.children) {
      return `?depth=${element.cat}`;
    } else if (element.feature) {
      return `features/${element.feature}`;
    } else {
      return '#';
    }
  }

</script>

<style scoped>


.container {
  display: flex;
  flex-flow: row wrap;
  padding-top: 2em;
  padding-bottom: 2em;
  margin-left: 2em;
  margin-right: 2em;
}

.cell {
  width: 50%;
  padding: 10px;



}
.cell-body {
  height: 100%;
  width: 100%;


  border: 3px outset hsla(160, 100%, 37%, 1);
  border-radius: 2.5em;
  padding: 1em;
  background-color: hsla(160, 100%, 37%, 0.2);

  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;

  /*box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;*/
  box-shadow: rgba(0, 0, 0, 0.19) 0 10px 20px, rgba(0, 0, 0, 0.23) 0 6px 6px;

}
.cell-body:hover {
  background-color: hsla(160, 100%, 37%, 0.3);
}

.tab-empty-elem {

}
.tab-pic {
  width: 40%;
  display:flex;
  padding-bottom: 1em;
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

.phone {

}

</style>

<template>





  <div class="phone">


      <div class="container">
        <div class="cell" v-for="element in extractStructure(menu_depth)">
          <a :href="cell_link(element)">
            <div class="cell-body">
              <div class="tab-empty-elem"></div>
              <img class="tab-pic" :src="`src/assets/icons/${element.logo}`" :alt="element.label"/>
              <p class="title"><a>{{ element.label }}</a></p>
            </div>
          </a>
        </div>
      </div>
      <div class="bottom-section">
        <a class="title" v-if="menu_depth" :href="`?depth=`">Retour au menu</a>
        <div v-else >
          <p class="title"> Récemment visités </p>
          <div class="container">

          </div>
        </div>
      </div>
    </div>

</template>