<template>
  <div class="tab-content">
    <div class="definition">
      <header>
        <div class="header-title">
          <h4>{{ title }}</h4>
        </div>
        <hr>
      </header>
    </div>
    <br>
    <slot/>
  </div>
</template>
<script lang="ts">
export default {
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>
