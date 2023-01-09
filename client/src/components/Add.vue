<script setup>
import { makeBlock } from '@vue/compiler-core';

defineProps({
  hyperlink: {
    type: String,
    required: true
  },
})
</script>

<template>
  <div class="wrapper">
    <div class="adding">
      <input v-model="link" placeholder="Вставь ссылку!" autocomplete="url" type="text" autofocus="true">
      <input v-model="description" placeholder="Добавь описание" type="text">
      <button v-on:click="addLink(link,description)">+</button>
    </div>
    <div>
      <h1>
        <a v-bind:href="hyperlink">{{hyperlink}}</a>
      </h1>
    </div>
  </div>
  
</template>

<style scoped>

input {
  font-size: 50px;
  font-weight: normal;
}
button{
  background-color: green;
  border: none;
  color: white;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 40px;
  margin: 2px 2px;
  border-radius: 50%;
  height: 50px;
  width: 50px;
}
.adding{
  display: flex;
  flex-direction: row; 
  justify-content: center; 
  align-items: center
}
.wrapper {
    display: flex;
    flex-direction: column; 
    justify-content: center; 
    align-items: center
  }
</style>
<script>
import axios from 'axios';

  export default {
    data(){
      return{
        link: null,
        description: null,
        all_links:''
      }
    },
    methods: {
      addLink (link,description) {
        console.log(link)
        console.log(description)
        const payload = {
          'url': link,
          'description': description
        }
        const path = "http://127.0.0.1:5000/shareit/api/v1.0/links"
        
        axios.post(path,payload).then(
          function (response){
            console.log(response)
          }
        );
       /* const path = "http://127.0.0.1:5000/api/links"
        axios.get(path)
          .then(function (response){
            console.log(response)
          })       
      */

      }
    
    }
  }
</script>