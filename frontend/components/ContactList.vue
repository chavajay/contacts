<template>
  <ion-content class="contacts-content" :fullscreen="true">
    <div class="contacts-container">
      <!-- Header con búsqueda y acciones -->
      <div class="search-header">
        <ion-searchbar 
          v-model="store.q" 
          placeholder="Buscar contactos..." 
          class="custom-searchbar"
        />
        
        <div class="header-actions">
          <ion-button @click="$router.push('/contacts/new')" class="new-contact-btn">
            <ion-icon slot="icon-only" :icon="addOutline"></ion-icon>
          </ion-button>
          
          <ion-button fill="clear" @click="showFilters = !showFilters" class="filter-btn">
            <ion-icon slot="icon-only" :icon="filterOutline"></ion-icon>
          </ion-button>
        </div>
      </div>

      <!-- Filtros expandibles -->
      <div v-if="showFilters" class="filters-panel">
        <ion-list lines="none" class="filters-list">
          <ion-item>
            <ion-select 
              interface="popover" 
              placeholder="Filtrar por tag" 
              v-model="store.tag"
              class="tag-filter"
            >
              <ion-select-option value="">Todos los tags</ion-select-option>
              <ion-select-option v-for="t in tags" :key="t" :value="t">
                {{ t }}
              </ion-select-option>
            </ion-select>
          </ion-item>
          
          <ion-item>
            <ion-segment v-model="favFilter" class="favorite-segment">
              <ion-segment-button value="all">
                <ion-label>Todos</ion-label>
              </ion-segment-button>
              <ion-segment-button value="fav">
                <ion-icon :icon="starOutline" slot="start"></ion-icon>
                <ion-label>Favoritos</ion-label>
              </ion-segment-button>
            </ion-segment>
          </ion-item>
        </ion-list>
      </div>

      <!-- Estado de carga -->
      <div v-if="store.loading" class="loading-state">
        <ion-spinner name="crescent"></ion-spinner>
        <p>Cargando contactos...</p>
      </div>

      <!-- Lista de contactos -->
      <ion-list v-else class="contacts-list" lines="none">
        <div v-if="store.items.length">
          <ion-item 
            v-for="c in store.items" 
            :key="c.id" 
            button 
            @click="$router.push(`/contacts/${c.id}`)"
            class="contact-item"
          >
            <ion-avatar slot="start" class="contact-avatar">
              {{ getInitials(c.name) }}
            </ion-avatar>
            
            <ion-label class="contact-info">
              <h2 class="contact-name">
                {{ c.name }}
                <ion-icon v-if="c.favorite" :icon="star" color="warning"></ion-icon>
              </h2>
              <p class="contact-details">
                <span v-if="c.email" class="contact-email">
                  <ion-icon :icon="mailOutline"></ion-icon>
                  {{ c.email }}
                </span>
                <span v-if="c.phone" class="contact-phone">
                  <ion-icon :icon="callOutline"></ion-icon>
                  {{ c.phone }}
                </span>
              </p>
              
              <div v-if="c.tags?.length" class="contact-tags">
                <ion-chip v-for="(tag, index) in c.tags" :key="index" class="tag-chip">
                  <ion-label>{{ tag }}</ion-label>
                </ion-chip>
              </div>
            </ion-label>
          </ion-item>
        </div>
        
        <!-- Estado vacío -->
        <div v-else class="empty-state">
          <ion-icon :icon="peopleOutline" class="empty-icon"></ion-icon>
          <h3>No hay contactos</h3>
          <p v-if="store.q || store.tag || store.favorite">
            Intenta ajustar los filtros de búsqueda.
          </p>
          <p v-else>
            Comienza agregando tu primer contacto
          </p>
          <ion-button @click="$router.push('/contacts/new')" fill="outline">
            Crear contacto
          </ion-button>
        </div>
      </ion-list>
    </div>
  </ion-content>
</template>

<script setup lang="ts">
import { 
  IonContent, 
  IonSearchbar, 
  IonList, 
  IonItem, 
  IonLabel, 
  IonButton, 
  IonIcon, 
  IonSegment, 
  IonSegmentButton, 
  IonSelect, 
  IonSelectOption,
  IonAvatar,
  IonChip,
  IonSpinner
} from '@ionic/vue'
import { 
  addOutline, 
  filterOutline, 
  starOutline, 
  star, 
  mailOutline, 
  callOutline, 
  peopleOutline 
} from 'ionicons/icons'

import { onMounted, ref, watch } from 'vue'
import { useContactsStore } from '~/stores/contacts'

const store = useContactsStore()
const tags = ref<string[]>([])
const favFilter = ref<'all'|'fav'>('all')
const showFilters = ref(false)
const api = useApi()

onMounted(async () => {
  await store.fetchContacts()
  const { data } = await api.get('/tags')
  tags.value = data.map((t: any) => t.name)
})

watch(favFilter, (v) => {
  store.favorite = v === 'fav' ? true : null
})

// Obtener iniciales para el avatar
const getInitials = (name: string) => {
  return name.split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}
</script>

<style scoped>
.contacts-content {
  --background: var(--ion-color-light);
}

.contacts-container {
  max-width: 800px;
  margin: 0 auto;
}

.search-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 16px 8px;
  background: var(--ion-color-light);
  position: sticky;
  top: 0;
  z-index: 10;
}

.custom-searchbar {
  flex: 1;
  padding: 0;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.new-contact-btn {
  --border-radius: 12px;
  --padding-start: 12px;
  --padding-end: 12px;
}

.filter-btn {
  --border-radius: 12px;
  color: var(--ion-color-medium);
}

.filters-panel {
  background: rgb(255, 255, 255);
  border-radius: 0 0 16px 16px;
  margin: 0 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.filters-list {
  padding: 0;
}

.tag-filter {
  width: 100%;
}

.favorite-segment {
  width: 100%;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: var(--ion-color-medium);
}

.contacts-list {
  padding: 8px 16px;
  background: transparent;
}

.contact-item {
  --border-radius: 12px;
  --padding-start: 12px;
  --padding-end: 12px;
  margin-bottom: 12px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.contact-item:active {
  transform: scale(0.98);
}

.contact-avatar {
  width: 48px;
  height: 48px;
  background: var(--ion-color-primary);
  color: rgb(7, 7, 7);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
}

.contact-info {
  margin: 12px 0;
}

.contact-name {
  font-weight: 600;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 8px;
  color: var(--ion-color-medium);
}

.contact-email, .contact-phone {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
}

.contact-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
  
}

.tag-chip {
  --background: var(--ion-color-primary-tint);
  --color: var(--ion-color-primary-shade);
  font-size: 0.75rem;
  height: 24px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--ion-color-medium);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  margin-bottom: 8px;
  color: var(--ion-color-dark);
}

.empty-state p {
  margin-bottom: 20px;
}

@media (min-width: 768px) {
  .contacts-container {
    padding: 0 24px;
  }
  
  .contact-details {
    flex-direction: row;
    gap: 16px;
  }
}
</style>