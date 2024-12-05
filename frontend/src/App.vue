<script setup>
import { RouterView } from 'vue-router';
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

  <RouterView />
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

  }
}
</script>
