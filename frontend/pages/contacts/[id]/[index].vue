<template>
  <ion-page>
    <ion-header class="detail-header">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-button @click="goBack" class="back-button">
            <ion-icon slot="icon-only" :icon="arrowBack"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title class="header-title">{{ contact?.name || 'Detalles del Contacto' }}</ion-title>
        <ion-buttons slot="end">
          <ion-button 
            @click="toggleFav" 
            fill="clear"
            class="action-btn"
            :class="{ 'is-favorite': contact?.favorite }"
          >
            <ion-icon 
              slot="icon-only" 
              :icon="contact?.favorite ? star : starOutline"
              :color="contact?.favorite ? 'warning' : 'medium'"
            ></ion-icon>
          </ion-button>
          <NuxtLink :to="`/contacts/${id}/edit`">
            <ion-button 
              :disabled="!contact"
              fill="clear"
              class="action-btn"
            >
              <ion-icon slot="icon-only" :icon="createOutline"></ion-icon>
            </ion-button>
          </NuxtLink>
          <ion-button 
            color="danger" 
            :disabled="!contact" 
            @click="confirmDelete"
            fill="clear"
            class="action-btn"
          >
            <ion-icon slot="icon-only" :icon="trashOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    
    <ion-content class="detail-content">
      <!-- Estado de carga -->
      <div v-if="!contact" class="loading-container">
        <ion-spinner name="crescent" class="loading-spinner"></ion-spinner>
        <p>Cargando información del contacto...</p>
      </div>

      <!-- Contenido del contacto -->
      <div v-else class="contact-container">
        <!-- Tarjeta de información principal -->
        <div class="info-card">
          <div class="contact-header">
            <div class="contact-avatar">
              {{ getInitials(contact.name) }}
            </div>
            <div class="contact-title">
              <h1 class="contact-name">{{ contact.name }}</h1>
              <div class="contact-status">
                <ion-badge v-if="contact.favorite" color="warning" class="favorite-badge">
                  <ion-icon :icon="star" size="small"></ion-icon>
                  Favorito
                </ion-badge>
              </div>
            </div>
          </div>

          <div class="contact-details-grid">
            <div class="detail-item">
              <div class="detail-icon">
                <ion-icon :icon="mailOutline"></ion-icon>
              </div>
              <div class="detail-content">
                <h3>Correo Electrónico</h3>
                <p>{{ contact.email || 'No especificado' }}</p>
                <a v-if="contact.email" :href="`mailto:${contact.email}`" class="contact-link">
                  Enviar correo
                </a>
              </div>
            </div>

            <div class="detail-item">
              <div class="detail-icon">
                <ion-icon :icon="callOutline"></ion-icon>
              </div>
              <div class="detail-content">
                <h3>Teléfono</h3>
                <p>{{ contact.phone || 'No especificado' }}</p>
                <a v-if="contact.phone" :href="`tel:${contact.phone}`" class="contact-link">
                  Llamar
                </a>
              </div>
            </div>

            <div v-if="contact.tags?.length" class="detail-item">
              <div class="detail-icon">
                <ion-icon :icon="pricetagsOutline"></ion-icon>
              </div>
              <div class="detail-content">
                <h3>Etiquetas</h3>
                <div class="tags-container">
                  <ion-chip v-for="(tag, index) in contact.tags" :key="index" class="tag-chip">
                    <ion-label>{{ tag }}</ion-label>
                  </ion-chip>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Navegación por pestañas -->
        <div class="tabs-navigation">
          <ion-segment v-model="tab" class="content-tabs">
            <ion-segment-button value="notes" class="tab-button">
              <ion-icon :icon="documentTextOutline"></ion-icon>
              <ion-label>Notas</ion-label>
            </ion-segment-button>
            <ion-segment-button value="history" class="tab-button">
              <ion-icon :icon="timeOutline"></ion-icon>
              <ion-label>Historial</ion-label>
            </ion-segment-button>
          </ion-segment>
        </div>

        <!-- Contenido de las pestañas -->
        <div class="tab-content-container">
          <div v-if="tab === 'notes'" class="notes-tab">
            <NotesPanel :contact-id="contact.id" />
          </div>
          
          <div v-else class="history-tab">
            <div class="history-card">
              <h2 class="history-title">Historial de Cambios</h2>
              
              <div v-if="history.length > 0" class="history-list">
                <div v-for="h in history" :key="h.id" class="history-item">
                  <div class="history-icon" :class="getHistoryIconClass(h.field)">
                    <ion-icon :icon="getHistoryIcon(h.field)"></ion-icon>
                  </div>
                  <div class="history-details">
                    <h4 class="history-field">{{ getFieldName(h.field) }}</h4>
                    <div class="history-change">
                      <span class="change-from">{{ h.old_value || 'Vacío' }}</span>
                      <ion-icon :icon="arrowForwardOutline" class="change-arrow"></ion-icon>
                      <span class="change-to">{{ h.new_value || 'Vacío' }}</span>
                    </div>
                    <p class="history-date">{{ formatDate(h.changed_at) }}</p>
                  </div>
                </div>
              </div>
              
              <div v-else class="empty-history">
                <ion-icon :icon="timeOutline" class="empty-icon"></ion-icon>
                <h3>No hay historial de cambios</h3>
                <p>Los cambios que realices se mostrarán aquí</p>
              </div>
            </div>
          </div>
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
  IonButtons, 
  IonBackButton, 
  IonButton, 
  IonIcon, 
  IonSegment, 
  IonSegmentButton,
  IonChip,
  IonLabel,
  IonSpinner,
  IonBadge,
  alertController
} from '@ionic/vue'
import { 
  star, 
  starOutline, 
  createOutline, 
  trashOutline, 
  mailOutline, 
  callOutline, 
  pricetagsOutline,
  documentTextOutline,
  timeOutline,
  personOutline,
  keyOutline,
  arrowForwardOutline,
  arrowBack
} from 'ionicons/icons'
import { onMounted, ref } from 'vue'
import type { Contact } from '~/types'
import NotesPanel from '~/components/NotesPanel.vue'
import { useContactsStore } from '~/stores/contacts'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)
const api = useApi()
const store = useContactsStore()

