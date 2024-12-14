<script setup>
import { ref, onMounted } from "vue"; // ref untuk var reaktif
import Datepicker from "@vuepic/vue-datepicker";
import formTransaction from "../form_transaction/formTransaction.vue";
import transactionCard from "../transaction_card/transactionCard.vue";
import editTransaction from "../transaction_card/editTransaction.vue";
import "@vuepic/vue-datepicker/dist/main.css";

// variabel reaktif
const selectedEvent = ref(null); // menyimpan transaksi yang dipilih

// array kategori
const categories = [
  { id: 1, name: "Utilities", class: "table-primary" },
  { id: 2, name: "Education", class: "table-success" },
  { id: 3, name: "Entertainment", class: "table-warning" },
  { id: 4, name: "Food", class: "table-info" },
  { id: 5, name: "Health", class: "table-danger" },
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
      startDate: null,
      endDate: null,
      filteredCategories: [
        { id: 1, name: "Utilities", class: "table-primary" },
        { id: 2, name: "Education", class: "table-success" },
        { id: 3, name: "Entertainment", class: "table-warning" },
        { id: 4, name: "Food", class: "table-info" },
        { id: 5, name: "Health", class: "table-danger" },
      ],
    };
  },
  computed: {
    /**
     * Filtered transactions that belong to the currently selected filtered categories
     */
    filteredTransactions() {
      return this.transactions.filter((transaction) =>
        this.filteredCategories.some(
          (category) => category.id === transaction.category_id
        )
      );
    },
  },

  methods: {
    formatDate(date) {
      if (!date) return null;
      const d = new Date(date);
      const month = String(d.getMonth() + 1).padStart(2, "0");
      const day = String(d.getDate()).padStart(2, "0");
      const year = d.getFullYear();
      return `${month}/${day}/${year}`;
      // return `${year}-${month}-${date}`;
    },

    async logout() {
      try {
        const token = localStorage.getItem("jwt_token");
        const response = await axios.get("http://127.0.0.1:8000/logout", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status === 200) {
          localStorage.removeItem("jwt_token");
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Logout error:", error);
      }
    },

    // axios get /transactions
    async fetchTransactions(args = null) {
      try {
        const token = localStorage.getItem("jwt_token");
        const queryString = args ? new URLSearchParams(args).toString() : "";
        const response = await axios.get(
          `http://127.0.0.1:8000/transactions?${queryString}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.transactions = response.data;
        // console.log("Transactions:", this.transactions);
      } catch (error) {
        if (error.response?.status === 401) {
          localStorage.removeItem("jwt_token");
          this.$router.push("/");
        }
        console.error("Fetch error:", error);
      }
    },

    // Update handleAddEvent to refresh transactions
    handleAddEvent(eventData) {
      console.log(eventData);
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
      console.log(eventData);
      this.fetchTransactions();
      const modal = bootstrap.Modal.getInstance(
        document.getElementById(`editTransaction${eventData.transaction_id}`)
      );
      if (modal) {
        modal.hide();
      }
    },

    // handleEditEvent(eventData) {
    //   console.log(eventData);
    //   // console.log('Transaction ID:', eventData.id);
    //   // console.log('Transaction_ID:', eventData.transaction_id);

    //   // Refresh transactions after editing
    //   this.fetchTransactions();
    //   const modal = bootstrap.Modal.getInstance(
    //     document.getElementById(`transactionCard${eventData.transaction_id}`)
    //   );
    //   if (modal) {
    //     modal.hide();
    //   }
    // },

    handleEditEvent(transaction) {
      if (transaction) {
        // Close current modal first
        const currentModal = bootstrap.Modal.getInstance(
          document.getElementById(
            `transactionCard${transaction.transaction_id}`
          )
        );
        if (currentModal) {
          currentModal.hide();
        }
        // Open edit modal
        const editModal = new bootstrap.Modal(
          document.getElementById(
            `editTransaction${transaction.transaction_id}`
          )
        );
        editModal.show();
      }
    },
    handleTransactionClick(transaction) {
      const modal = new bootstrap.Modal(
        document.getElementById(`transactionCard${transaction.transaction_id}`)
      );
      modal.show();
    },

    // Add method to handle transaction deletion
    handleDeleteEvent() {
      this.fetchTransactions();
    },

    //Buat filter
    async handleFilterEvent() {
      try {
        const token = localStorage.getItem("jwt_token");
        let categoriesFiltered = {};
        Object.values(this.selectedCategories).forEach(function (val, index) {
          categoriesFiltered[val] = true;
        });
        const categoryQueryString = new URLSearchParams(
          categoriesFiltered
        ).toString();
        const categoryResponse = await axios.get(
          `http://127.0.0.1:8000/category?${categoryQueryString}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.filteredCategories = categoryResponse["data"];
        // console.log(this.filteredCategories);

        const args = {
          start_date: this.formatDate(this.startDate),
          end_date: this.formatDate(this.endDate),
        };
        this.fetchTransactions(args);
      } catch (error) {
        console.error("Filter error:", error);
      }
    },

    // Update to open edit modal
    // openEditModal(transaction) {
    //   console.log(transaction);
    //   // Ensure transaction is not null before setting
    //   if (transaction) {
    //     const modal = new bootstrap.Modal(
    //       document.getElementById(`editTransaction${transaction.id}`)
    //     );
    //     modal.show();
    //   }
    // },

    getTotalSpentForCategory(categoryId) {
      return this.transactions
        .filter((transaction) => transaction.category_id === categoryId)
        .reduce((total, transaction) => total + transaction.amount, 0);
    },

    isOverBudget(category) {
      const totalSpent = this.getTotalSpentForCategory(category.id);
      return totalSpent > category.budget;
    },
  },

  // saat komponent dibuat, panggil fetchTransactions
  created() {
    // console.log(this.transactions)
    if (!localStorage.getItem("jwt_token")) {
      this.$router.push("/");
      return;
    }
    this.fetchTransactions();
  },
};
</script>

<template>
  <formTransaction
    v-for="category in categories"
    :key="category.id"
    :category="category"
    :modal-id="`formTransaction${category.id}`"
    @submit-event="handleAddEvent"
  />

  <!-- <transactionCard
    v-for="transaction in transactions"
    :key="transaction.id"
    :event-data="transaction"
    :modal-id="`transactionCard${transaction.id}`"
    @edit-transaction="openEditModal"
    @delete-transaction="handleDeleteEvent"
  /> -->

  <transactionCard
    v-for="transaction in transactions"
    :key="transaction.transaction_id"
    :event-data="transaction"
    :modal-id="`transactionCard${transaction.transaction_id}`"
    @edit-event="handleEditEvent"
    @delete-transaction="handleDeleteEvent"
  />

  <!-- <editTransaction
    v-for="transaction in transactions"
    :key="transaction.id"
    :transaction-data="transaction"
    :modal-id="`editTransaction${transaction.id}`"
    @update-transaction="handleUpdateEvent"
  /> -->

  <editTransaction
    v-for="transaction in transactions"
    :key="transaction.transaction_id"
    :transaction-data="transaction"
    :modal-id="`editTransaction${transaction.transaction_id}`"
    @update-transaction="handleUpdateEvent"
  />

  <!-- Navigation & Filters -->
  <nav class="bg-white shadow-sm mb-4 rounded-3">
    <div class="container-fluid p-4">
      <div class="d-flex flex-column flex-md-row gap-4 align-items-md-center">
        <!-- Date filters -->
        <div class="d-flex gap-3 flex-grow-1">
          <Datepicker v-model="startDate" class="datepicker-custom" />
          <Datepicker v-model="endDate" class="datepicker-custom" />
        </div>

        <!-- Category filters -->
        <div class="d-flex flex-wrap gap-3 flex-grow-1">
          <div
            class="form-check"
            v-for="category in categories"
            :key="category.id"
          >
            <input
              class="form-check-input"
              type="checkbox"
              :value="category.name"
              v-model="selectedCategories"
            />
            <label class="form-check-label">{{ category.name }}</label>
          </div>
        </div>

        <!-- Action buttons -->
        <div class="d-flex gap-3">
          <button
            class="btn btn-success px-4 py-2"
            type="button"
            @click="handleFilterEvent"
          >
            Filter
          </button>
          <button
            class="btn btn-outline-danger px-4 py-2"
            type="button"
            @click="logout()"
          >
            <i class="bi bi-box-arrow-right me-2"></i>Logout
          </button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Transaction Table -->
  <div class="table-responsive">
    <table class="table table-hover border">
      <thead class="table-light">
        <tr>
          <th
            v-for="category in filteredCategories"
            :key="category.id"
            :class="[
              { 'table-danger': isOverBudget(category) },
              category.class,
              'p-3',
            ]"
          >
            <div class="d-flex justify-content-between align-items-center">
              <div>
                {{ category.name }}
                <span v-if="isOverBudget(category)" class="badge bg-danger ms-2"
                  >Overbudget</span
                >
              </div>
              <button
                type="button"
                class="btn btn-dark btn-sm px-2"
                data-bs-toggle="modal"
                :data-bs-target="`#formTransaction${category.id}`"
              >
                +
              </button>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in filteredTransactions" :key="transaction.id">
          <td
            v-for="category in filteredCategories"
            :key="category.id"
            :class="[category.class, 'p-3']"
          >
            <div
              v-if="transaction.category_id === category.id"
              class="card border-0 shadow-sm"
              :data-category-id="category.id"
            >
              <div class="card-body p-3">
                <h5 class="card-title fw-bold mb-2">
                  Rp {{ transaction.amount }}
                </h5>
                <h6 class="card-subtitle text-muted mb-3 small">
                  {{ transaction.date }}
                </h6>

                <!-- <button
                  class="btn btn-primary btn-sm w-100"
                  data-bs-toggle="modal"
                  :data-bs-target="`#transactionCard${transaction.id}`"
                >
                  <i class="bi bi-eye me-2"></i>See More
                </button> -->

                <button
                  class="btn btn-primary btn-sm w-100"
                  @click="handleTransactionClick(transaction)"
                >
                  <i class="bi bi-eye me-2"></i>See More
                </button>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* .datepicker-custom :deep(.dp__input) {
 border: 1px solid #dee2e6;
 border-radius: 6px;
 padding: 8px 12px;
 font-size: 14px;
 width: 130px;
 transition: border-color 0.2s;
}

.datepicker-custom :deep(.dp__input:focus) {
 border-color: #86b7fe;
 outline: 0;
 box-shadow: 0 0 0 0.25rem rgba(13,110,253,.25);
} */

.form-check-input:checked {
  background-color: #198754;
  border-color: #198754;
}

.btn {
  font-weight: 500;
  letter-spacing: 0.3px;
  transition: all 0.2s;
}

.btn-outline-danger {
  border-width: 2px;
}

.btn-outline-danger:hover {
  transform: translateY(-1px);
}

.btn-sm {
  font-size: 1rem;
  line-height: 1;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}

@media (min-width: 1024px) {
  .card {
    width: 18rem;
  }
}
</style>
