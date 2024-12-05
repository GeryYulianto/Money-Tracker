<script setup>
import { ref, computed } from 'vue'

// Import Eksternal Component
import Login from './components/login/login.vue'
import FormTransaction from './components/form transaction/formTransaction.vue'

// Definisi Rute
const routes = {
  '/': Login,
  '/form-transaction': FormTransaction
}

const currentPath = ref(window.location.pathname)

const currentView = computed(() => {
  return routes[currentPath.value]
})

function navigate(path) {
  window.history.pushState({}, '', path)
  currentPath.value = path
}

window.addEventListener('popstate', () => {
  currentPath.value = window.location.pathname
})
</script>

<template>
  <!-- <div id="app">
    <button
      type="button"
      class="btn"
      @click="showModal"
    >
      Open Modal!
    </button>

    <FormTransaction
      v-show="isModalVisible"
      @close="closeModal"
    />
  </div>  -->

  <component :is="currentView" />
</template>

<!-- <script>
  export default {
    name: 'App',
    components: {
      FormTransaction,
    },
    data() {
      return {
        isModalVisible: false,
      };
    },
    methods: {
      showModal() {
        this.isModalVisible = true;
      },
      closeModal() {
        this.isModalVisible = false;
      }
    }
  };
</script> -->

<script>
export default {
  name: 'App',
  components: {
    Login,
  }
}
</script>
