<template>
  <p v-if="!response">Uploadez une photo de votre repas ici !</p>

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

  <button class="button-3" @click="sendPicture()">Envoyer l'image au serveur</button>

  <div v-if="response">
    <div v-if="response.data">
      <p>Votre repas appartient à la catégorie : {{response.data.class}}</p>
      <p>D'après vos entrées, votre portion contient les nutriments suivants :</p>

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
      response: ''
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
        const res = await axios.post("http://localhost:5001/predict_img_api", formData, {
          headers: this.image.target.files[0].type
        })
        this.response = res

      } catch (e) {
        console.error(e)
      }
    }
  }
}
</script>

<style scoped>

</style>