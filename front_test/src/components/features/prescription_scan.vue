<template>
  <p>Send the picture of your meal here!</p>

  <picture-input
      ref="pictureInput"
      width="600"
      height="600"
      margin="16"
      accept="image/jpeg,image/png"
      size="10"
      button-class="btn"
      :custom-strings="{
        upload: '<h1>Uploadez une photo de votre prescription ici !</h1>',
        drag: 'Uploadez une photo de votre prescription ici !'
      }"
      @change="onChange">
  </picture-input>

  <button class="button-3" @click="sendPicture()">Envoyer l'image au serveur</button>

  <div v-if="response">
    <div v-if="response.data">
      {{response.data.texts}}
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
        const res = await axios.post("http://localhost:5001/detect_text_api", formData, {
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