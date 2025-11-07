<template>
  <v-container fluid class="form-settings">
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>General Settings</v-card-title>
          <v-card-text>
            <v-form ref="settingsForm">
              <v-text-field
                v-model="formData.name"
                label="Form Name"
                :rules="[rules.required]"
                variant="outlined"
                class="mb-4"
              />

              <v-textarea
                v-model="formData.description"
                label="Form Description"
                variant="outlined"
                rows="3"
                class="mb-4"
              />

              <v-select
                v-model="formData.status"
                :items="statusOptions"
                label="Status"
                variant="outlined"
                class="mb-4"
              />

              <v-divider class="my-6" />

              <h3 class="text-h6 mb-4">Form Behavior</h3>

              <v-text-field
                v-model="formData.schema.settings.submitButtonText"
                label="Submit Button Text"
                variant="outlined"
                class="mb-4"
              />

              <v-textarea
                v-model="formData.schema.settings.successMessage"
                label="Success Message"
                variant="outlined"
                rows="2"
                class="mb-4"
              />

              <v-text-field
                v-model="formData.schema.settings.redirectUrl"
                label="Redirect URL (after submission)"
                variant="outlined"
                hint="Optional: Redirect users after form submission"
                persistent-hint
                class="mb-4"
              />

              <v-checkbox
                v-model="formData.schema.settings.allowMultipleSubmissions"
                label="Allow multiple submissions from same user"
                class="mb-2"
              />

              <v-checkbox
                v-model="formData.schema.settings.saveProgress"
                label="Allow users to save progress and continue later"
                class="mb-2"
              />

              <v-checkbox
                v-model="formData.schema.settings.showProgressBar"
                label="Show progress bar (for multi-page forms)"
                class="mb-2"
              />

              <v-checkbox
                v-model="formData.schema.settings.requireLogin"
                label="Require login to submit"
                class="mb-2"
              />

              <v-divider class="my-6" />

              <h3 class="text-h6 mb-4">Notifications</h3>

              <v-checkbox
                v-model="formData.schema.settings.sendConfirmationEmail"
                label="Send confirmation email to submitter"
                class="mb-2"
              />

              <v-text-field
                v-if="formData.schema.settings.sendConfirmationEmail"
                v-model="formData.schema.settings.confirmationEmailSubject"
                label="Confirmation Email Subject"
                variant="outlined"
                class="mb-4"
              />

              <v-checkbox
                v-model="formData.schema.settings.notifyAdmin"
                label="Notify admin on new submission"
                class="mb-2"
              />

              <v-text-field
                v-if="formData.schema.settings.notifyAdmin"
                v-model="formData.schema.settings.adminEmail"
                label="Admin Email"
                type="email"
                variant="outlined"
                class="mb-4"
              />

              <v-divider class="my-6" />

              <h3 class="text-h6 mb-4">Security</h3>

              <v-checkbox
                v-model="formData.schema.settings.enableCaptcha"
                label="Enable CAPTCHA"
                hint="Protect against spam and bots"
                persistent-hint
                class="mb-2"
              />

              <v-checkbox
                v-model="formData.schema.settings.enableHoneypot"
                label="Enable Honeypot field"
                hint="Hidden anti-spam protection"
                persistent-hint
                class="mb-2"
              />

              <v-text-field
                v-model.number="formData.schema.settings.rateLimit"
                label="Rate Limit (submissions per hour)"
                type="number"
                variant="outlined"
                hint="0 = unlimited"
                persistent-hint
                class="mb-4"
              />

              <v-divider class="my-6" />

              <div class="d-flex gap-2">
                <v-btn
                  color="primary"
                  :loading="saving"
                  @click="saveSettings"
                >
                  Save Changes
                </v-btn>
                <v-btn
                  variant="outlined"
                  @click="resetSettings"
                >
                  Reset
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <!-- Webhooks -->
        <v-card class="mb-4">
          <v-card-title>Webhooks</v-card-title>
          <v-card-text>
            <p class="text-body-2 text-medium-emphasis mb-4">
              Configure webhooks to send form submissions to external services
            </p>
            
            <v-list v-if="webhooks.length > 0">
              <v-list-item
                v-for="webhook in webhooks"
                :key="webhook.id"
              >
                <v-list-item-title>{{ webhook.url }}</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip size="x-small" :color="webhook.is_active ? 'success' : 'grey'">
                    {{ webhook.is_active ? 'Active' : 'Inactive' }}
                  </v-chip>
                </v-list-item-subtitle>
                <template #append>
                  <v-btn
                    icon="mdi-delete"
                    size="small"
                    variant="text"
                    @click="deleteWebhook(webhook.id)"
                  />
                </template>
              </v-list-item>
            </v-list>

            <v-btn
              block
              color="primary"
              variant="outlined"
              prepend-icon="mdi-plus"
              @click="showWebhookDialog = true"
            >
              Add Webhook
            </v-btn>
          </v-card-text>
        </v-card>

        <!-- Integrations -->
        <v-card>
          <v-card-title>Integrations</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-google</v-icon>
                </template>
                <v-list-item-title>Google Sheets</v-list-item-title>
                <template #append>
                  <v-switch
                    color="primary"
                    hide-details
                    disabled
                  />
                </template>
              </v-list-item>
              
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-email</v-icon>
                </template>
                <v-list-item-title>Mailchimp</v-list-item-title>
                <template #append>
                  <v-switch
                    color="primary"
                    hide-details
                    disabled
                  />
                </template>
              </v-list-item>
              
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-slack</v-icon>
                </template>
                <v-list-item-title>Slack</v-list-item-title>
                <template #append>
                  <v-switch
                    color="primary"
                    hide-details
                    disabled
                  />
                </template>
              </v-list-item>
            </v-list>

            <p class="text-caption text-medium-emphasis mt-4">
              More integrations coming soon
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Webhook Dialog -->
    <v-dialog v-model="showWebhookDialog" max-width="500">
      <v-card>
        <v-card-title>Add Webhook</v-card-title>
        <v-card-text>
          <v-form ref="webhookForm">
            <v-text-field
              v-model="newWebhook.url"
              label="Webhook URL"
              :rules="[rules.required, rules.url]"
              variant="outlined"
              class="mb-4"
            />

            <v-select
              v-model="newWebhook.event"
              :items="webhookEvents"
              label="Trigger Event"
              variant="outlined"
              class="mb-4"
            />

            <v-checkbox
              v-model="newWebhook.is_active"
              label="Active"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showWebhookDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addWebhook">Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { useSnackbarStore } from '@/stores/snackbar'
