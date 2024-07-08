<template>
  <div class="tab-content">
    <div class="definition">
      <header>
        <h4>{{ title }}</h4>
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
