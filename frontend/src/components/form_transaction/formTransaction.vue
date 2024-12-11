<template>
  <div class="modal fade" :id="modalId" tabindex="-1" :aria-labelledby="`${modalId}Label`" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">

        <!-- header untuk modal berdasarkan id dan category name nya -->
        <div class="modal-header">
          <h5 class="modal-title" :id="`${modalId}Label`">Add New {{ category.name }} Transaction</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="submitTransaction">
            <div class="mb-3">
              <label for="date" class="form-label">Date</label>
              <Datepicker 
                v-model="formData.date"
                :format="formatDate" 
                :auto-apply="true"
                input-class-name="form-control"
              />
            </div>

            <div class="mb-3">
              <label for="amount" class="form-label">Amount</label>
              <input 
                type="number" 
                step="0.01" 
                class="form-control" 
                id="amount" 
                v-model.number="formData.amount"
                required
              >
            </div>

            <div class="mb-3">
              <label for="desc" class="form-label">Description</label>
              <textarea 
                class="form-control" 
                id="desc" 
                v-model="formData.description"
                required
              ></textarea>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary" data-bs-dismiss="modal" :disabled="isSubmitting">
                {{ isSubmitting ? 'Saving...' : 'Save Transaction' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import axios from 'axios'

export default {
  components: {
    Datepicker
  },

  props: {
    category: {
      type: Object,
      required: true
    },
    modalId: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      formData: {
        category_id: this.category.id,
        date: new Date(),
        amount: null,
        description: ''
      },
      isSubmitting: false
    }
  },

  methods: {
    formatDate(date) {
      const day = date.getDate().toString().padStart(2, '0')
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const year = date.getFullYear()
      return `${month}/${day}/${year}`
    },

    async submitTransaction() {
      this.isSubmitting = true

      try {
        const token = localStorage.getItem('jwt_token')
        if (!token) {
          this.$router.push("/main")
          return
        }

        const response = await axios.post('http://127.0.0.1:8000/transactions', 
          {
            category_id: this.formData.category_id,
            date: this.formatDate(this.formData.date),
            amount: this.formData.amount,
            description: this.formData.description
          },
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )

        if (response.status === 200) {
          // Use nextTick to ensure DOM updates before emitting
          this.$nextTick(() => {
            this.$emit('submit-event', {
              category_id: this.formData.category_id
            });

            // Programmatically close the modal
            const modalElement = document.getElementById(this.modalId);
            if (modalElement) {
              const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
              modalInstance.hide();
            }
          });

          // Reset form data
          this.formData = {
            category_id: this.category.id,
            date: new Date(),
            amount: null,
            description: ''
          };
        }
      } catch (error) {
        console.error('Transaction error:', error)
        if (error.response?.status === 401) {
          this.$router.push("/")
        }
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>