const contact = ref<Contact | null>(null)
const history = ref<any[]>([])
const tab = ref<'notes'|'history'>('notes')
const loading = ref(true)

// Función para regresar a la página principal
const goBack = () => {
  router.push('/')
}


const load = async () => {
  try {
    loading.value = true
    const { data } = await api.get(`/contacts/${id}`)
    contact.value = data
    history.value = await store.getHistory(id)
  } catch (error) {
    console.error('Error loading contact:', error)
  } finally {
    loading.value = false
  }
}

const toggleFav = async () => {
  if (!contact.value) return
  try {
    const updated = await store.update(id, { favorite: !contact.value.favorite })
    contact.value = updated
  } catch (error) {
    console.error('Error updating favorite:', error)
  }
}

const confirmDelete = async () => {
  const alert = await alertController.create({
    header: 'Eliminar contacto',
    message: `¿Estás seguro de que quieres eliminar a ${contact.value?.name}? Esta acción no se puede deshacer.`,
    buttons: [
      {
        text: 'Cancelar',
        role: 'cancel',
        cssClass: 'secondary'
      },
      {
        text: 'Eliminar',
        role: 'destructive',
        handler: remove
      }
    ]
  })
  
  await alert.present()
}

const remove = async () => {
  try {
    await store.remove(id)
    // Navegar a la página principal después de eliminar
    router.push('/')
  } catch (error) {
    console.error('Error deleting contact:', error)
  }
}

const getInitials = (name: string) => {
  return name.split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const getHistoryIcon = (field: string) => {
  const icons: Record<string, string> = {
    name: personOutline,
    email: mailOutline,
    phone: callOutline,
    favorite: starOutline,
    tags: pricetagsOutline
  }
  return icons[field] || keyOutline
}

const getHistoryIconClass = (field: string) => {
  const classes: Record<string, string> = {
    name: 'icon-name',
    email: 'icon-email',
    phone: 'icon-phone',
    favorite: 'icon-favorite',
    tags: 'icon-tags'
  }
  return classes[field] || 'icon-default'
}

const getFieldName = (field: string) => {
  const names: Record<string, string> = {
    name: 'Nombre',
    email: 'Correo Electrónico',
    phone: 'Teléfono',
    favorite: 'Favorito',
    tags: 'Etiquetas'
  }
  return names[field] || field
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(load)
</script>

<style scoped>
.detail-header {
  --background: var(--ion-color-light);
  border-bottom: 1px solid var(--ion-color-light-shade);
}

.detail-header ion-toolbar {
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
  --icon-font-size: 1.4rem;
}

.action-btn {
  --padding-start: 8px;
  --padding-end: 8px;
  margin: 0 4px;
}

.action-btn ion-icon {
  font-size: 1.2rem;
}

.is-favorite {
  --color: var(--ion-color-warning);
}

.detail-content {
  --background: #f8f9fa;
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

.contact-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 16px;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--ion-color-light-shade);
}

.contact-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ion-color-light-shade);
}

