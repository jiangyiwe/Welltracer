<script>
import {ref} from 'vue'
import VueCookies from 'vue-cookies'

export default {
  name: "Login",

  setup() {
    const userId = ref(getUserId());
    if (userId.value === undefined) {
      userId.value = -1;
    }
    const message = ref("Connectez vous avec votre numéro d'utilisateur. Il sera utilisé pour vous identifier.");

    function setUserId() {
      if (!isNaN(userId.value) && userId.value > 0) {
        // set UserId
        $cookies.set("userId", userId.value);
        message.value = "Vous êtes connectée."
      } else {
        message.value = "Ceci n'est pas un numéro d'utilisateur valide. Veuillez entrer un entier supérieur à 1.";
      }
    }

    function disconnect() {
      $cookies.remove("userId");
      userId.value = -1;
      message.value = "Connectez vous avec votre numéro d'utilisateur. Il sera utilisé pour vous identifier."
      try {
        const loginNavElem = document.getElementById("login");

          loginNavElem.style.maxWidth = loginNavElem.scrollWidth + 40 +"px";
      } catch (e) {}
    }

    return {
      userId, message, getUserId, setUserId, disconnect
    }
  },
  getUserId: getUserId(),
  //setUserId: setUserId(),

}

// getUserId returns userId >= 1 if the user is logged in (userId numerical and > 1), and -1 otherwise
export function getUserId() {
  const userId = $cookies.get("userId");
  if (!userId || isNaN(userId) || userId < 1) {
    return -1;
  }
  else
    return userId;
}




</script>
<template id="template-login">

  <div class="login-container">

    <div v-if="getUserId() !== -1" class="login-subcontainer">
      <h3 class="title">Vous êtes connecté en tant qu'utilisateur : {{userId}}</h3>
      <button class="button-3" role="button" @click="disconnect()">Se déconnecter</button>
    </div>
    <div v-else>
      <h3 class="title">{{message}}</h3>

      <div class="login-subcontainer">
        <input v-model="userId" style="flex-grow: 100" class="login-input" type="number">
        <button class="button-3" role="button"  @click="setUserId()">Se connecter</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.login-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  white-space: nowrap;
}

.login-subcontainer {
  display: flex;
  justify-content: flex-end;
  gap: 1em;
  align-items: stretch;
  white-space: nowrap;
}

.login-input {

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