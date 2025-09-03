<template>
  <ion-page>
    <ion-header class="edit-header">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button 
            :default-href="`/contacts/${id}`" 
            text="Cancelar"
            class="back-button"
          />
        </ion-buttons>
        <ion-title class="header-title">Editar contacto</ion-title>
        <ion-buttons slot="end">
          <ion-button 
            @click="handleSave" 
            :disabled="isSaving"
            class="save-button"
          >
            <ion-spinner v-if="isSaving" name="crescent" class="save-spinner"></ion-spinner>
            <span v-else>Guardar</span>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    
    <ion-content class="edit-content">
      <div class="content-wrapper">
        <!-- Estado de carga -->
        <div v-if="!loaded" class="loading-container">
          <ion-spinner name="crescent" class="loading-spinner"></ion-spinner>
          <p>Cargando información del contacto...</p>
        </div>
        
        <!-- Formulario -->
        <div v-else class="form-container">
          <ContactForm 
            :initial="initial" 
            @submit="save" 
            submitText="Guardar cambios"
            ref="contactForm"
          />
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { 
  IonPage, 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent, 
  IonBackButton, 
  IonButtons,
  IonButton,
  IonSpinner,
  alertController
} from '@ionic/vue'
import ContactForm from '~/components/ContactForm.vue'
import { ref, onMounted } from 'vue'
import { useContactsStore } from '~/stores/contacts'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)
const api = useApi()
const store = useContactsStore()

const initial = ref<any>({})
const loaded = ref(false)
const isSaving = ref(false)
const contactForm = ref<InstanceType<typeof ContactForm> | null>(null)

const handleSave = () => {
  contactForm.value?.submit()
}

const load = async () => {
  try {
    const { data } = await api.get(`/contacts/${id}`)
    initial.value = data
  } catch (error) {
    console.error('Error loading contact:', error)
    showErrorAlert('No se pudo cargar la información del contacto')
    initial.value = {}
  } finally {
    loaded.value = true
  }
}

const save = async (payload: any) => {
  isSaving.value = true
  try {
    await store.update(id, payload)
    await showSuccessAlert()
    router.push(`/contacts/${id}`)
  } catch (error: any) {
    console.error('Error updating contact:', error)
    showErrorAlert(error.response?.data?.detail || 'Error al guardar los cambios')
  } finally {
    isSaving.value = false
  }
}

const showSuccessAlert = async () => {
  const alert = await alertController.create({
    header: '¡Éxito!',
    message: 'Los cambios se guardaron correctamente',
    buttons: ['OK'],
    cssClass: 'success-alert'
  })
  await alert.present()
}

const showErrorAlert = async (message: string = 'Ocurrió un error inesperado') => {
  const alert = await alertController.create({
    header: 'Error',
    message: message,
    buttons: ['OK'],
    cssClass: 'error-alert'
  })
  await alert.present()
}

onMounted(load)
</script>

<style scoped>
.edit-header {
  --background: var(--ion-color-light);
}

.edit-header ion-toolbar {
  --background: transparent;
  --border-width: 0;
}

.header-title {
  font-weight: 600;
  font-size: 1.2rem;
}

.back-button {
  --color: var(--ion-color-medium);
  --icon-margin-end: 4px;
}

.save-button {
  --color: var(--ion-color-primary);
  font-weight: 600;
  margin-right: 8px;
}

.save-button:disabled {
  --color: var(--ion-color-medium);
  opacity: 0.7;
}

.save-spinner {
  width: 18px;
  height: 18px;
}

.edit-content {
  --background: var(--ion-color-light);
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: var(--ion-color-medium);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin-bottom: 16px;
  color: var(--ion-color-primary);
}

.loading-container p {
  margin: 0;
  font-size: 0.9rem;
}

.form-container {
  padding: 16px;
  background: white;
  border-radius: 16px;
  margin: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* Estilos para las alertas */
:deep(.success-alert) {
  --background: var(--ion-color-light);
}

:deep(.success-alert .alert-head) {
  color: var(--ion-color-success);
}

:deep(.error-alert) {
  --background: var(--ion-color-light);
}

:deep(.error-alert .alert-head) {
  color: var(--ion-color-danger);
}

/* Responsive design */
@media (max-width: 768px) {
  .form-container {
    margin: 8px;
    padding: 12px;
    border-radius: 12px;
  }
  
  .header-title {
    font-size: 1.1rem;
  }
  
  .save-button {
    font-size: 0.9rem;
  }
}

@media (min-width: 992px) {
  .content-wrapper {
    padding: 0 24px;
  }
  
  .form-container {
    margin: 24px auto;
    padding: 24px;
  }
}
</style>