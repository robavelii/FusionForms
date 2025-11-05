<template>
  <v-card>
    <v-card-title>Form Settings</v-card-title>
    <v-card-text>
      <v-text-field v-model="form.title" label="Title" />
      <v-textarea v-model="form.description" label="Description" />
      <v-text-field v-model="form.settings.submitButtonText" label="Submit Button Text" />
      <v-text-field v-model="form.settings.successMessage" label="Success Message" />
      <v-checkbox v-model="form.settings.saveProgress" label="Allow save progress" />
      <v-checkbox v-model="form.settings.multipleSubmissions" label="Allow multiple submissions" />
    </v-card-text>
  </v-card>
</template>