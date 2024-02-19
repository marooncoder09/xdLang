# from pathlib import Path

# import rich
# import typer
# from lark.tree import pydot__tree_to_png

# from xdlang.pipeline.parser import Parser
# from xdlang.pipeline.ast_builder import AstBuilder
# from xdlang.pipeline.ir_generator import IRGenerator 


# app = typer.Typer()


# @app.command()
# def build():
#     pass


# @app.command(help="Compiles and runs an xd program with a lot of debug info.")
# def run(input_file: Path):
#     print("XD Compiler")
#     print(f"Compiling and running {input_file}")

#     parser = Parser()
#     with input_file.open("rt") as f:
#         tree = parser.parse_text(f.read())
#     rich.print(tree)

#     pydot__tree_to_png(tree, str(input_file.with_suffix(".png")), rankdir="TB")

#     transformed = AstBuilder().transform(tree)
#     rich.print(transformed)

#     # Generate LLVM IR from the AST
#     ir_generator = IRGenerator()
#     ir_generator.generate(transformed)

#     print(ir_generator.module)

# def main():
#     app()


# if __name__ == "__main__":
#     app()


from pathlib import Path

import rich
import typer
from lark.tree import pydot__tree_to_png
from ctypes import CFUNCTYPE, c_int

from xdlang.pipeline.parser import Parser
from xdlang.pipeline.ast_builder import AstBuilder
from xdlang.pipeline.ir_generator import IRGenerator 

from llvmlite import binding as llvm

app = typer.Typer()

def print_module(module):
    print("LLVM IR Module:")
    if isinstance(module, str):
        print(module)
    else:
        print("Module is not a string")

def execute_module(module):
    # Initialize LLVM
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    # Create an execution engine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly(str(module))
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    # Run the main function
    main_func_ptr = engine.get_function_address("main")
    cfunc = CFUNCTYPE(c_int)(main_func_ptr)
    result = cfunc()

    return result

@app.command()
def build():
    pass

@app.command(help="Compiles and runs an xd program with a lot of debug info.")
def run(input_file: Path):
    print("XD Compiler")
    print(f"Compiling and running {input_file}")

    parser = Parser()
    with input_file.open("rt") as f:
        tree = parser.parse_text(f.read())
    rich.print(tree)

    pydot__tree_to_png(tree, str(input_file.with_suffix(".png")), rankdir="TB")

    transformed = AstBuilder().transform(tree)
    rich.print(transformed)

    # Generate LLVM IR from the AST
    ir_generator = IRGenerator()
    ir_generator.generate(transformed)

    # Print the LLVM IR module
    print_module(ir_generator.module)

    # Execute the LLVM IR
    result = execute_module(ir_generator.module)
    print("Output:", result)

def main():
    app()

if __name__ == "__main__":
    app()
