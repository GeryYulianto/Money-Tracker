<script setup>
import { ref } from 'vue';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

const startDate = ref();
const endDate = ref()
// defineProps({
//   msg: {
//     type: String,
//     required: true,
//   },
// })
</script>

<script>
import axios from "axios";
const app = Vue.createApp({
    components: { VueDatePicker },
})

export default {
  data() {
    return {
      transactions: [],
    }
  },
  methods: {
    fetchTransactions() {
      const path = 'http://127.0.0.1:8000/transactions'
      axios
        .get(path)
        .then((res) => {this.transactions = res.data
          console.log(res.data)
        })
        .catch((err) => {
          console.error(err)
        })
    },
    //Add other methods
  },
  created() {
    this.fetchTransactions()
  }
}
</script>

<template>
    <div class="filter d-flex m-3">
        <div class='filter-date d-flex gap-2 me-2'>
            <div class="start-date">
                <Datepicker v-model="startDate" />
            </div>
            <div class="end-date">
                <Datepicker v-model="endDate" />
            </div>
        </div>
        <div class="category-filter d-flex gap-2 me-2">
          <div class="form-check w-100 mw-100"><input class="form-check-input" type="checkbox" value="utilities" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              Utilities
            </label>
          </div>
          <div class="form-check w-100 mw-100"><input class="form-check-input" type="checkbox" value="education" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              Education
            </label>
          </div>
          <div class="form-check w-100 mw-100"><input class="form-check-input" type="checkbox" value="entertainment" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              Entertainment
            </label>
          </div>
          <div class="form-check w-100 mw-100"><input class="form-check-input" type="checkbox" value="food" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              Food
            </label>
          </div>
          <div class="form-check w-100 mw-100"><input class="form-check-input" type="checkbox" value="health" id="flexCheckChecked" checked>
            <label class="form-check-label" for="flexCheckChecked">
              health
            </label>
          </div>
        </div>
        <button type="submit" class="btn btn-success">Filter</button>
    </div>
    <table class="table m-5">
      <thead>
        <tr>
          <th scope="col" class="table-primary">Utilities <button class="btn btn-dark">+</button></th>
          <th scope="col" class="table-success">Education <button class="btn btn-dark">+</button></th>
          <th scope="col" class="table-warning">Entertainment <button class="btn btn-dark">+</button></th>
          <th scope="col" class="table-info">Food <button class="btn btn-dark">+</button></th>
          <th scope="col" class="table-danger">Health <button class="btn btn-dark">+</button></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions">
          <th v-for="categoryId in [1, 2, 3, 4, 5]" :key="categoryId">
            <div v-if="categoryId === transaction.category_id" class="card" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">{{ transaction.amount }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ transaction.date }}</h6>
                <button class="btn btn-primary">See More</button>
              </div>
            </div>
          </th>
        </tr>
      </tbody>
    </table>
  </template>

<style scoped>
th button {
  padding: 0rem 0.3rem; /* Adjust padding as needed */
}

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
