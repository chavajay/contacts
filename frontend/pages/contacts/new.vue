<template>
  <ion-page>
    <ion-header class="new-contact-header">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-button @click="goBack" class="back-button">
            <ion-icon slot="icon-only" :icon="arrowBack"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title class="header-title">Nuevo Contacto</ion-title>
        <ion-buttons slot="end">
          <ion-button 
            @click="handleCreate" 
            :disabled="isCreating"
            class="create-button"
          >
            <ion-spinner v-if="isCreating" name="crescent" class="create-spinner"></ion-spinner>
            <span v-else>Crear</span>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    
    <ion-content class="new-contact-content">
      <div class="content-wrapper">
        <div class="form-container">
          <div class="form-header">
            <ion-icon :icon="personAddOutline" class="form-icon"></ion-icon>
            <h2 class="form-title">Agregar Nuevo Contacto</h2>
            <p class="form-subtitle">Complete la información del contacto</p>
          </div>
          
          <ContactForm 
            @submit="create" 
            submitText="Crear contacto" 
            ref="contactForm"
            :key="formKey"
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
  IonButton, 
  IonButtons,
  IonIcon,
  IonSpinner,
  alertController
} from '@ionic/vue'
import { arrowBack, personAddOutline } from 'ionicons/icons'
import ContactForm from '~/components/ContactForm.vue'
import { useContactsStore } from '~/stores/contacts'
import { ref } from 'vue'

const store = useContactsStore()
const router = useRouter()
const contactForm = ref<InstanceType<typeof ContactForm> | null>(null)
const isCreating = ref(false)
const formKey = ref(0)

// Función para regresar
const goBack = () => {
  router.push('/')
}

const handleCreate = () => {
  if (contactForm.value) {
    // Disparar el evento submit del formulario
    const formElement = contactForm.value.$el as HTMLElement
    const submitEvent = new Event('submit', { bubbles: true, cancelable: true })
    formElement.dispatchEvent(submitEvent)
  }
}

const create = async (payload: any) => {
  isCreating.value = true
  try {
    const contact = await store.create(payload)
    await showSuccessAlert(contact.name)
    router.push(`/contacts/${contact.id}`)
  } catch (error: any) {
    console.error('Error creating contact:', error)
    showErrorAlert(error.response?.data?.detail || 'Error al crear el contacto')
    // Resetear el formulario para permitir correcciones
    formKey.value++ // Esto fuerza a recrear el formulario
  } finally {
    isCreating.value = false
  }
}

const showSuccessAlert = async (contactName: string) => {
  const alert = await alertController.create({
    header: '¡Contacto Creado!',
    message: `El contacto "${contactName}" se ha creado exitosamente.`,
    buttons: ['OK'],
    cssClass: 'success-alert'
  })
  await alert.present()
}

const showErrorAlert = async (message: string = 'Ocurrió un error inesperado') => {
  const alert = await alertController.create({
    header: 'Error al Crear',
    message: message,
    buttons: ['OK'],
    cssClass: 'error-alert'
  })
  await alert.present()
}
</script>

<style scoped>
.new-contact-header {
  --background: var(--ion-color-light);
  border-bottom: 1px solid var(--ion-color-light-shade);
}

.new-contact-header ion-toolbar {
  --background: white;
  --border-width: 0;
}

.header-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--ion-color-dark);
}

.back-button {
  --color: var(--ion-color-dark);
  --padding-start: 8px;
  --padding-end: 8px;
}

.back-button ion-icon {
  font-size: 1.4rem;
}

.create-button {
  --color: var(--ion-color-primary);
  font-weight: 600;
  margin-right: 8px;
}

.create-button:disabled {
  --color: var(--ion-color-medium);
  opacity: 0.7;
}

.create-spinner {
  width: 18px;
  height: 18px;
}

.new-contact-content {
  --background: #f8f9fa;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
}

.form-container {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--ion-color-light-shade);
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ion-color-light-shade);
}

.form-icon {
  font-size: 48px;
  color: var(--ion-color-primary);
  margin-bottom: 16px;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ion-color-dark);
  margin: 0 0 8px 0;
}

.form-subtitle {
  font-size: 1rem;
  color: var(--ion-color-medium);
  margin: 0;
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
  .content-wrapper {
    padding: 12px;
  }
  
  .form-container {
    padding: 24px;
    border-radius: 12px;
  }
  
  .form-header {
    margin-bottom: 24px;
    padding-bottom: 20px;
  }
  
  .form-icon {
    font-size: 40px;
  }
  
  .form-title {
    font-size: 1.3rem;
  }
  
  .header-title {
    font-size: 1.1rem;
  }
  
  .create-button {
    font-size: 0.9rem;
  }
}

@media (min-width: 992px) {
  .content-wrapper {
    padding: 24px;
  }
  
  .form-container {
    padding: 40px;
  }
  
  .form-title {
    font-size: 1.8rem;
  }
}

/* Animaciones suaves */
.form-container {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>