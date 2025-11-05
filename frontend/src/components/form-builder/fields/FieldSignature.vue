<template>
  <div class="field-signature">
    <p>{{ field.label }}</p>

    <v-card
      class="signature-pad"
      :style="{ width: field.options.width + 'px', height: field.options.height + 'px' }"
    >
      <canvas v-if="isPreview" ref="signatureCanvas" />
      <div v-else class="signature-placeholder">
        <v-icon size="48">mdi-draw</v-icon>
        <p>Signature Field</p>
      </div>
    </v-card>

    <div v-if="isPreview" class="signature-actions">
      <v-btn size="small" @click="clearSignature">Clear</v-btn>
    </div>

    <v-textarea
      v-if="field.options.helpText"
      :model-value="field.options.helpText"
      label="Help Text"
      readonly
      class="mt-2"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

interface FieldSignatureOption {
  width?: number
  height?: number
  helpText?: string
}

interface FieldSignature {
  label: string
  value?: string
  required?: boolean
  options: FieldSignatureOption
}

// Props
const props = defineProps<{
  field: FieldSignature
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldSignature): void
}>()

// Canvas reference
const signatureCanvas = ref<HTMLCanvasElement | null>(null)
let ctx: CanvasRenderingContext2D | null = null
let drawing = false

// Initialize signature pad
const initSignaturePad = () => {
  if (!signatureCanvas.value) return
  const canvas = signatureCanvas.value
  ctx = canvas.getContext('2d')
  if (!ctx) return

  canvas.width = props.field.options.width || 300
  canvas.height = props.field.options.height || 150

  ctx.strokeStyle = '#000'
  ctx.lineWidth = 2
  ctx.lineCap = 'round'

  const startDrawing = (e: MouseEvent) => {
    drawing = true
    ctx?.beginPath()
    ctx?.moveTo(e.offsetX, e.offsetY)
  }

  const draw = (e: MouseEvent) => {
    if (!drawing) return
    ctx?.lineTo(e.offsetX, e.offsetY)
    ctx?.stroke()
  }

  const stopDrawing = () => {
    drawing = false
  }

  canvas.addEventListener('mousedown', startDrawing)
  canvas.addEventListener('mousemove', draw)
  canvas.addEventListener('mouseup', stopDrawing)
  canvas.addEventListener('mouseleave', stopDrawing)

  onBeforeUnmount(() => {
    canvas.removeEventListener('mousedown', startDrawing)
    canvas.removeEventListener('mousemove', draw)
    canvas.removeEventListener('mouseup', stopDrawing)
    canvas.removeEventListener('mouseleave', stopDrawing)
  })
}

// Clear signature
const clearSignature = () => {
  if (!signatureCanvas.value || !ctx) return
  ctx.clearRect(0, 0, signatureCanvas.value.width, signatureCanvas.value.height)
  emit('update', { ...props.field, value: '' })
}

// Watch for preview mode to initialize
onMounted(() => {
  if (props.isPreview) {
    initSignaturePad()
  }
})
</script>

<style scoped>
.signature-pad {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.signature-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #9e9e9e;
}

.signature-actions {
  margin-top: 8px;
}
</style>
