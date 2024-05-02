<template>
  <div class="w-full px-10">
    <div class="py-8 mx-auto">
      <div class="text-gray-600 text-5xl mx-16 my-4">Recognizer</div>
    </div>
    <div class="flex flex-column w-full">
      <form class="p-10 bg-white rounded-lg w-full justify-center align-center">
        <v-row class="flex justify-center align-center">
          <v-file-input label="File input" v-model="fileInput" class="h-25 mx-4" />
          <div class="m-10"><canvas-input /></div>
        </v-row>
        <upper-error-snackbar :is-open="snackbar" :text="errorMessage" />
        <v-btn
          :onclick="recognize"
          variants="outlined"
          color="primary"
          class="w-full mt-2 font-weight-bold"
          text="Recognize"
        />
      </form>
      <div class="ma-4 w-full" v-if="resultFormula">
        <div class="text-3xl text-gray-600 m-10 text-center">
          Result:
          <span class="text-gray-900 bold bg-white p-3 rounded-lg">{{
            resultFormula.expression
          }}</span>
        </div>
        <v-row class="align-center">
          <v-img class="p-5 object-cover h-64" :src="formulaInputSrc"></v-img>
          <v-icon color="primary" size="100">mdi-arrow-right</v-icon>
          <v-img
            class="p-5 object-cover h-64"
            :src="'data:image/png;base64,' + resultFormula.image"
          ></v-img>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RecognizerApi from '@/api/RecognizerApi'
import UpperErrorSnackbar from '@/components/snackbars/upperErrorSnackbar.vue'
import APIError from '@/api/exceptions/apiExceptions'
import { Formula } from '@/domain/entities/formula'
import CanvasInput from '@/components/inputs/canvasInput.vue'

const loading = ref(false)
const snackbar = ref(false)
const errorMessage = ref('')
const formulaInput = ref<File | Blob>()
const fileInput = ref<File>()
const formulaInputSrc = ref('')
const resultFormula = ref<Formula>()
const recognizerApi = new RecognizerApi()

const showErrorMessage = (message: string) => {
  errorMessage.value = message
  snackbar.value = true
  setTimeout(() => {
    snackbar.value = false
    errorMessage.value = ''
  }, 5000)
}

const recognize = async () => {
  const canvas = document.querySelector('canvas')
  const inputUrl = canvas?.toDataURL('image/png')
  formulaInput.value = fileInput.value || (inputUrl ? dataURLtoBlob(inputUrl) : undefined)
  if (formulaInput.value) {
    loading.value = true
    setFormulaInputSrc()
    try {
      resultFormula.value = await recognizerApi.recognizeFormula({ image: formulaInput.value })
      loading.value = false
    } catch (error) {
      if (error instanceof APIError) showErrorMessage(error.message)
    }
  }
}

const dataURLtoBlob = (dataURL: string) => {
  const arr = dataURL.split(',')
  let mime = arr[0].match(/:(.*?);/)
  if (mime) {
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n)
    }
    return new Blob([u8arr], { type: mime[1] })
  }
}

const setFormulaInputSrc = () => {
  if (formulaInput.value) {
    const reader = new FileReader()
    reader.readAsDataURL(formulaInput.value)
    reader.onload = () => {
      formulaInputSrc.value = reader.result as string
    }
  }
  return null
}
</script>
