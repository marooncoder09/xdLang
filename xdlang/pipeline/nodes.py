import abc
from typing import List

class Node(abc.ABC):
    """Base class for all AST nodes."""
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.__class__.__name__}(line={self.line}, column={self.column})"

class ExprNode(Node):
    """Base class for expression nodes."""
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

class StmtNode(Node):
    """Base class for statement nodes."""
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

class LiteralExprNode(ExprNode):
    """Node representing a literal expression."""
    def __init__(self, line: int, column: int, value: int) -> None:
        super().__init__(line, column)
        self.value = value

class ReturnStmtNode(StmtNode):
    """Node representing a return statement."""
    def __init__(self, line: int, column: int, expr: ExprNode) -> None:
        super().__init__(line, column)
        self.expr = expr

class BlockNode(Node):
    """Node representing a block of statements."""
    def __init__(self, line: int, column: int, stmts: List[StmtNode]) -> None:
        super().__init__(line, column)
        self.stmts = stmts

class FuncDefNode(Node):
    """Node representing a function definition."""
    def __init__(
        self, line: int, column: int, var_type: str, identifier: str, body: BlockNode
    ) -> None:
        super().__init__(line, column)
        self.var_type = var_type
        self.identifier = identifier
        self.body = body

class ProgramNode(Node):
    """Node representing the root of the AST."""
    def __init__(self, line: int, column: int, func_defs: List[FuncDefNode]) -> None:
        super().__init__(line, column)
        self.func_defs = func_defs

class VarDeclNode(StmtNode):
    """Node representing a variable declaration."""
    def __init__(self, line: int, column: int, var_type: str, identifier: str):
        super().__init__(line, column)
        self.var_type = var_type
        self.identifier = identifier

class AssignmentNode(StmtNode):
    """Node representing an assignment statement."""
    def __init__(self, line: int, column: int, identifier: str, expr: ExprNode):
        super().__init__(line, column)
        self.identifier = identifier
        self.expr = expr

class InputStmtNode(StmtNode):
    """Node representing an input statement."""
    def __init__(self, line: int, column: int):
        super().__init__(line, column)

class PrintStmtNode(StmtNode):
    """Node representing a print statement."""
    def __init__(self, line: int, column: int, expr: ExprNode):
        super().__init__(line, column)
        self.expr = expr
