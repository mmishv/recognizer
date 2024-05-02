<template>
  <div class="text-center">
    <v-snackbar
      v-if="text"
      location="top"
      :model-value="snackbar"
      multi-line
      timeout="8000"
      variant="elevated"
    >
      {{ text }}
      <template v-slot:actions>
        <v-btn color="red" variant="text" @click="snackbar = false" text="Close" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { shallowRef, watch } from 'vue'

const props = defineProps<{ isOpen?: boolean; text?: string }>()
const snackbar = shallowRef(false)

watch(
  () => props.isOpen,
  (newValue) => {
    snackbar.value = newValue
  }
)
</script>