.contact-avatar {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--ion-color-primary), var(--ion-color-secondary));
  color: rgb(0, 0, 0);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin-right: 16px;
  flex-shrink: 0;
}

.contact-title {
  flex: 1;
}

.contact-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--ion-color-dark);
}

.contact-status {
  display: flex;
  align-items: center;
}

.favorite-badge {
  font-weight: 500;
  padding: 6px 10px;
}

.favorite-badge ion-icon {
  margin-right: 4px;
}

.contact-details-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.detail-icon {
  width: 40px;
  height: 40px;
  background: var(--ion-color-light);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.detail-icon ion-icon {
  font-size: 1.2rem;
  color: var(--ion-color-primary);
}

.detail-content {
  flex: 1;
}

.detail-content h3 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--ion-color-medium);
  margin: 0 0 6px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-content p {
  font-size: 1rem;
  color: var(--ion-color-dark);
  margin: 0;
  font-weight: 500;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.tag-chip {
  --background: var(--ion-color-primary-tint);
  --color: var(--ion-color-primary-shade);
  font-weight: 500;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.tabs-navigation {
  margin-bottom: 24px;
}

.content-tabs {
  --background: white;
  border-radius: 12px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--ion-color-light-shade);
}

.tab-button {
  --border-radius: 8px;
  --color: var(--ion-color-medium);
  --color-checked: var(--ion-color-primary);
  --indicator-color: var(--ion-color-primary);
  min-height: 44px;
}

.tab-content-container {
  min-height: 400px;
}

.history-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--ion-color-light-shade);
}

.history-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--ion-color-dark);
  margin: 0 0 20px 0;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ion-color-light-shade);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: var(--ion-color-light);
  border-radius: 8px;
  border-left: 4px solid var(--ion-color-primary);
}

.history-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--ion-color-primary);
  color: white;
}

.history-icon.icon-name { background: var(--ion-color-primary); }
.history-icon.icon-email { background: var(--ion-color-success); }
.history-icon.icon-phone { background: var(--ion-color-warning); }
.history-icon.icon-favorite { background: var(--ion-color-tertiary); }
.history-icon.icon-tags { background: var(--ion-color-secondary); }
.history-icon.icon-default { background: var(--ion-color-medium); }

.history-details {
  flex: 1;
}

.history-field {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--ion-color-dark);
  margin: 0 0 8px 0;
}

.history-change {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.change-from {
  color: var(--ion-color-danger);
  font-weight: 500;
  background: rgba(var(--ion-color-danger-rgb), 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  text-decoration: line-through;
}

.change-arrow {
  color: var(--ion-color-medium);
  font-size: 0.9rem;
}

.change-to {
  color: var(--ion-color-success);
  font-weight: 500;
  background: rgba(var(--ion-color-success-rgb), 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

.history-date {
  font-size: 0.8rem;
  color: var(--ion-color-medium);
  margin: 0;
}

.empty-history {
  text-align: center;
  padding: 40px 20px;
  color: var(--ion-color-medium);
}

.empty-history .empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-history h3 {
  margin: 0 0 8px 0;
  color: var(--ion-color-dark);
  font-size: 1.1rem;
}

.empty-history p {
  margin: 0;
  font-size: 0.9rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .contact-container {
    padding: 12px;
  }
  
  .info-card {
    padding: 20px;
    margin-bottom: 16px;
  }
  
  .contact-header {
    flex-direction: column;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .contact-avatar {
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .contact-name {
    font-size: 1.3rem;
  }
  
  .detail-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .detail-icon {
    align-self: center;
  }
  
  .history-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .history-change {
    justify-content: center;
  }
}

@media (min-width: 992px) {
  .contact-container {
    padding: 24px;
  }
  
  .info-card {
    padding: 32px;
  }
}
</style>