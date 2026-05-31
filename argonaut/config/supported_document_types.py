# Standard imports
from pathlib import Path

# Third party imports

# Local imports
from argonaut.templates.minimal_template import init_minimal_folder
from argonaut.config.document_type import DocumentType
from argonaut.templates.requirements_template import init_requirements_folder
from argonaut.templates.pcb_template import init_pcb_folder

SUPPORTED_DOCUMENT_TYPES = sorted(
    [
        DocumentType(
            "REQ",
            "Requirements Specification",
            "Requirements Specifications",
            Path("requirements"),
            separate_repo=False,
            init_function=init_requirements_folder,
        ),
        DocumentType(
            "PCB",
            "KiCad PCB Project",
            "KiCad PCB Projects",
            Path("pcb"),
            separate_repo=True,
            init_function=init_pcb_folder,
        ),
        DocumentType(
            "SW",
            "Software Project",
            "Software Projects",
            Path("software"),
            separate_repo=True,
            init_function=init_minimal_folder,
        ),
        DocumentType(
            "FW",
            "Firmware Project",
            "Firmware Projects",
            Path("firmware"),
            separate_repo=True,
            init_function=init_minimal_folder,
        ),
        DocumentType(
            "RTL",
            "RTL Project",
            "RTL Projects",
            Path("rtl"),
            separate_repo=True,
            init_function=init_minimal_folder,
        ),
        DocumentType(
            "LIB",
            "Asset Library",
            "Asset Libraries",
            Path("libraries"),
            separate_repo=True,
            init_function=init_minimal_folder,
        ),
        # DocumentType("CAD", "Mechanical CAD part", Path("cad"), separate_repo=False),
    ]
)


def get_document_type_from_abbreviation(abbr: str) -> DocumentType:
    possible_matches = [x for x in SUPPORTED_DOCUMENT_TYPES if x.abbreviation == abbr]
    assert len(possible_matches) == 1, "Multiple document types have same abbreviation"
    return possible_matches[0]


def main():
    print(SUPPORTED_DOCUMENT_TYPES)


if __name__ == "__main__":
    main()
