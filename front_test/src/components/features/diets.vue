<template>

  <h1 style="margin-top: 2em">Analyseur de portions</h1>

  <div v-if="response">


    <div class="container">
      <div>
        <h3 class="text-box"> Conseils généraux</h3>
        <div class="text-box">
          {{response.data.advice_warning}}
        </div>
        <div class="text-box">
          {{response.data.advice}}
        </div>

        <h3 class="text-box">Conseils nutritionnels précis</h3>
        <div class="text-box">
          {{response.data.advice2}}
        </div>

      </div>

    </div>

    <h3>Détails de consommation</h3>

    <table>
      <tr>
        <td>Consommation</td>
        <td>{{response.data.calories_intake}}</td>
      </tr>
      <tr>
        <td>Besoins journaliers</td>
        <td>{{response.data.daily_needs}}</td>
      </tr>
      <tr>
        <td>Différence</td>
        <td style="font-weight: bold">{{response.data.calorie_intake_diff}}</td>
      </tr>


    </table>
  </div>


  <button class="button-3" @click="clearHistory">Nettoyer l'historique de consommation</button>

  {{ eraseMessage }}


</template>

<script>
import axios from 'axios';
export default {
  name: "diets",
  data() {

    return {
      response: false, formData: '', eraseMessage: ''
    }
  },
  mounted() {
    this.analyzeConsumption()
  },
  methods: {
    async analyzeConsumption(){

      try {
        const formData = new FormData()
        formData.append("gender", $cookies.get("gender"))
        formData.append("weight", $cookies.get("weight"))
        formData.append("height", $cookies.get("height"))
        if ($cookies.get("personal_kcal_objective") === "true") {
          formData.append("kcal_objective", $cookies.get("kcal_objective"))
        }
        const res = await axios.post("http://localhost:5001/analyze_api", formData)
        this.response = res
        this.formData = formData
        console.log(formData)

      } catch (e) {
        console.error(e)
      }


    },
    async clearHistory() {
      try {
        const formData=new FormData()
        const res = await axios.post("http://localhost:5001/clear_predictions", formData)
        this.eraseMessage = "Prédictions effacées, scannez de nouveaux repas pour à nouveau recevoir des prédictions !"
      } catch (e) {
        console.error(e)
      }
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}
.text-box {
  padding-bottom: 1em;
}
</style>