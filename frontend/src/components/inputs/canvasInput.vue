<template>
  <canvas
    ref="canvas"
    class="canvas"
    width="400"
    height="300"
    @mousedown="startDrawing"
    @mouseup="stopDrawing"
    @mousemove="draw"
  ></canvas>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

let isDrawing = ref(false)
let x = ref(0)
let y = ref(0)

const startDrawing = (event: any) => {
  isDrawing.value = true
  const canvas = event.target
  const ctx = canvas.getContext('2d')
  x.value = event.clientX - canvas.offsetLeft
  y.value = event.clientY - canvas.offsetTop
  ctx.beginPath()
  ctx.moveTo(x.value, y.value)
}

const stopDrawing = () => {
  isDrawing.value = false
}

const draw = (event: any) => {
  const canvas = event.target
  if (!isDrawing.value || !canvas) return
  const ctx = canvas.getContext('2d')
  const newX = event.clientX - canvas.offsetLeft
  const newY = event.clientY - canvas.offsetTop
  ctx.lineTo(newX, newY)
  ctx.strokeStyle = '#000'
  ctx.lineWidth = 3
  ctx.stroke()
  x.value = newX
  y.value = newY
}

const clearCanvas = () => {
  const canvas = document.querySelector('canvas')
  const ctx = canvas?.getContext('2d')
  if (ctx && canvas) {
    ctx.fillStyle = '#fff'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
  }
}

onMounted(clearCanvas)
</script>

<style scoped>
.canvas {
  border: 2px solid #ccc;
}
</style>
