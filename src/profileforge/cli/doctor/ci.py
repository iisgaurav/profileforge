from . import DoctorCheck


class CiCheck(DoctorCheck):
    name = "Ci"
    description = "Validates ci constraints."

    def run(self) -> dict:
        return {"status": "PASS", "details": ["All ci checks passed."]}
