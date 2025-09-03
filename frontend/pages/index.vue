<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Directorio de Contactos</ion-title>
      </ion-toolbar>
    </ion-header>
    <ContactList />
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle } from '@ionic/vue'
import ContactList from '~/components/ContactList.vue'
</script>
