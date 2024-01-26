<template>

  <picture-input
      ref="pictureInput"
      width="600"
      height="600"
      margin="16"
      accept="image/jpeg,image/png"
      size="10"
      button-class="btn"
      :custom-strings="{
        upload: '<h1>Uploadez une photo de votre repas ici !</h1>',
        drag: 'Uploadez une photo de votre repas ici !'
      }"
      @change="onChange">
  </picture-input>

  <div style="padding-top: 2em; padding-bottom: 2em">
    <h3>Quelle est la masse de votre portion ?</h3>

    <label class="button-3">Petite portion (100g)
      <input type="radio" v-model="meal_mass" value="100" />
    </label>
    <label class="button-3">Portion moyenne (250g)
      <input type="radio" v-model="meal_mass" value="250" />
    </label>
    <label class="button-3">Grande portion (400g)
      <input type="radio" v-model="meal_mass" value="400" />
    </label>


  </div>

  <button class="button-3" @click="sendPicture()">Envoyer l'image au serveur</button>

  <div v-if="response">
    <div v-if="response.data" style="margin-top: 1em">
      <p>Votre repas appartient à la catégorie : {{response.data.class}}</p>
      <p>D'après vos entrées, votre portion contient les nutriments suivants :</p>

      <p>{{response.data.mass }} g : &emsp; {{response.data.calories}}cal / {{response.data.kj}}kJ</p>

    </div>

    <div v-if="response.data">
      <p style="margin-top: 1em">La prédiction de catégorie est erronée ? Corrigiez la ici !</p>

      <select v-model="corrected_class" class=button-3 style="margin-bottom: 1em; background-color: grey">
        <option disabled value="">Sélectionnez la catégorie</option>
        <option>Dairy product</option>
        <option>Dessert</option>
        <option>Egg</option>
        <option>Fried food</option>
        <option>Meat</option>
        <option>Seafood</option>
        <option>Soup</option>
        <option>Bread</option>
        <option>Noodles-Pasta</option>
        <option>Rice</option>
      </select>

      <p>{{corrected_thankyou}}</p>

      <button @click="sendCorrection()" class="button-3">Valider la correction</button>


    </div>
  </div>



  <div v-else>
    {{ response }}
  </div>
</template>

<script>
import axios from 'axios';
import { getUserId } from '@/components/Login.vue'
import PictureInput from 'vue-picture-input'

export default {
  name: "scan_a_meal",
  data () {
    return {
      response: '', meal_mass: 100, corrected_class:'', corrected_thankyou:''
    }
  },
  components: {
    PictureInput
  },
  methods: {
    onChange (image) {
      console.log('New picture selected!')
      if (image) {
        console.log('Picture loaded.')
        console.log(image)
        this.image = image
      } else {
        console.log('FileReader API not supported.')
      }
    },
    async sendPicture() {
      if (!this.image) {
        return;
      }
      try {
        const formData = new FormData();
        console.log(this.image.target.files[0])
        formData.append('image', this.image.target.files[0]);


        let gender = $cookies.get("gender")
        let weight = $cookies.get("weight")
        let height = $cookies.get("height")
        if (gender) formData.append("gender", gender)
        if (weight) formData.append("weight", weight)
        if (height) formData.append("height", height)
        if ($cookies.get("personal_kcal_objective") && $cookies.get("personal_kcal_objective") === "true") {
          formData.append("kcal_objective",  $cookies.get("kcal_objective"))
        }
        console.log(this.meal_mass)
        formData.append("mass",this.meal_mass)

        console.log(formData)

        const res = await axios.post("http://localhost:5001/predict_img_api", formData, {
          headers: this.image.target.files[0].type
        })
        this.response = res

      } catch (e) {
        console.error(e)
      }
    },
    async sendCorrection() {

      if (!this.response || this.corrected_class.value === '' || this.corrected_class.value === this.response.data.class) {
        console.error(this.corrected_class)
        console.error(this.response.data.class)
        this.corrected_thankyou.value = "Correction invalide !"
        return
      }
      try {
        const formData = new FormData();
        formData.append("class_override", this.corrected_class)
        formData.append("mass", this.meal_mass)

        formData.append("img_str", this.response.data.img_str)

        const res = await axios.post('http://localhost:5001/confirm_prediction_api', formData)

        this.corrected_thankyou = "Merci d'avoir corrigé la prédiction ! L'image représente donc un " + res.data.predicted_class_name + " d'une masse de " + res.data.mass +" grammes."



      } catch (e) {
        console.error(e)
      }
    }
  }
}
</script>

<style scoped>

</style>