<template>


  {{  response }}
</template>

<script>
import axios from 'axios'
export default {
  name: "find_a_doctor",
  data() {
    return {
      response: ''
    }
  },
  mounted (){
    this.findDoc()
  },
  methods: {
    async findDoc() {

      try {
        const res = await axios.get("http://localhost:5001/search")
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