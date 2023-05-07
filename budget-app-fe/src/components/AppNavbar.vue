<script>
import AppLink from './AppLink.vue'

export default {
  name: "AppNavbar",
  props: {
    navlinks: {
      type: Array,
      required: true,
    }
  },
  components: { AppLink }
}
</script>

<template>
  <!-- <nav>
    <div class="nav-wrapper" style="padding-left: 10px; padding-right: 10px;">
      <a href="#" class="brand-logo">Budget Manager</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <AppLink tag="li" active-class="active" to="/">Home</AppLink>
        <AppLink tag="li" active-class="active" to="/about">About</AppLink>
      </ul>
    </div>
  </nav> -->
  <nav>
    <div class="nav-wrapper">
      <a href="#!" class="brand-logo">Logo</a>
      <a href="#" data-target="mobile-demo" class="sidenav-trigger"><i class="material-icons">menu</i></a>
      <ul class="right hide-on-med-and-down">
        <AppLink tag="li" active-class="active" v-for="(item, index) in navlinks" :key="index" :to="item.link">{{
          item.name }}</AppLink>
      </ul>
    </div>
  </nav>

  <ul class="sidenav" id="mobile-demo">
    <AppLink tag="li" active-class="active" v-for="(item, index) in navlinks" :key="index" :to="item.link">{{ item.name }}
    </AppLink>
  </ul>
</template>