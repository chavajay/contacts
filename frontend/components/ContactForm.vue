<template>
  <form @submit.prevent="onSubmit" class="contact-form">
    <ion-list class="form-list" lines="none">

      <!-- Campo Nombre -->
      <div class="form-item">
        <ion-item class="custom-item" :class="{ 'ion-invalid': errors.name, 'ion-touched': touched.name }">
          <ion-icon :icon="personOutline" slot="start" class="input-icon"></ion-icon>
          <ion-input 
            label-placement="floating" 
            label="Nombre completo" 
            v-model="values.name" 
            required 
            @ionBlur="touched.name = true"
            :error-text="errors.name"
            class="custom-input"
          />
        </ion-item>
      </div>

      <!-- Campo Email -->
      <div class="form-item">
        <ion-item class="custom-item" :class="{ 'ion-invalid': errors.email, 'ion-touched': touched.email }">
          <ion-icon :icon="mailOutline" slot="start" class="input-icon"></ion-icon>
          <ion-input 
            label-placement="floating" 
            type="email" 
            label="Correo electrónico" 
            v-model="values.email" 
            required 
            @ionBlur="touched.email = true"
            :error-text="errors.email"
            class="custom-input"
          />
        </ion-item>
      </div>

      <!-- Campo Teléfono -->
      <div class="form-item">
        <ion-item class="custom-item" :class="{ 'ion-invalid': errors.phone, 'ion-touched': touched.phone }">
          <ion-icon :icon="callOutline" slot="start" class="input-icon"></ion-icon>
          <ion-input 
            label-placement="floating" 
            label="Teléfono" 
            v-model="values.phone" 
            required 
            @ionBlur="touched.phone = true"
            :error-text="errors.phone"
            class="custom-input"
          />
        </ion-item>
      </div>

      <!-- Campo Tags -->
      <div class="form-item">
        <ion-item class="custom-item">
          <ion-icon :icon="pricetagsOutline" slot="start" class="input-icon"></ion-icon>
          <ion-input 
            label-placement="floating" 
            label="Etiquetas (separadas por comas)" 
            v-model="tagsInput" 
            class="custom-input"
          />
        </ion-item>
        <div class="tags-hint">Ejemplo: cliente, importante, empresaX</div>
        
        <!-- Mostrar tags como chips -->
        <div v-if="values.tags.length > 0" class="tags-container">
          <ion-chip v-for="(tag, index) in values.tags" :key="index" class="tag-chip">
            <ion-label>{{ tag }}</ion-label>
            <ion-icon :icon="closeCircle" @click="removeTag(index)"></ion-icon>
          </ion-chip>
        </div>
      </div>

      <!-- Toggle Favorito -->
      <div class="form-item favorite-item">
        <ion-item lines="none" class="custom-item">
          <ion-icon :icon="starOutline" slot="start" class="input-icon"></ion-icon>
          <ion-label>Marcar como favorito</ion-label>
          <ion-toggle 
            v-model="values.favorite" 
            slot="end"
            color="primary"
          ></ion-toggle>
        </ion-item>
      </div>
    </ion-list>

    <!-- Botón de envío -->
    <ion-button 
      expand="block" 
      type="submit" 
      class="submit-button"
      :disabled="!isFormValid"
    >
      <ion-icon :icon="saveOutline" slot="start" v-if="!isSubmitting"></ion-icon>
      <ion-spinner name="crescent" slot="start" v-if="isSubmitting"></ion-spinner>
      {{ submitText }}
    </ion-button>
  </form>
</template>

<script setup lang="ts">
import { 
  IonList, 
  IonItem, 
  IonInput, 
  IonToggle, 
  IonButton, 
  IonIcon, 
  IonChip, 
  IonLabel,
  IonSpinner 
} from '@ionic/vue'
import { 
  personOutline, 
  mailOutline, 
  callOutline, 
  pricetagsOutline, 
  closeCircle, 
  starOutline, 
  saveOutline 
} from 'ionicons/icons'
import { reactive, computed, watch, ref } from 'vue'
import { z } from 'zod'

const emit = defineEmits<{ (e: 'submit', payload: any): void }>()

const props = defineProps<{
  initial?: { name?: string; email?: string; phone?: string; favorite?: boolean; tags?: string[] }
  submitText?: string
}>()

const schema = z.object({
  name: z.string().min(1, "El nombre es obligatorio").max(120, "Máximo 120 caracteres"),
  email: z.string().email("Introduce un email válido"),
  phone: z.string().regex(/^[+]?\d[\d\s-]{6,16}\d$/, "Introduce un teléfono válido"),
  favorite: z.boolean().optional().default(false),
  tags: z.array(z.string()).optional().default([])
})

const values = reactive({
  name: props.initial?.name ?? '',
  email: props.initial?.email ?? '',
  phone: props.initial?.phone ?? '',
  favorite: props.initial?.favorite ?? false,
  tags: props.initial?.tags ?? []
})

const touched = reactive({
  name: false,
  email: false,
  phone: false
})

const isSubmitting = ref(false)
const tagsInput = computed({
  get: () => values.tags?.join(', ') ?? '',
  set: (v: string) => { values.tags = v.split(',').map(t => t.trim()).filter(Boolean) }
})

// Validación en tiempo real
const errors = computed(() => {
  const result = schema.safeParse(values)
  if (!result.success) {
    const errorMap: Record<string, string> = {}
    result.error.errors.forEach(err => {
      if (err.path) {
        errorMap[err.path[0]] = err.message
      }
    })
    return errorMap
  }
  return {}
})

const isFormValid = computed(() => {
  return schema.safeParse(values).success
})

watch(() => props.initial, (nv) => {
  if (!nv) return
  values.name = nv.name ?? ''
  values.email = nv.email ?? ''
  values.phone = nv.phone ?? ''
  values.favorite = nv.favorite ?? false
  values.tags = nv.tags ?? []
})

const submitText = computed(() => props.submitText ?? 'Guardar contacto')

const removeTag = (index: number) => {
  values.tags.splice(index, 1)
}

const onSubmit = async () => {
  // Marcar todos los campos como tocados para mostrar errores
  Object.keys(touched).forEach(key => {
    touched[key as keyof typeof touched] = true
  })
  
  const parsed = schema.safeParse(values)
  if (!parsed.success) {
    return
  }
  
  isSubmitting.value = true
  try {
    await emit('submit', parsed.data)
  } finally {
    isSubmitting.value = false
  }
}

defineExpose({ submit: onSubmit })

</script>

<style scoped>
.contact-form {
  padding: 0 16px;
}

.form-list {
  background: transparent;
}

.form-item {
  margin-bottom: 16px;
}

.custom-item {
  --border-radius: 12px;
  --border-width: 1px;
  --border-color: var(--ion-color-medium-shade);
  --background: var(--ion-color-light);
  --padding-start: 12px;
  --inner-padding-end: 12px;
  margin-bottom: 8px;
}

.custom-item.ion-invalid.ion-touched {
  --border-color: var(--ion-color-danger);
}

.custom-input {
  --padding-start: 8px;
}

.input-icon {
  color: var(--ion-color-medium);
  margin-right: 8px;
}

.tags-hint {
  font-size: 0.75rem;
  color: var(--ion-color-medium);
  margin-top: -4px;
  margin-bottom: 8px;
  padding-left: 16px;
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
}

.favorite-item {
  margin-top: 24px;
}

.submit-button {
  --border-radius: 12px;
  margin: 24px 0;
  font-weight: 600;
  height: 50px;
}

.submit-button:disabled {
  --background: var(--ion-color-medium);
  --opacity: 0.8;
}
</style>