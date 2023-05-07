<script setup>
import M from 'materialize-css'
import { RouterView } from 'vue-router'
import AppNavbar from './components/AppNavbar.vue';
</script>

<template>
  <header>
    <AppNavbar :navlinks="navlinks" />
  </header>

  <RouterView />
</template>

<script>
export default {
  components: {
    AppNavbar
  },
  data() {
    return {
      navlinks: [
        { link: "/", name: "Home" },
        { link: "/about", name: "About" },
      ]
    }
  },
  mounted() {
    M.AutoInit()
  }
}
</script>