<template>
    <button 
      @click="openModal" 
      class="btn btn-primary"
    >
      Open Transaction
    </button>
  
    <!-- Modal from previous example -->
    <div class="modal fade" id="transactionModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <div class="d-flex justify-content-between w-100 align-items-center">
              <h5 class="text-danger fw-bold">Rp {{ amount }}</h5>
              <span class="text-muted">{{ date }}</span>
            </div>
          </div>
          <div class="modal-body">
            <p class="text-secondary">{{ description }}</p>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-warning" 
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
  export default {
    data() {
      return {
        amount: 250000,
        date: '12/12/2024',
        description: 'Sample transaction description'
      }
    },
    methods: {
      openModal() {
        const modal = new bootstrap.Modal(document.getElementById('transactionModal'));
        modal.show();
      },
      editTransaction() {
        console.log('Transaction edited');
      },
      deleteTransaction() {
        console.log('Transaction deleted');
      }
    }
  }
  </script>