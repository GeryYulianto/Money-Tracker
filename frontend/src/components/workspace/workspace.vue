<script setup>
import { ref } from "vue"; // ref untuk var reaktif 
import Datepicker from "@vuepic/vue-datepicker";
import formTransaction from "../form_transaction/formTransaction.vue";
import transactionCard from "../transaction_card/transactionCard.vue";
import editTransaction from "../transaction_card/editTransaction.vue";
import "@vuepic/vue-datepicker/dist/main.css";

// variabel reaktif
// const startDate = ref(null);
// const endDate = ref(null);
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
    editTransaction,
  },

  // array transaction akan menyimpan daftar transaksi
  data() {
    return {
      transactions: [],
      selectedCategories: [],
      startDate : null,
      endDate: null
    };
  },

  methods: {
    formatDate(date) {
      if (!date) return null;
      const d = new Date(date);
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      const year = d.getFullYear();
      return `${month}/${day}/${year}`;
    },

    async logout() {
      try {
        const token = localStorage.getItem('jwt_token');
        const response = await axios.get('http://127.0.0.1:8000/logout', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 200) {
          localStorage.removeItem('jwt_token');
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Logout error:", error);
      }
    },

    // axios get /transactions
    async fetchTransactions(args=null) {
      try {
        const token = localStorage.getItem('jwt_token');
        const queryString = args ? new URLSearchParams(args).toString() : '';
        const response = await axios.get(`http://127.0.0.1:8000/transactions?${queryString}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.transactions = response.data;
        console.log("Transactions:", this.transactions);
      } catch (error) {
        if (error.response?.status === 401) {
          localStorage.removeItem('jwt_token');
          this.$router.push("/");
        }
        console.error("Fetch error:", error);
      }
    },

    // Update handleAddEvent to refresh transactions
    handleAddEvent(eventData) {
      // Refresh transactions after adding a new one
      this.fetchTransactions();
      const modal = bootstrap.Modal.getInstance(
        document.getElementById(`formTransaction${eventData.category_id}`)
      );
      if (modal) {
        modal.hide();
      }
    },

    // Update event to handle transaction update
    handleUpdateEvent(eventData) {
      this.fetchTransactions();
      const modal = bootstrap.Modal.getInstance(
        document.getElementById(`editTransaction${eventData.transaction_id}`)
      );
      if (modal) {
        modal.hide();
      }
    },

    // edit transaction
    handleEditEvent(eventData) {
      // Refresh transactions after editing
      this.fetchTransactions();
      const modal = bootstrap.Modal.getInstance(
        document.getElementById(`transactionCard${eventData.transaction_id}`)
      );
      if (modal) {
        modal.hide();
      }
    },

    // Add method to handle transaction deletion
    handleDeleteEvent() {
      this.fetchTransactions();
    },

    //Buat filter
    handleFilterEvent() {
      const args = {
        start_date: this.formatDate(this.startDate),
        end_date: this.formatDate(this.endDate)
        // categories: this.selectedCategories.join(',')
      };
      this.fetchTransactions(args);
    },

    // Update to open edit modal
    openEditModal(transaction) {
      // Ensure transaction is not null before setting
      if (transaction) {
        const modal = new bootstrap.Modal(document.getElementById(`editTransaction${transaction.id}`));
        modal.show();
      }
    },
  },

  // saat komponent dibuat, panggil fetchTransactions
  created() {
    if (!localStorage.getItem('jwt_token')) {
      this.$router.push("/");
      return;
    }
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

  <!-- modal card untuk see more -->
  <transactionCard 
    v-for="transaction in transactions"
    :key="transaction.id"
    :event-data="transaction" 
    :modal-id="`transactionCard${transaction.id}`"
    @edit-transaction="openEditModal"
    @delete-transaction="handleDeleteEvent"
  />

  <!-- modal edit transaction -->
  <editTransaction
    v-for="transaction in transactions"
    :key="transaction.id"
    :transaction-data="transaction"
    :modal-id="`editTransaction${transaction.id}`"
    @update-transaction="handleUpdateEvent"
  />

  <!-- Filter -->
  <div class="filter d-flex m-3">
      <div class="filter-date d-flex gap-2 me-2">
        <div class="start-date">
          <Datepicker v-model="startDate"/>
        </div>
        <div class="end-date">
          <Datepicker v-model="endDate"/>
        </div>
      </div>
      <div class="category-filter d-flex gap-2 me-2">
        <div class="form-check w-100 mw-100" v-for="category in categories" :key="category">
          <input
            class="form-check-input"
            type="checkbox"
            :value="category"
            v-model="selectedCategories"
          />
          <label class="form-check-label">
            {{ category.name }}
          </label>
        </div>
      </div>

      <button
        class="btn btn-success"
        type="button"
        v-on:click="handleFilterEvent">
        Filter
      </button>
    </div>
    <button
        class="btn btn-outline-dark"
        type="button"
        v-on:click="logout()">
        Logout
      </button>

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
              <button 
                class="btn btn-primary" 
                data-bs-toggle="modal" 
                :data-bs-target="`#transactionCard${transaction.id}`">
                See More
              </button>
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
