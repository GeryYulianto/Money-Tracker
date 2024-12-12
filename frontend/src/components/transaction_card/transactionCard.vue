<template>
  <div 
    class="modal fade" 
    :id="`transactionCard${eventData.id}`" 
    tabindex="-1"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <div class="d-flex justify-content-between w-100 align-items-center">
            <h5 class="text-danger fw-bold">Rp {{ eventData.amount }}</h5>
            <span class="text-muted">{{ eventData.date }}</span>
          </div>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p class="text-secondary">{{ eventData.description }}</p>
        </div>
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-warning" 
            data-bs-dismiss="modal"
            @click="editTransaction"
          >
            <i class="bi bi-pencil me-2"></i>Edit
          </button>
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="deleteTransaction"
          >
            <i class="bi bi-trash me-2"></i>Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    eventData: {
      type: Object,
      required: true
    },
    modalId: {
      type: String,
      required: true
    }
  },
  methods: {
    editTransaction() {
      this.$emit('edit-transaction', this.eventData);
    },
    async deleteTransaction() {
      try {
        const token = localStorage.getItem('jwt_token');
        await axios.delete(`http://127.0.0.1:8000/transactions`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          data: {
            "transaction_id": this.eventData.transaction_id
          }
        });
        this.$emit('delete-transaction');
      } catch (error) {
        console.error("Delete error:", error);
      }
    }
  }
}
</script>