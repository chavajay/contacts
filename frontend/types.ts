export interface Contact {
  id: number
  name: string
  email: string
  phone: string
  favorite: boolean
  tags: string[]
  created_at: string
  updated_at: string
}

export interface Note {
  id: number
  content: string
  created_at: string
}
