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
              <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                {{ isSubmitting ? 'Saving...' : 'Save Transaction' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import axios from 'axios'

const props = defineProps({
  category: {
    type: Object,
    required: true
  },
  modalId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['transaction-added', 'transaction-error'])

const formatDate = (date) => {
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear()
  return `${month}/${day}/${year}`
}

const formData = reactive({
  category_id: props.category.id,
  date: new Date(),
  amount: null,
  description: ''
})

const isSubmitting = ref(false)

const submitTransaction = async () => {
  isSubmitting.value = true

  console.log('Sending transaction:', {
    category_id: formData.category_id,
    date: formatDate(formData.date),
    amount: formData.amount,
    description: formData.description
  });

  try {
    const response = await axios.post('http://127.0.0.1:8000/transactions', {
      category_id: formData.category_id,
      date: formatDate(formData.date),
      amount: formData.amount,
      description: formData.description
    })

    // Emit success event
    emit('transaction-added', response.data)

    // Reset form
    formData.amount = null
    formData.date = new Date()
    formData.description = ''

    // Close modal (using Bootstrap's modal method)
    const modalElement = document.getElementById(props.modalId)
    const modalInstance = bootstrap.Modal.getInstance(modalElement)
    modalInstance.hide()
  } catch (error) {
    console.error('Full error details:', error.response);
    emit('transaction-error', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>