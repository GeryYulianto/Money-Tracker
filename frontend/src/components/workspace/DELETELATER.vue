<script setup>
import { ref } from "vue";
import axios from "axios";
import Datepicker from "@vuepic/vue-datepicker";
import formTransaction from "../form_transaction/formTransaction.vue";
import transactionCard from "../transaction_card/transactionCard.vue";
import EditTransaction from "../components/editTransaction.vue";
import "@vuepic/vue-datepicker/dist/main.css";

// Use ref for selectedEvent
const selectedEvent = ref(null);

// ... rest of existing setup script ...
</script>

<script>
export default {
  components: {
    Datepicker,
    formTransaction,
    transactionCard,
    EditTransaction,
  },

  methods: {
    // ... other methods ...

    openEditModal(transaction) {
      // Use .value to set ref
      this.selectedEvent = { ...transaction };
      const modal = new bootstrap.Modal(
        document.getElementById("editTransaction")
      );
      modal.show();
    },

    handleUpdateEvent(updatedTransaction) {
      this.fetchTransactions();
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("editTransaction")
      );
      if (modal) {
        modal.hide();
      }
    },

    handleDeleteEvent() {
      this.fetchTransactions();
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("transactionCard")
      );
      if (modal) {
        modal.hide();
      }
    },
  },
};
</script>