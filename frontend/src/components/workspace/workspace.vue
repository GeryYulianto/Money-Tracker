<script setup>
import { ref } from 'vue';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

const date = ref();
// defineProps({
//   msg: {
//     type: String,
//     required: true,
//   },
// })
</script>

<script>
    const app = Vue.createApp({
        components: { VueDatePicker },
    }).mount("#app");
</script>

<template>
    <div class="filter d-flex">
        <div class='filter-date'>
            <div class="start-date">
                <Datepicker v-model="date" />
            </div>
            <div class="end-date">
                <Datepicker v-model="date" />
            </div>
            <button type="submit">Filter</button>
        </div>
    </div>
  </template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
