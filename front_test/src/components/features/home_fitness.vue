
<style scoped>

.flexc {
  display: flex;
  flex-wrap: wrap;
}
.cell {
  padding-right: 1em;
  padding-left: 1em;
  padding-bottom: 1em;
}
.videoPlayer {
  flex-grow: 1;
  max-width: 100%
}

.container {
  display: flex;
  align-items: flex-start;

  flex-flow: row wrap;
  padding-top: 2em;
  padding-bottom: 2em;
  margin-left: 2em;
  margin-right: 2em;
}

.cell-body {


  border: 3px outset hsla(160, 100%, 37%, 1);
  border-radius: 1.5em;
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

.button-3 {
  font-weight: 0;
  font-size: 12px;
}

</style>

<template>
  <div class="container">
    <div class="cell videoPlayer cell-body">

          <VideoPlayer
              :src="loadedVideo"
              controls
              :loop="true"
              :volume="0.6"
              :fluid="true"
              :autoplay="true"
          />
          <!--
          ...
          @mounted="..."
          @ready="..."
          @play="..."
          @pause="..."
          @ended="..."
          @seeking="..."
          ...-->


    </div>
    <div class="videoList">
      <div class="cell">
        <div class="recommendedVideos cell-body">
          <h3 class="title">Vidéos suggérées</h3>
          <button class="button-3" @click="recommend()">Me suggérer une vidéo</button>
          <div>
            {{ this.recommendMessage }}
          </div>
          <div v-if="recommendation">
            <div v-for="video in recommendation">
              <div style="display: flex; justify-content: space-between">
                <span>{{ video.filename }} </span>- <span style="text-align: end">{{video.class}}</span>
              </div>
              <button class="button-3" @click="loadedVideo = `http://localhost:5001${video.url}` "> Voir la vidéo dans le lecteur</button>
              <span style="padding-left: 0.5em"></span>
              <button class="button-3" @click="recordWatch(video.class, video.filename)">Enregistrer une visualisation</button>
            </div>
          </div>
        </div>

      </div>
      <div class="cell">
        <div class="randomVideos cell-body">
          <h3 class="title">Vidéos aléatoires</h3>
          <div>
            <div v-for="video in random_vids">
              <div style="display: flex; justify-content: space-between">
                <span>{{ video.filename }} </span>- <span style="text-align: end">{{video.class}}</span>
              </div>
              <button class="button-3" @click="loadedVideo = `http://localhost:5001${video.url}` "> Voir la vidéo dans le lecteur</button>
              <span style="padding-left: 0.5em"></span>
              <button class="button-3" @click="recordWatch(video.class, video.filename)">Enregistrer une visualisation</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <div class="flexc">


    <div class="cell">
      <h3 class="title">Historique de vidéos </h3>
      <div style="display: flex; flex-wrap: wrap">
        <div v-for="video in history" style="padding: 1rem; width: 16%">
          <p>Cl: {{video.video_class}}</p>
          <p>User: {{video.user_id}}</p>
        </div>

      </div>
    </div>
    <div class="cell">


    </div>

  </div>




</template>

<script >
import axios from 'axios';
import { getUserId } from '@/components/Login.vue'
import {VideoPlayer as VideoPlayer} from '@videojs-player/vue';
import 'video.js/dist/video-js.css'

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
      count: 1,
      recommendMessage: '',
      loadedVideo: ''
    }
  },
  methods: {
    async getRandomVideos(){
      const path= "http://localhost:5001/random_videos"


      try {
        const res = await axios.get(path);
        this.random_vids = res.data;
        this.loadedVideo = "http://localhost:5001/" + res.data[0].url
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
        this.recommendMessage = 'Voici ce qui vous est recommandé selon votre historique.'
      } catch (e) {
        this.errorMessage = e;
        console.error(e);
        this.recommendMessage = "Vous n'avez aucun historique, regardez quelques vidéos d'abord."
      }
    },
    testMethod() {
      this.msg = 'OK';
    }

  },
  components: {
    VideoPlayer
  },
  created() {
    this.watchHistory();
    this.getRandomVideos();
    this.testMethod();
  },


}
</script>



