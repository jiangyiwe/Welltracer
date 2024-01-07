<script>
import {ref} from 'vue'

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

    <div v-if="getUserId() !== -1">
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
  border: 3px outset hsla(160, 100%, 37%, 1);
  border-radius: 2.5em;
  padding: 1em;
  background-color: hsla(160, 100%, 37%, 0.2);

  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.login-subcontainer {
  display: flex;
  justify-content: flex-end;
  gap: 1em;
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


/* CSS */
.button-3 {
   appearance: none;
   background-color: #2ea44f;
   border: 1px solid rgba(27, 31, 35, .15);
   border-radius: 6px;
   box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
   box-sizing: border-box;
   color: #fff;
   cursor: pointer;
   display: inline-block;
   font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
   font-size: 14px;
   font-weight: 600;
   line-height: 20px;
   padding: 6px 16px;
   text-align: center;
   user-select: none;
   -webkit-user-select: none;
   touch-action: manipulation;
   white-space: nowrap;
 }

.button-3:focus:not(:focus-visible):not(.focus-visible) {
  box-shadow: none;
  outline: none;
}

.button-3:hover {
  background-color: #2c974b;
}

.button-3:focus {
  box-shadow: rgba(46, 164, 79, .4) 0 0 0 3px;
  outline: none;
}

.button-3:disabled {
  background-color: #94d3a2;
  border-color: rgba(27, 31, 35, .1);
  color: rgba(255, 255, 255, .8);
  cursor: default;
}

.button-3:active {
  background-color: #298e46;
  box-shadow: rgba(20, 70, 32, .2) 0 1px 0 inset;
}
</style>