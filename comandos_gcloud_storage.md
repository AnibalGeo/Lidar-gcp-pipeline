# Referencia: gcloud storage CLI

**Reemplazo moderno de gsutil. Usar siempre `gcloud storage` en proyectos nuevos.**

---

## 1. Buckets — Gestión

### Crear bucket
```bash
gcloud storage buckets create gs://[NOMBRE-BUCKET] \
  --project=[PROYECTO] \
  --location=us-central1 \
  --default-storage-class=STANDARD \
  --uniform-bucket-level-access
```

### Listar buckets del proyecto
```bash
gcloud storage buckets list --project=[PROYECTO]
```

### Ver detalles de un bucket
```bash
gcloud storage buckets describe gs://[BUCKET]
```

### Eliminar bucket (debe estar vacío)
```bash
gcloud storage buckets delete gs://[BUCKET]
```

### Eliminar bucket con contenido
```bash
gcloud storage rm -r gs://[BUCKET]
```

---

## 2. Listar Archivos

### Listar contenido raíz
```bash
gcloud storage ls gs://[BUCKET]/
```

### Listar con detalles (tamaño, fecha)
```bash
gcloud storage ls -l gs://[BUCKET]/raw/
```

### Listar recursivamente
```bash
gcloud storage ls -r gs://[BUCKET]/**
```

### Filtrar por extensión
```bash
gcloud storage ls gs://[BUCKET]/raw/**/*.laz
```

### Tamaño total del bucket
```bash
gcloud storage du -s gs://[BUCKET]
```

### Tamaño por carpeta
```bash
gcloud storage du gs://[BUCKET]/raw/sector_1/
```

---

## 3. Subir Archivos (Upload)

### Subir un archivo
```bash
gcloud storage cp archivo.laz gs://[BUCKET]/raw/sector_1/
```

### Subir múltiples archivos explícitos
```bash
gcloud storage cp archivo1.laz archivo2.laz gs://[BUCKET]/raw/sector_1/
```

### Subir carpeta completa (recursivo)
```bash
gcloud storage cp -r ./Sectores gs://[BUCKET]/raw/
```

### Subir con paralelismo (más rápido)
```bash
gcloud storage cp -r ./Sectores gs://[BUCKET]/raw/ \
  --parallel-composite-upload-component-size=50M
```

### Subir solo si no existe (no sobrescribir)
```bash
gcloud storage cp archivo.laz gs://[BUCKET]/raw/sector_1/ --no-clobber
```

---

## 4. Descargar Archivos (Download)

### Descargar un archivo
```bash
gcloud storage cp gs://[BUCKET]/raw/sector_1/archivo.laz ./
```

### Descargar carpeta completa
```bash
gcloud storage cp -r gs://[BUCKET]/raw/ ./datos_locales/
```

### Descargar con sincronización (rsync-style)
```bash
gcloud storage rsync -r gs://[BUCKET]/raw/ ./datos_locales/
```

---

## 5. Mover y Renombrar

### Mover archivo dentro del mismo bucket
```bash
gcloud storage mv gs://[BUCKET]/raw/old_path/archivo.laz gs://[BUCKET]/raw/new_path/
```

### Renombrar archivo
```bash
gcloud storage mv gs://[BUCKET]/old_name.laz gs://[BUCKET]/new_name.laz
```

### Mover entre buckets
```bash
gcloud storage mv gs://[BUCKET-A]/archivo.laz gs://[BUCKET-B]/
```

---

## 6. Eliminar

### Eliminar un archivo
```bash
gcloud storage rm gs://[BUCKET]/raw/archivo.laz
```

### Eliminar múltiples archivos
```bash
gcloud storage rm gs://[BUCKET]/raw/sector_1/*.laz
```

### Eliminar carpeta recursivo
```bash
gcloud storage rm -r gs://[BUCKET]/raw/sector_1/
```

### Eliminar todo el contenido de un bucket
```bash
gcloud storage rm -r gs://[BUCKET]/**
```

---

## 7. Permisos y Acceso

### Hacer público un archivo
```bash
gcloud storage objects update gs://[BUCKET]/archivo.laz \
  --add-acl-grant=entity=AllUsers,role=READER
```

### Generar URL firmada (acceso temporal)
```bash
gcloud storage sign-url gs://[BUCKET]/archivo.laz \
  --duration=1h \
  --private-key-file=key.json
```

### Ver permisos de un objeto
```bash
gcloud storage objects describe gs://[BUCKET]/archivo.laz
```

---

## 8. Metadata y Versiones

