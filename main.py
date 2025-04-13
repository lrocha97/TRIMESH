from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import trimesh
import tempfile
import os

app = FastAPI()

# Permitir CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analisar/")
async def analisar_malha(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".glb") as temp:
        temp.write(await file.read())
        temp.flush()
        mesh = trimesh.load(temp.name)

    # Verifica se é uma cena e converte em uma malha combinada
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate([g for g in mesh.geometry.values()])

    if isinstance(mesh, trimesh.Trimesh):
        resultado = {
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "area": float(mesh.area),
            "volume": float(mesh.volume),
            "bounding_box": mesh.bounding_box.bounds.tolist()
        }
    else:
        resultado = {"erro": "Arquivo não contém uma malha válida."}

    os.remove(temp.name)
    return resultado
