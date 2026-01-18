
"""
Use Case S-00)
Trivialer Fall einer statischen Funktion ohne 3rp party library nutzung.
"""

def correct_asserts_indent(code: str) -> str:
    """Corrects the indentation of assert statements in the given code.
    """
    if not isinstance(code, str):
        raise TypeError("Input must be a string")

    lines = [l.strip() for l in code.strip().split("\n")]
    lines = [lines[0]] + [" " * 8 + l for l in lines[1:] if len(l) > 0]
    return "\n".join(lines)