### Ver metadata de archivo
```bash
gcloud storage objects describe gs://[BUCKET]/archivo.laz
```

### Habilitar versionado del bucket
```bash
gcloud storage buckets update gs://[BUCKET] --versioning
```

### Listar versiones de un archivo
```bash
gcloud storage ls -a gs://[BUCKET]/archivo.laz
```

### Restaurar versión anterior
```bash
gcloud storage cp gs://[BUCKET]/archivo.laz#[GENERATION-ID] gs://[BUCKET]/archivo.laz
```

---

## 9. Storage Classes (Clases de almacenamiento)

```
STANDARD       → Acceso frecuente              ($0.020/GB/mes)
NEARLINE       → Acceso mensual                ($0.010/GB/mes)
COLDLINE       → Acceso trimestral             ($0.004/GB/mes)
ARCHIVE        → Acceso anual                  ($0.0012/GB/mes)
```

### Cambiar clase de un archivo
```bash
gcloud storage objects update gs://[BUCKET]/archivo.laz \
  --storage-class=NEARLINE
```

### Aplicar lifecycle rule (mover a NEARLINE después de 30 días)
```bash
# Crear lifecycle.json
cat > lifecycle.json <<EOF
{
  "rule": [{
    "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
    "condition": {"age": 30}
  }]
}
EOF

gcloud storage buckets update gs://[BUCKET] \
  --lifecycle-file=lifecycle.json
```

---

## 10. Comandos Útiles para LiDAR/Geomática

### Verificar integridad de archivos subidos
```bash
gcloud storage hash gs://[BUCKET]/raw/sector_1/archivo.laz
```

### Subir con metadata personalizada
```bash
gcloud storage cp archivo.laz gs://[BUCKET]/raw/sector_1/ \
  --custom-metadata="epsg=25830,sector=1,epoch=old"
```

### Filtrar archivos por metadata
```bash
gcloud storage ls -l gs://[BUCKET]/raw/** \
  | grep "Custom-Metadata.*sector=1"
```

---

## 11. Equivalencia Rápida gsutil → gcloud storage

| gsutil | gcloud storage |
|--------|----------------|
| `gsutil mb gs://[B]` | `gcloud storage buckets create gs://[B]` |
| `gsutil ls gs://[B]` | `gcloud storage ls gs://[B]` |
| `gsutil ls -lh gs://[B]` | `gcloud storage ls -l gs://[B]` |
| `gsutil cp a.laz gs://[B]/` | `gcloud storage cp a.laz gs://[B]/` |
| `gsutil -m cp -r ./d gs://[B]/` | `gcloud storage cp -r ./d gs://[B]/` |
| `gsutil rm gs://[B]/a.laz` | `gcloud storage rm gs://[B]/a.laz` |
| `gsutil mv a.laz b.laz` | `gcloud storage mv a.laz b.laz` |
| `gsutil du -s gs://[B]` | `gcloud storage du -s gs://[B]` |
| `gsutil rsync src dst` | `gcloud storage rsync src dst` |

---

## 12. Tu Caso Específico — Comandos Listos

### Verificar tu bucket actual
```bash
gcloud storage ls -l gs://lidar-pnoa-portfolio/raw/**
```

### Ver tamaño total
```bash
gcloud storage du -s gs://lidar-pnoa-portfolio
```

### Subir nuevos archivos procesados (cuando los tengas)
```bash
gcloud storage cp ./processed/*.tif gs://lidar-pnoa-portfolio/processed/sector_1/dtm/
```

### Descargar un archivo para verificar local
```bash
gcloud storage cp gs://lidar-pnoa-portfolio/raw/sector_1/20240703_old_epsg25830.laz ./verificacion/
```

---

## 13. Best Practices

```
✅ Usar nombres descriptivos en buckets ([proyecto]-[propósito])
✅ Habilitar versionado en buckets de producción
✅ Aplicar lifecycle rules para optimizar costos
✅ Usar uniform bucket-level access (más simple que ACLs por archivo)
✅ Etiquetar buckets con labels para tracking de costos
✅ Custom metadata para info crítica (CRS, fecha, sector)

❌ NO usar wildcards * en Windows CMD con gcloud (mismo problema que gsutil)
❌ NO subir archivos sin CRS asignado
❌ NO mezclar archivos de diferentes proyectos en un solo bucket
❌ NO usar STANDARD para datos archivados (gastas dinero innecesariamente)
```

---

## 14. Documentación Oficial

```
https://cloud.google.com/sdk/gcloud/reference/storage
https://cloud.google.com/storage/docs/gsutil-transition-to-gcloud
```
