import { useState } from 'react'
import './SearchBar.css'

export function SearchBar({ onSearch }) {
  const [make, setMake] = useState('')
  const [model, setModel] = useState('')
  const [status, setStatus] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const params = {}
    if (make.trim()) params.make = make.trim()
    if (model.trim()) params.model = model.trim()
    if (status) params.status = status
    onSearch(params)
  }

  const handleReset = () => {
    setMake('')
    setModel('')
    setStatus('')
    onSearch({})
  }

  return (
    <form className="searchbar" onSubmit={handleSubmit}>
      <input
        type="text"
        className="searchbar__input"
        placeholder="Marca (ej. Toyota)"
        value={make}
        onChange={(e) => setMake(e.target.value)}
      />
      <input
        type="text"
        className="searchbar__input"
        placeholder="Modelo (ej. Corolla)"
        value={model}
        onChange={(e) => setModel(e.target.value)}
      />
      <select
        className="searchbar__select"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        <option value="">Todos los estados</option>
        <option value="available">Disponible</option>
        <option value="unavailable">No disponible</option>
      </select>
      <button type="submit" className="searchbar__btn searchbar__btn--primary">
        Buscar
      </button>
      <button type="button" className="searchbar__btn searchbar__btn--ghost" onClick={handleReset}>
        Limpiar
      </button>
    </form>
  )
}
