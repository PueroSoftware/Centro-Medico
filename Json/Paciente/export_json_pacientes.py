import json
from pathlib import Path
from Gui_Paciente.Paciente_Crud import Paciente

def exportar_pacientes_a_json():
    out_dir = Path(__file__).parent / "Json" / "pacientes"
    out_dir.mkdir(parents=True, exist_ok=True)

    pacientes = Paciente.read_all()

    for p in pacientes:
        payload = {
            "id": p.id_paciente,
            "cedula_id": p.cedula_id,
            "nombres": p.nombres,
            "apellido_paterno": p.apellido_paterno,
            "apellido_materno": p.apellido_materno,
            "fecha_nacimiento": p.fecha_nacimiento.isoformat(),
            "email": p.email,
            "telefono": p.telefono,
            "direccion": p.direccion
        }
        file_path = out_dir / f"paciente_{p.id_paciente}.json"
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"✅ Exportados {len(pacientes)} pacientes a '{out_dir}'")

if __name__ == "__main__":
    exportar_pacientes_a_json()
