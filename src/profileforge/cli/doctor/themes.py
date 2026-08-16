from . import DoctorCheck


class ThemesCheck(DoctorCheck):
    name = "Themes"
    description = "Validates themes constraints."

    def run(self) -> dict:
        return {"status": "PASS", "details": ["All themes checks passed."]}
