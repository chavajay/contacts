import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { Contact, Note } from '~/types'

export const useContactsStore = defineStore('contacts', () => {
  const api = useApi()
  const items = ref<Contact[]>([])
  const q = ref('')
  const favorite = ref<boolean | null>(null)
  const tag = ref<string>('')
  const loading = ref(false)

  const fetchContacts = async () => {
    loading.value = true
    const params: Record<string, any> = {}
    if (q.value) params.q = q.value
    if (favorite.value !== null) params.favorite = favorite.value
    if (tag.value) params.tag = tag.value
    const { data } = await api.get('/contacts', { params })
    items.value = data
    loading.value = false
  }

  // buscador tiempo real
  let timer: any
  watch([q, favorite, tag], () => {
    clearTimeout(timer)
    timer = setTimeout(fetchContacts, 250)
  })

  const addNote = async (contactId: number, content: string) => {
    const { data } = await api.post(`/contacts/${contactId}/notes`, { content })
    return data as Note
  }
  
  const deleteNote = async (contactId: number, noteId: number) => {
    await api.delete(`/contacts/${contactId}/notes/${noteId}`)
    return await getNotes(contactId)
  }

  const getNotes = async (contactId: number) => {
    const { data } = await api.get(`/contacts/${contactId}/notes`)
    return data as Note[]
  }

  const getHistory = async (contactId: number) => {
    const { data } = await api.get(`/contacts/${contactId}/history`)
    return data
  }

  const create = async (payload: any) => {
    const { data } = await api.post('/contacts', payload)
    await fetchContacts()
    return data as Contact
  }

  const update = async (id: number, payload: any) => {
    const { data } = await api.patch(`/contacts/${id}`, payload)
    await fetchContacts()
    return data as Contact
  }

  const remove = async (id: number) => {
    await api.delete(`/contacts/${id}`)
    await fetchContacts()
  }

  return { items, q, favorite, tag, loading, fetchContacts, addNote, getNotes, getHistory, create, update, remove, deleteNote }
})
