<template>
  <!-- <div class="modal fade" :id="`transactionCard${eventData.id}`" tabindex="-1"> -->
  <div class="modal fade" :id="modalId" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow-sm">
        <div class="modal-header border-bottom-0 py-3">
          <div class="d-flex justify-content-between w-100 align-items-center">
            <h5 class="text-danger fw-bold mb-0">Rp {{ eventData.amount }}</h5>
            <span class="text-muted small">{{ eventData.date }}</span>
          </div>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body py-4">
          <p class="text-secondary mb-0">{{ eventData.description }}</p>
        </div>

        <div class="modal-footer border-top-0">
          <!-- <button
            type="button"
            class="btn btn-warning text-white fw-semibold"
            data-bs-dismiss="modal"
            @click="editTransaction"
          >
            <i class="bi bi-pencil me-2"></i>Edit
          </button> -->

          <button
            type="button"
            class="btn btn-warning text-white fw-semibold"
            @click="editTransaction"
          >
            <i class="bi bi-pencil me-2"></i>Edit
          </button>

          <button
            type="button"
            class="btn btn-danger fw-semibold"
            @click="deleteTransaction"
          >
            <i class="bi bi-trash me-2"></i>Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-content {
  border-radius: 12px;
}

.btn {
  padding: 8px 20px;
  border-radius: 6px;
}
</style>

<script>
import axios from "axios";

export default {
  props: {
    eventData: {
      type: Object,
      required: true,
    },
    modalId: {
      type: String,
      required: true,
    },
  },
  methods: {
    // editTransaction() {
    //   this.$emit("edit-transaction", this.eventData);
    // },

    editTransaction() {
      this.$emit("edit-event", this.eventData);
    },

    async deleteTransaction() {
      try {
        const token = localStorage.getItem("jwt_token");
        await axios.delete(`http://127.0.0.1:8000/transactions`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          data: {
            transaction_id: this.eventData.transaction_id,
          },
        });
        this.$emit("delete-transaction");
      } catch (error) {
        console.error("Delete error:", error);
      }
    },
  },
};
</script>
