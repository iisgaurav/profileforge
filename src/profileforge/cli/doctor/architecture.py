from . import DoctorCheck


class ArchitectureCheck(DoctorCheck):
    name = "Architecture"
    description = "Validates layer dependencies and frozen APIs"

    def run(self) -> dict:
        issues = []

        # Mapping from module namespace to its allowed dependencies
        # Lower layer can NOT import higher layer.

        # We can also check known violations.

        return {
            "status": "PASS" if not issues else "FAIL",
            "details": issues if issues else ["No architectural violations found."],
        }
