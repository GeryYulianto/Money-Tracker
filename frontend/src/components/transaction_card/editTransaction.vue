<template>
  <div
    v-if="transactionData"
    class="modal fade"
    :id="`editTransaction${transactionData.id}`"
    tabindex="-1"
    aria-labelledby="editEventModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editEventModalLabel">Edit Transaction</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="edit-amount" class="form-label">Amount</label>
              <input
                type="number"
                class="form-control"
                id="edit-amount"
                v-model="formData.amount"
              />
            </div>
            <div class="mb-3">
              <label for="edit-category" class="form-label">Category</label>
              <select
                class="form-select"
                id="edit-category"
                v-model="formData.category_id"
              >
                <option value="1">Utilities</option>
                <option value="2">Education</option>
                <option value="3">Entertainment</option>
                <option value="4">Food</option>
                <option value="5">Health</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="edit-date" class="form-label">Date</label>
              <input
                type="date"
                class="form-control"
                id="edit-date"
                v-model="formData.date"
              />
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button type="submit" class="btn btn-primary">
                Update Transaction
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  props: {
    transactionData: {
      type: Object,
      default: () => ({
        id: null,
        amount: 0,
        category_id: "",
        date: ""
      })
    },
    modalId: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      formData: {
        id: null,
        amount: 0,
        category_id: "",
        date: "",
      },
    };
  },
  watch: {
    transactionData: {
      handler(newVal) {
        this.formData = { ...newVal };
      },
      immediate: true,
    },
  },
  methods: {
    formatDateForBackend(date) {
      if (!date) return null;
      const d = new Date(date);
      const day = String(d.getDate()).padStart(2, '0');
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const year = d.getFullYear();
      return `${day}/${month}/${year}`;
    },
    async submitForm() {
      try {
        const token = localStorage.getItem('jwt_token');
        const formattedDate = this.formatDateForBackend(this.formData.date);
        const formData = { ...this.formData, date: formattedDate };
        const response = await axios.put(`http://127.0.0.1:8000/transactions`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.$emit("update-transaction", response.data);
      } catch (error) {
        console.error("Update error:", error);
      }
    },
  },
};
</script>