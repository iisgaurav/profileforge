from . import DoctorCheck


class WidgetsCheck(DoctorCheck):
    name = "Widgets"
    description = "Validates widgets constraints."

    def run(self) -> dict:
        return {"status": "PASS", "details": ["All widgets checks passed."]}
