<script setup>
import { ref } from "vue"; // ref untuk var reaktif 
import Datepicker from "@vuepic/vue-datepicker";
import formTransaction from "../form_transaction/formTransaction.vue";
import transactionCard from "../transaction_card/transactionCard.vue";
import "@vuepic/vue-datepicker/dist/main.css";

// variabel reaktif
const startDate = ref();
const endDate = ref();
const selectedEvent = ref(null); // menyimpan transaksi yang dipilih

// array kategori
const categories = [
  { id: 1, name: 'Utilities', class: 'table-primary' },
  { id: 2, name: 'Education', class: 'table-success' },
  { id: 3, name: 'Entertainment', class: 'table-warning' },
  { id: 4, name: 'Food', class: 'table-info' },
  { id: 5, name: 'Health', class: 'table-danger' }
];
</script>

<script>
import axios from "axios";

// Import components
export default {
  components: {
    Datepicker,
    formTransaction,
    transactionCard,
  },

  // array transaction akan menyimpan daftar transaksi
  data() {
    return {
      transactions: [],
    };
  },

  methods: {
    // logout
    async logout() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/logout");
        console.log(response.data);

        // redirect ke login
        if (response.status == 200) {
          this.$router.push("/");
        } else {
          console.error("Login error:", response);
        }
      } catch (error) {
        console.error("Login error:", error);
      }
    },

    // axios get /transactions
    fetchTransactions() {
      const path = "http://127.0.0.1:8000/transactions";
      axios.get(path)
        .then((res) => {
          this.transactions = res.data;
          console.log(res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },

    // add new transaction
    handleAddEvent(eventData) {
      console.log("Adding event:", eventData);
      const modal = bootstrap.Modal.getInstance(
        document.getElementById(`formTransaction${eventData.category_id}`)
      );
      modal.hide();
    },

    // edit transaction
    handleEditEvent(eventData) {
      console.log("Updating event:", eventData);
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("transactionCard")
      );
      modal.hide();
    },

    // open modal edit (?)
    openEditModal(transaction) {
      this.selectedEvent = transaction;
      const modal = new bootstrap.Modal(
        document.getElementById("transactionCard")
      );
      modal.show();
    },

  },
  // saat komponent dibuat, panggil fetchTransactions
  created() {
    this.fetchTransactions();
  },
};
</script>

<template>
  <!-- Import Modal Component -->

  <!-- modal form untuk setiap kategori -->
  <formTransaction 
    v-for="category in categories" 
    :key="category.id"
    :category="category"
    :modal-id="`formTransaction${category.id}`"
    @submit-event="handleAddEvent" 
  />

  <!-- modal card untuk edit -->
  <transactionCard :event-data="selectedEvent" @update-event="handleEditEvent" />

  <!-- Filter -->
  <div class="filter d-flex m-3">
    <div class="filter-date d-flex gap-2 me-2">
      <div class="start-date">
        <Datepicker v-model="startDate" />
      </div>
      <div class="end-date">
        <Datepicker v-model="endDate" />
      </div>
    </div>
    <div class="category-filter d-flex gap-2 me-2">
      <div class="form-check w-100 mw-100">
        <input
          class="form-check-input"
          type="checkbox"
          value="utilities"
          id="flexCheckChecked"
          checked
        />
        <label class="form-check-label" for="flexCheckChecked">
          Utilities
        </label>
      </div>
      <div class="form-check w-100 mw-100">
        <input
          class="form-check-input"
          type="checkbox"
          value="education"
          id="flexCheckChecked"
          checked
        />
        <label class="form-check-label" for="flexCheckChecked">
          Education
        </label>
      </div>
      <div class="form-check w-100 mw-100">
        <input
          class="form-check-input"
          type="checkbox"
          value="entertainment"
          id="flexCheckChecked"
          checked
        />
        <label class="form-check-label" for="flexCheckChecked">
          Entertainment
        </label>
      </div>
      <div class="form-check w-100 mw-100">
        <input
          class="form-check-input"
          type="checkbox"
          value="food"
          id="flexCheckChecked"
          checked
        />
        <label class="form-check-label" for="flexCheckChecked"> Food </label>
      </div>
      <div class="form-check w-100 mw-100">
        <input
          class="form-check-input"
          type="checkbox"
          value="health"
          id="flexCheckChecked"
          checked
        />
        <label class="form-check-label" for="flexCheckChecked"> health </label>
      </div>
    </div>
    <button type="submit" class="btn btn-success">Filter</button>
    <button
        class="btn btn-outline-dark"
        type="button"
        v-on:click="logout()">
        Logout
      </button>
  </div>

  <!-- menampilkan transaksi -->
  <table class="table m-5">
    <thead>
      <tr>
        <th v-for="category in categories" :key="category.id" :class="category.class">
          {{ category.name }}
          <button 
            type="button" 
            class="btn btn-dark"
            data-bs-toggle="modal" 
            :data-bs-target="`#formTransaction${category.id}`"
          >+</button>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="transaction in transactions">
        <th v-for="categoryId in [1, 2, 3, 4, 5]" :key="categoryId">
          <div
            v-if="categoryId === transaction.category_id"
            class="card"
            style="width: 18rem"
          >
            <div class="card-body">
              <h5 class="card-title">{{ transaction.amount }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">
                {{ transaction.date }}
              </h6>
              <button class="btn btn-primary" @click="openEditModal(transaction)">See More</button>
            </div>
          </div>
        </th>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
th button {
  padding: 0rem 0.3rem;
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
