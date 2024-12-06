<!-- Bukan gini nanti -->

<template>
  <div
    class="modal fade"
    id="transactionCard"
    tabindex="-1"
    aria-labelledby="editEventModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editEventModalLabel">Edit Event</h5>
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
                Update Event
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TransactionCard",
  props: {
    eventData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        amount: 0,
        category_id: "",
        date: "",
      },
    };
  },
  watch: {
    eventData: {
      handler(newVal) {
        this.formData = { ...newVal };
      },
      immediate: true,
    },
  },
  methods: {
    submitForm() {
      this.$emit("update-event", this.formData);
    },
  },
};
</script>
