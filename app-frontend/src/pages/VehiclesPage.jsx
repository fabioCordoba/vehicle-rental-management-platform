import { useEffect, useCallback } from 'react'
import { useVehicles } from '../hooks/useVehicles'
import { VehicleCard } from '../components/vehicles/VehicleCard'
import { SearchBar } from '../components/vehicles/SearchBar'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { Pagination } from '../components/ui/Pagination'
import './VehiclesPage.css'

export function VehiclesPage() {
  const { vehicles, meta, loading, error, fetchVehicles, searchVehicles, fetchPage } = useVehicles()

  useEffect(() => {
    fetchVehicles({}, true)
  }, [fetchVehicles])

  const handleSearch = useCallback((params) => {
    if (Object.keys(params).length === 0) {
      fetchVehicles({}, true)
    } else {
      searchVehicles(params)
    }
  }, [fetchVehicles, searchVehicles])

  const total = meta.count || vehicles.length

  return (
    <div className="vehicles-page">
      <div className="vehicles-page__header">
        <h1 className="vehicles-page__title">Vehículos disponibles</h1>
        <p className="vehicles-page__subtitle">
          Encuentra el vehículo ideal y solicita tu alquiler.
        </p>
      </div>

      <SearchBar onSearch={handleSearch} />

      {loading && <LoadingSpinner message="Cargando vehículos…" />}

      {!loading && error && (
        <div className="vehicles-page__error">
          <p>⚠️ {error}</p>
        </div>
      )}

      {!loading && !error && vehicles.length === 0 && (
        <div className="vehicles-page__empty">
          <span>🔍</span>
          <p>No se encontraron vehículos con esos criterios.</p>
        </div>
      )}

      {!loading && vehicles.length > 0 && (
        <>
          <p className="vehicles-page__count">
            {meta.next || meta.previous
              ? `Mostrando ${vehicles.length} de ${total} vehículo${total !== 1 ? 's' : ''}`
              : `${total} vehículo${total !== 1 ? 's' : ''} encontrado${total !== 1 ? 's' : ''}`
            }
          </p>
          <div className="vehicles-grid">
            {vehicles.map((v) => (
              <VehicleCard key={v.id} vehicle={v} />
            ))}
          </div>
          <Pagination
            meta={meta}
            showing={vehicles.length}
            onPrev={() => fetchPage(meta.previous)}
            onNext={() => fetchPage(meta.next)}
          />
        </>
      )}
    </div>
  )
}
