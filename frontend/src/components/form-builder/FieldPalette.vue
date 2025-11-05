<template>
  <div class="field-palette">
    <v-card>
      <v-card-title class="text-h6">
        Field Palette
      </v-card-title>
      <v-card-text>
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title>
              Basic Fields
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="field-list">
                <div
                  v-for="field in basicFields"
                  :key="field.type"
                  class="field-item"
                  draggable="true"
                  @dragstart="onDragStart($event, field)"
                >
                  <v-icon>{{ field.icon }}</v-icon>
                  <span>{{ field.label }}</span>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-title>
              Advanced Fields
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="field-list">
                <div
                  v-for="field in advancedFields"
                  :key="field.type"
                  class="field-item"
                  draggable="true"
                  @dragstart="onDragStart($event, field)"
                >
                  <v-icon>{{ field.icon }}</v-icon>
                  <span>{{ field.label }}</span>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-title>
              Layout
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="field-list">
                <div
                  v-for="field in layoutFields"
                  :key="field.type"
                  class="field-item"
                  draggable="true"
                  @dragstart="onDragStart($event, field)"
                >
                  <v-icon>{{ field.icon }}</v-icon>
                  <span>{{ field.label }}</span>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

interface Field {
  type: string
  label: string
  icon: string
}

// Reactive state
const basicFields: Field[] = reactive([
  { type: 'text', label: 'Text Input', icon: 'mdi-textbox' },
  { type: 'textarea', label: 'Text Area', icon: 'mdi-textarea' },
  { type: 'number', label: 'Number', icon: 'mdi-numeric' },
  { type: 'email', label: 'Email', icon: 'mdi-email' },
  { type: 'url', label: 'URL', icon: 'mdi-link' },
  { type: 'date', label: 'Date', icon: 'mdi-calendar' },
  { type: 'time', label: 'Time', icon: 'mdi-clock' },
  { type: 'checkbox', label: 'Checkbox', icon: 'mdi-checkbox-marked' },
  { type: 'radio', label: 'Radio Buttons', icon: 'mdi-radiobox-marked' },
  { type: 'select', label: 'Dropdown', icon: 'mdi-menu-down' }
])

const advancedFields: Field[] = reactive([
  { type: 'file', label: 'File Upload', icon: 'mdi-file-upload' },
  { type: 'rating', label: 'Rating Scale', icon: 'mdi-star' },
  { type: 'signature', label: 'Signature', icon: 'mdi-draw' },
  { type: 'hidden', label: 'Hidden Field', icon: 'mdi-eye-off' },
  { type: 'richtext', label: 'Rich Text', icon: 'mdi-format-text' }
])

const layoutFields: Field[] = reactive([
  { type: 'heading', label: 'Heading', icon: 'mdi-format-title' },
  { type: 'paragraph', label: 'Paragraph', icon: 'mdi-text' },
  { type: 'divider', label: 'Divider', icon: 'mdi-minus' },
  { type: 'image', label: 'Image', icon: 'mdi-image' }
])

// Drag event handler
function onDragStart(event: DragEvent, field: Field) {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/json', JSON.stringify(field))
  }
}
</script>

<style scoped>
.field-palette {
  height: 100%;
  overflow-y: auto;
}

.field-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: grab;
  transition: background-color 0.2s;
}

.field-item:hover {
  background-color: #f5f5f5;
}

.field-item:active {
  cursor: grabbing;
}
</style>
