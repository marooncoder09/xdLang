from typing import Any
from llvmlite import ir
from lark import Token, Transformer

import xdlang.pipeline.nodes as xdnodes


class AstBuilder(Transformer):
    def LITERAL(self, item: Token) -> xdnodes.LiteralExprNode:
        return xdnodes.LiteralExprNode(item.line, item.column, int(item.value))

    def expr(self, items: list[Any]) -> xdnodes.ExprNode:
        return items[0]

    def return_stmt(self, items: list[Any]) -> xdnodes.ReturnStmtNode:
        expr = items[1]
        return xdnodes.ReturnStmtNode(expr.line, expr.column, expr)

    def block(self, items: list[Any]) -> xdnodes.BlockNode:
        # Find the first Token in the items list for line and column numbers
        line = column = None
        for item in items:
            if isinstance(item, Token):
                line = item.line
                column = item.column
                break
            elif isinstance(item, list) and item and isinstance(item[0], Token):
                line = item[0].line
                column = item[0].column
                break
        
        # Fallback if no Token was found
        if line is None or column is None:
            line = column = 0
        
        statements = [i for i in items if isinstance(i, xdnodes.StmtNode)]
        return xdnodes.BlockNode(line, column, statements)


    def func_def(self, items: list[Any]) -> xdnodes.FuncDefNode:
        type = items[0].value
        identifier = items[1].value
        body = items[2]
        return xdnodes.FuncDefNode(
            items[0].line, items[0].column, type, identifier, body
        )

    def program(self, items: list[Any]) -> xdnodes.ProgramNode:
        return xdnodes.ProgramNode(0, 0, items)

    def var_decl(self, items: list[Any]) -> xdnodes.VarDeclNode:
        type = items[0].value
        identifier = items[1].value
        return xdnodes.VarDeclNode(items[0].line, items[0].column, type, identifier)

    def assignment(self, items: list[Any]) -> xdnodes.AssignmentNode:
        identifier, expr = items[0].value, items[1]
        return xdnodes.AssignmentNode(items[0].line, items[0].column, identifier, expr)

    def input_stmt(self, items: list[Any]) -> xdnodes.InputStmtNode:
        # Assuming the input statement doesn't have any arguments to process
        # and that the line and column information is to be derived from the first item if it's a token or a fixed value
        line = items[0].line if isinstance(items[0], Token) else 0
        column = items[0].column if isinstance(items[0], Token) else 0
        return xdnodes.InputStmtNode(line, column)

    def print_stmt(self, items: list[Any]) -> xdnodes.PrintStmtNode:
        # Assuming the expression to print is the first item in the list
        expr = items[0]
        return xdnodes.PrintStmtNode(expr.line, expr.column, expr)
    def generate_FuncDefNode(self, node):
        # Define the function type based on the node's signature
        func_type = ir.FunctionType(...)
        func = ir.Function(self.module, func_type, name=node.identifier)
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        # Generate IR for the function body
        for stmt in node.body.stmts:
            self.generate(stmt)