import { useFormsStore } from '@/stores/forms'
import apiClient from '@/services/api'

const props = defineProps<{
  form: any
}>()

const emit = defineEmits<{
  (e: 'update', form: any): void
}>()

const snackbarStore = useSnackbarStore()
const formsStore = useFormsStore()

const settingsForm = ref()
const webhookForm = ref()
const saving = ref(false)
const showWebhookDialog = ref(false)
const webhooks = ref<any[]>([])

const statusOptions = ['draft', 'published', 'archived']
const webhookEvents = ['form.submitted', 'form.updated', 'form.published']

const formData = reactive({
  name: '',
  description: '',
  status: 'draft',
  schema: {
    settings: {
      submitButtonText: 'Submit',
      successMessage: 'Thank you for your submission!',
      redirectUrl: '',
      allowMultipleSubmissions: false,
      saveProgress: false,
      showProgressBar: true,
      requireLogin: false,
      sendConfirmationEmail: false,
      confirmationEmailSubject: 'Form Submission Confirmation',
      notifyAdmin: false,
      adminEmail: '',
      enableCaptcha: false,
      enableHoneypot: true,
      rateLimit: 0
    }
  }
})

const newWebhook = reactive({
  url: '',
  event: 'form.submitted',
  is_active: true
})

const rules = {
  required: (v: string) => !!v || 'This field is required',
  url: (v: string) => {
    try {
      new URL(v)
      return true
    } catch {
      return 'Please enter a valid URL'
    }
  }
}

watch(() => props.form, (newForm) => {
  if (newForm) {
    Object.assign(formData, {
      name: newForm.name,
      description: newForm.description,
      status: newForm.status,
      schema: {
        ...newForm.schema,
        settings: {
          ...formData.schema.settings,
          ...newForm.schema?.settings
        }
      }
    })
  }
}, { immediate: true })

onMounted(() => {
  fetchWebhooks()
})

async function fetchWebhooks() {
  try {
    const response = await apiClient.get(`/webhooks/?form=${props.form.id}`)
    webhooks.value = response.data.results || []
  } catch (error) {
    console.error('Error fetching webhooks:', error)
  }
}

async function saveSettings() {
  const { valid } = await settingsForm.value.validate()
  if (!valid) return

  saving.value = true
  try {
    await formsStore.updateForm(props.form.id, formData)
    snackbarStore.success('Settings saved successfully')
    emit('update', formData)
  } catch (error) {
    snackbarStore.error('Failed to save settings')
  } finally {
    saving.value = false
  }
}

function resetSettings() {
  Object.assign(formData, props.form)
}

async function addWebhook() {
  const { valid } = await webhookForm.value.validate()
  if (!valid) return

  try {
    await apiClient.post('/webhooks/', {
      ...newWebhook,
      form: props.form.id
    })
    snackbarStore.success('Webhook added successfully')
    showWebhookDialog.value = false
    fetchWebhooks()
    
    // Reset form
    newWebhook.url = ''
    newWebhook.event = 'form.submitted'
    newWebhook.is_active = true
  } catch (error) {
    snackbarStore.error('Failed to add webhook')
  }
}

async function deleteWebhook(id: number) {
  try {
    await apiClient.delete(`/webhooks/${id}/`)
    snackbarStore.success('Webhook deleted successfully')
    fetchWebhooks()
  } catch (error) {
    snackbarStore.error('Failed to delete webhook')
  }
}
</script>

<style scoped>
.form-settings {
  padding: 0;
}
</style>
