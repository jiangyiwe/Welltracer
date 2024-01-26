<script>
import {ref} from 'vue'
import VueCookies from 'vue-cookies'

export default {
  name: "PhysicalInfo",
  data() {
    function setPhysicalInfo() {
      $cookies.set("weight", weight.value)
      $cookies.set("height", height.value)
      $cookies.set("gender", gender.value)
      $cookies.set("kcal_objective", kcal_objective.value)
      $cookies.set("personal_kcal_objective", personal_kcal_objective.value)

    }
    const weight = ref(60)
    const height = ref(170)
    const gender = ref('X')
    const kcal_objective = ref(2200)
    const personal_kcal_objective = ref("false")

    const cweight = $cookies.get("weight")
    const cheight = $cookies.get("height")
    const cgender = $cookies.get("gender")
    const ckcal = $cookies.get("kcal_objective")
    const cpkcal = $cookies.get("personal_kcal_objective")


    if (cweight && !isNaN(cweight) && cweight > 30) {
      weight.value = cweight
    }
    if (cheight && !isNaN(cheight) && cheight > 100) {
      height.value = cheight
    }
    if (cgender && ["F", "M", "X"].includes(cgender)) {
      gender.value = cgender
    }
    if (ckcal && !isNaN(ckcal) && ckcal > 0) {
      kcal_objective.value = ckcal
    }
    if (cpkcal==="true") {
      personal_kcal_objective.value = "true"
    }

    return {
      setPhysicalInfo, weight, height, gender, kcal_objective, personal_kcal_objective
    }
  },


}




</script>
<template id="template-physical">

  <div style="padding:1em">
    <h3 class="title">Vos caractéristiques physiques</h3>

    <div class="physical-content">
      <label for="height">Ma taille
        <input class="physical-input" id="height" v-model="height" type="number" />
      </label>
    </div>
    <div class="physical-content">
      <label >Mon poids
        <input class="physical-input" id="weight" v-model="weight" type="number" />
      </label>
    </div>
    <div class="physical-content">
      <span>Genre</span>
      <div>

        <label class="button-3">
          F
          <input type="radio" id="gender-f" v-model="gender" value="F" />
        </label>
        <label class="button-3">
          M
          <input type="radio" id="gender-m" v-model="gender" value="M" />
        </label>
        <label class="button-3">
          X
          <input type="radio" id="gender-x" v-model="gender" value="X" />
        </label>
      </div>
    </div>
    <div class="physical-content">
      <span>Utiliser un objectif calorique personnalisé ?</span>
    <div>
      <label class="button-3">Oui
        <input type="radio"  v-model="personal_kcal_objective" value="true" />
      </label>
      <label class="button-3">Non
        <input type="radio"  v-model="personal_kcal_objective" value="false" />
      </label>
    </div>

    </div>
    <div class="physical-content">
      <label>Mon objectif calorique personnel
        <input class="physical-input" id="kcal" v-model="kcal_objective" type="number" />
      </label>

    </div>
    <div class="physical-content">
      <button class="button-3" role="button"  @click="setPhysicalInfo()">Enregistrer vos caractéristiques</button>
    </div>

  </div>


  <div class="physical-container">



    <div class="physical-subcontainer">
    </div>

  </div>
</template>
<style scoped>
.physical-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  /*white-space: nowrap;*/
}

.physical-subcontainer {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 1em;
  align-items: stretch;
  /*white-space: nowrap;*/
}
.physical-content {
  padding-top: 1em;
}

.physical-input {

  padding: 5px 12px;
  font-size: 14px;
  line-height: 20px;
  color: #24292e;
  vertical-align: middle;
  background-color: #ffffff;
  background-repeat: no-repeat;
  background-position: right 8px center;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  outline: none;
  box-shadow: rgba(225, 228, 232, 0.2) 0 1px 0 0 inset;
}
:focus{
  border-color: #0366d6;
  outline: none;
  box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 3px;
}






</style>