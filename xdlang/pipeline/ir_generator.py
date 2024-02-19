from llvmlite import ir
from .nodes import *  # Import your AST node classes

class IRGenerator:
    def __init__(self):
        self.module = ir.Module(name="xdlang_module")
        self.builder = None  

    def generate(self, node):
        method_name = 'generate_' + type(node).__name__
        # generator = getattr(self, method_name, self.generic_generate)
        # generator(node)
        generator = self.generate_FuncDefNode(self, node)
        print("CP1", generator)
        return str(self.module)


    def generic_generate(self, node):
        raise Exception(f"Unimplemented IR generation for {type(node)}")

    def generate_ProgramNode(self, node):
        for func_def in node.func_defs:
            self.generate(func_def) 

    def generate_FuncDefNode(self, node):
        # Define the function type based on the node's signature
        return_type = ir.IntType(32)  # Assuming the function returns an integer, adjust as needed
        arg_types = []  # List of argument types, adjust as needed

        # Example: if the function takes an integer argument:
        arg_types.append(ir.IntType(32))

        # Create the function type
        func_type = ir.FunctionType(return_type, arg_types)

        # Create the function
        func = ir.Function(self.module, func_type, name=node.identifier)

        # Append a basic block to the function
        block = func.append_basic_block(name="entry")

        # Set the IRBuilder to start inserting instructions into the basic block
        self.builder = ir.IRBuilder(block)

        # Generate IR for the function body
        for stmt in node.body.stmts:
            self.generate(stmt)




