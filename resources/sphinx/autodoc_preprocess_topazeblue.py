import re

def setup(app):
    app.connect('autodoc-process-docstring', pre_process_docstring)


# Regular expression pattern
_PATTERN = r'^\s*(:)(\w+)(:)\s+(.*)$'

# Replacement function
def _replace(match):
    return f"{match.group(1)}param {match.group(2)}{match.group(3)} {match.group(4)}"


def pre_process_docstring(app, what, name, obj, options, lines):
    """
    pre-processes docstrings in the format used in topaze.blue code
    
    This function is called before the docstring is parsed by autodoc. It modifies the docstring
    lines in place, then passing them back to autodoc. Changes made are the following:
    
    1. In topaze.blue code, for readability the `param` term in `:param variable: description` is implied,
    ie it only uses `:variable: description`. This function adds `param` before the variable name.
    
    2. If there is a line that ONLY has "---" plus whitespace then that line and everything after it 
    is removed 
    """
    new_lines = []
    for line in lines:
        if line.strip() == "---":
            break
        if re.match(_PATTERN, line):
            # If it matches, perform the replacement
            new_line = re.sub(_PATTERN, _replace, line)
            #print("Modified line:", new_line)
        else:
            new_line = line
        new_lines.append(new_line)
    lines[:] = new_lines  # Update the original list with modified lines
