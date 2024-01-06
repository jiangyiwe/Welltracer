
<style scoped>

.flexc {
  display: flex;
  flex-wrap: wrap;
}
.cell {
  width: 50%;
  padding: 3em;
}

</style>

<template>
  <div><p>Messages système</p>
    <p v-html="msg"></p>
  </div>

  <div>
    {{errorMessage}}
  </div>

  <div class="flexc">
    <div class="cell">
      <h3 class="title">Vidéos aléatoires</h3>
      <div>
        <span :id="random_vids"></span>
        <div v-for="video in random_vids">
          <p>{{video.class}}</p>
          <p>{{ video.filename }}</p>
          <a :href="`localhost:5001${video.url}`"> Accéder à la vidéo sur le server</a>
          <button @click="recordWatch(video.class, video.filename)">Enregistrer une visualisation</button>
        </div>
      </div>

    </div>


    <div class="cell">
      <h3 class="title">Vidéos suggérées</h3>
      <button @click="recommend()">Me suggérer une vidéo</button>
      <div v-if="recommendation">
        <div v-for="video in recommendation">
          <p>{{video.class}}</p>
          <p>{{ video.filename }}</p>
          <a :href="`localhost:5001${video.url}`"> Accéder à la vidéo sur le server</a>
          <button @click="recordWatch(video.class, video.filename)">Enregistrer une visualisation</button>
        </div>
      </div>

    </div>

    <div class="cell">
      <h3 class="title">Accéder à une vidéo</h3>
      <div>
        ajouter un videoplayer
      </div>
    </div>
    <div class="cell">
      <h3 class="title">Historique de vidéos </h3>
      <div style="display: flex; flex-wrap: wrap">
        <div v-for="video in history" style="padding: rem; width: 33%">
          <p>Cl: {{video.video_class}}</p>
          <p>User: {{video.user_id}}</p>
        </div>

      </div>
    </div>

  </div>




</template>

<script >
import axios from 'axios';
import { getUserId } from '../Login.vue'

export default {
  name: "home_fitness",
  data() {
    return {
      video: '',
      msg: '',
      history: '',
      errorMessage: '',
      random_vids: [],
      recommendation: null,
      count: 1
    }
  },
  methods: {
    async getRandomVideos(){
      const path= "http://localhost:5001/random_videos"


      try {
        const res = await axios.get(path);
        this.random_vids = res.data;
      } catch (error) {
        this.errorMessage = error;
        console.error(error);
      }

    },
    getVideo(video_class, video_filename) {
      const path = `http://localhost:5001/${video_class}/${video_filename}`
    },
    async recordWatch(video_class, video_filename){
      const path = "http://localhost:5001/record_watch"
      if (getUserId() < 1) {
        this.errorMessage="You need to log in!"
        console.error(this.msg);
        return
      }

      // POST
      try {
        const res = await axios.post(path, {
          video_class: video_class,
          video_filename: video_filename,
          user_id: getUserId()
        })
        console.log(res)
        this.watchHistory()
      } catch (e) {
        this.errorMessage = e
        console.error(e)
      }

    },
    watchHistory() {
      const path = 'http://localhost:5001/history'
      axios.get(path)
          .then((res) => {
            this.history = res.data;
          })
          .catch((error) => {
            this.errorMessage = error;
            console.error(error);
          });
    },
    async recommend() {
      if (getUserId() < 1) {
        return;
      }
      const path = `http://localhost:5001/recommend?user_id=${getUserId()}`
      try {
        const res = await axios.get(path);
        this.recommendation = res.data;
        console.log(res.data);
      } catch (e) {
        this.errorMessage = e;
        console.error(e);
      }
    },
    testMethod() {
      this.msg = 'OK';
    }

  },
  mounted() {
    this.watchHistory();
    this.getRandomVideos();
    this.testMethod();
  }


}
</script>



