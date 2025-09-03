<template>
  <div class="notes-container">
    <div class="notes-header">
      <h2 class="notes-title">Notas</h2>
      <ion-badge color="primary" class="notes-count">{{ notes.length }}</ion-badge>
    </div>

    <!-- Formulario para añadir notas -->
    <form @submit.prevent="submit" class="note-form">
      <ion-item class="note-input-item" lines="none">
        <ion-textarea 
          v-model="note" 
          placeholder="Escribe una nueva nota..." 
          auto-grow 
          rows="3"
          maxlength="500"
          counter
          class="note-textarea"
          :class="{ 'has-content': note.trim().length > 0 }"
        />
      </ion-item>
      
      <div class="note-actions">
        <div class="char-counter" v-if="note.length > 0">
          {{ note.length }}/500
        </div>
        <ion-button 
          type="submit" 
          :disabled="!note.trim()" 
          class="add-note-btn"
          expand="block"
        >
          <ion-icon slot="start" :icon="addCircleOutline"></ion-icon>
          Añadir nota
        </ion-button>
      </div>
    </form>

    <!-- Lista de notas -->
    <div class="notes-list" v-if="notes.length > 0">
      <div v-for="n in notes" :key="n.id" class="note-card">
        <div class="note-content">
          <p class="note-text">{{ n.content }}</p>
          <div class="note-meta">
            <ion-icon :icon="timeOutline" class="note-time-icon"></ion-icon>
            <span class="note-date">{{ formatDate(n.created_at) }}</span>
          </div>
        </div>
        <ion-button 
          fill="clear" 
          size="small" 
          @click="confirmDelete(n.id)"
          class="note-delete-btn"
        >
          <ion-icon slot="icon-only" :icon="trashOutline" color="medium"></ion-icon>
        </ion-button>
      </div>
    </div>

    <!-- Estado vacío -->
    <div v-else class="empty-notes">
      <ion-icon :icon="documentTextOutline" class="empty-icon"></ion-icon>
      <h3>No hay notas aún</h3>
      <p>Agrega la primera nota para este contacto</p>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="notes-loading">
      <ion-spinner name="crescent"></ion-spinner>
      <p>Cargando notas...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  IonItem, 
  IonTextarea, 
  IonButton, 
  IonIcon, 
  IonBadge,
  IonSpinner,
  alertController
} from '@ionic/vue'
import { 
  addCircleOutline, 
  trashOutline, 
  timeOutline, 
  documentTextOutline 
} from 'ionicons/icons'
import { ref, onMounted } from 'vue'
import type { Note } from '~/types'
import { useContactsStore } from '~/stores/contacts'

const props = defineProps<{ contactId: number }>()
const store = useContactsStore()

const note = ref('')
const notes = ref<Note[]>([])
const loading = ref(false)

const load = async () => {
  loading.value = true
  try {
    notes.value = await store.getNotes(props.contactId)
  } catch (error) {
    console.error('Error loading notes:', error)
  } finally {
    loading.value = false
  }
}

const submit = async () => {
  if (!note.value.trim()) return
  
  try {
    await store.addNote(props.contactId, note.value.trim())
    note.value = ''
    await load()
  } catch (error) {
    console.error('Error adding note:', error)
  }
}

const confirmDelete = async (noteId: number) => {
  const alert = await alertController.create({
    header: 'Eliminar nota',
    message: '¿Estás seguro de que quieres eliminar esta nota?',
    buttons: [
      {
        text: 'Cancelar',
        role: 'cancel'
      },
      {
        text: 'Eliminar',
        role: 'destructive',
        handler: async () => {
          try {
            await store.deleteNote(props.contactId, noteId)
            // Recargamos las notas después de eliminar
            await load()
          } catch (error) {
            console.error('Error deleting note:', error)
          }
        }
      }
    ]
  })

  await alert.present()
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) {
    return 'Hoy a las ' + date.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  } else if (diffDays === 2) {
    return 'Ayer a las ' + date.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  } else {
    return date.toLocaleDateString('es-ES', { 
      year: 'numeric',
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
}

onMounted(load)
</script>

<style scoped>
.notes-container {
  padding: 16px;
}

.notes-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.notes-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ion-color-dark);
}

.notes-count {
  font-size: 0.9rem;
}

.note-form {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.note-input-item {
  --background: transparent;
  --padding-start: 0;
  --inner-padding-end: 0;
}

.note-textarea {
  --padding-start: 0;
  --padding-end: 0;
  font-size: 1rem;
  line-height: 1.5;
}

.note-textarea.has-content {
  min-height: 80px;
}

.note-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.char-counter {
  font-size: 0.8rem;
  color: var(--ion-color-medium);
}

.add-note-btn {
  --border-radius: 8px;
  margin: 0;
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.note-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.note-content {
  flex: 1;
}

.note-text {
  margin: 0 0 8px 0;
  line-height: 1.5;
  color: var(--ion-color-dark);
  white-space: pre-wrap;
}

.note-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--ion-color-medium);
}

.note-time-icon {
  font-size: 0.9rem;
}

.note-delete-btn {
  --padding-start: 8px;
  --padding-end: 8px;
  margin: -8px;
}

.empty-notes {
  text-align: center;
  padding: 40px 20px;
  color: var(--ion-color-medium);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-notes h3 {
  margin: 0 0 8px 0;
  color: var(--ion-color-dark);
  font-size: 1.1rem;
}

.empty-notes p {
  margin: 0;
  font-size: 0.9rem;
}

.notes-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: var(--ion-color-medium);
}

/* Responsive design */
@media (max-width: 768px) {
  .notes-container {
    padding: 12px;
  }
  
  .note-form {
    padding: 12px;
  }
  
  .note-actions {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }
  
  .char-counter {
    order: 2;
    text-align: center;
  }
}
</style>