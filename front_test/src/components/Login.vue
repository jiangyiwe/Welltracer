<script>
//import getUserId from 'main';
import VueCookies from 'vue-cookies'
import {ref} from 'vue'

export default {
  name: "Login",

  setup() {
    let userId = ref(getUserId());
    if (userId.value === undefined) {
      userId.value = -1;
    }
    let message = ref("What's your User ID?");

    function setUserId() {
      if (!isNaN(userId.value) && userId.value > 0) {
        // set UserId
        $cookies.set("userId", userId.value);
      } else {
        message.value = "This is not a valid userId. Please enter an integer greater than 1.";
      }
    }

    function disconnect() {
      $cookies.remove("userId");
      userId = -1;
    }

    return {
      userId, message, setUserId, disconnect
    }
  },
  getUserId: getUserId(),
  //setUserId: setUserId(),

}

// getUserId returns userId >= 1 if the user is logged in (userId numerical and > 1), and -1 otherwise
function getUserId() {
  const userId = $cookies.get("userId");
  if (!userId || isNaN(userId) || userId < 1) {
    return -1;
  }
  else
    return userId;
}




let message2 = "nzejkjke fejfdlnfsdn"

</script>
<template id="template-login">

  <div>
    <p>Connectez vous avec votre numéro d'utilisateur. Il sera utilisé pour vous identifier.</p>
    <p>Votre numéro d'utilisateur est : {{userId}}</p>
    <input v-model="userId" type="number">
    <button @click="setUserId()">Se connecter</button>
    <button @click="disconnect()">Se déconnecter</button>
  </div>
</template>
<style scoped>

</style>