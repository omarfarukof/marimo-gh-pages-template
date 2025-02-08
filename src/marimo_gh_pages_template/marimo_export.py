#!/usr/bin/env python3

import os
import subprocess

format_ext = {
    "html": ".html",
    "html-wasm": ".html",
    "script": ".py",
    "ipynb": ".ipynb",
    "md": ".md",
}


def get_export_cmd(
    notebook_path: str, output: str=None, 
    export_format:str="html",   # html, html-wasm, ipynb, md, script
    mode:str="run",             # run, edit
    show_code:bool=True, watch:bool=False, sandbox:bool=False, 
    sort:str="topological"      # topological, top-down
    ) -> list[str]:

    if output is None:
        output = notebook_path.replace(".py", format_ext[export_format])
        
    cmd = ["marimo", "export", export_format, notebook_path, "-o", output]
    # Watch the notebook for changes and automatically export
    if watch:
        cmd.append("--watch")
    else:
        cmd.append("--no-watch")

    # Export to HTML
    if export_format == "html":
        if sandbox:
            cmd.append("--sandbox")

        if show_code:
            cmd.append("--include-code")
        else:
            cmd.append("--no-include-code")


    # Export to IPYNB
    if export_format == "ipynb":
        if sandbox:
            cmd.append("--sandbox")

        if show_code:
            cmd.append("--include-code")
        else:
            cmd.append("--no-include-code")

        if sort not in ["topological", "top-down"]:
            raise ValueError("sort must be either 'topological' or 'top-down'")
        cmd += ["--sort", sort]

    # Export to HTML WebAssembly
    if export_format == "html-wasm":
        if mode not in ["run", "edit"]:
            raise ValueError("mode must be either 'run' or 'edit'")

        # Export Mode
        cmd += ["--mode", mode]
        if show_code:
            cmd.append(f"--show-code")
        else:
            cmd.append(f"--no-show-code")

    
    return cmd

def export(
    notebook_path: str, output: str=None, 
    export_format:str="html",   # html, html-wasm, ipynb, md, script
    mode:str="run",             # run, edit
    show_code:bool=True, watch:bool=False, sandbox:bool=False, 
    sort:str="topological"      # topological, top-down
    ) -> bool:

    if output is None:
        output = notebook_path.replace(".py", format_ext[export_format])
        
    cmd = get_export_cmd(notebook_path, output, export_format, mode, show_code, watch, sandbox, sort)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Exported {notebook_path} to {output}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error exporting {notebook_path}:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error exporting {notebook_path}: {e}")
        return False

def export_executable(notebook_path: str, output: str=None, watch=False, sandbox=False) -> bool:
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="run",
        show_code=True,
        watch=watch,
        sandbox=sandbox,
        sort="topological"
    )

def export_editable(notebook_path: str, output: str=None, watch=False) -> bool:
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="edit",
        show_code=True,
        watch=watch
    )

def export_app(notebook_path: str, output: str=None) -> bool:
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="run",
        show_code=False
    )


# # For Testing
# if __name__ == "__main__":
#     export(notebook_path="notebooks/fibonacci.py", output="notebooks/web/fibonacci.html")
#     export_executable(notebook_path="notebooks/fibonacci.py", output="notebooks/web/fibonacci_exe.html")
#     export_editable(notebook_path="notebooks/fibonacci.py", output="notebooks/web/fibonacci_edit.html")
#     export_app(notebook_path="notebooks/fibonacci.py", output="notebooks/web/fibonacci_app.html")

#     pass