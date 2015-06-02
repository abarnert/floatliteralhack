import ast
import importlib
import importlib.machinery
import decimal
import sys

def _call_with_frames_removed(f, *args, **kwargs):
    return f(*args, **kwargs)

class FloatLiteral(float):
    def __new__(cls, *args):
        obj = super().__new__(cls, *args)
        if args and len(args) == 1 and isinstance(args[0], str):
            obj._str = args[0]
        return obj
    # optionally use _str in repr/str

class Decimal(decimal.Decimal):
    def __new__(cls, value="0", *args, **kwargs):
        try:
            value = value._str
        except AttributeError:
            pass
        return super().__new__(cls, value, *args, **kwargs)

decimal.Decimal = Decimal

class FloatNodeWrapper(ast.NodeTransformer):
    def visit_Num(self, node):
        if isinstance(node.n, float):
            return ast.Call(func=ast.Name(id='FloatLiteral', ctx=ast.Load()),
                            args=[ast.Str(s=str(node.n))], keywords=[])
        return node

class FloatLiteralLoader(importlib.machinery.SourceFileLoader):
    def source_to_code(self, data, path, *, _optimize=-1):
        source = importlib._bootstrap.decode_source(data)
        tree = _call_with_frames_removed(compile, source, path, 'exec',
                                         dont_inherit=True,
                                         optimize=_optimize,
                                         flags=ast.PyCF_ONLY_AST)        
        tree = FloatNodeWrapper().visit(tree)
        ast.fix_missing_locations(tree)
        return _call_with_frames_removed(compile, tree, path, 'exec',
                                         dont_inherit=True,
                                         optimize=_optimize)

_real_pathfinder = sys.meta_path[-1]

class FloatLiteralFinder(type(_real_pathfinder)):
    @classmethod
    def find_module(cls, fullname, path=None):
        spec = _real_pathfinder.find_spec(fullname, path)
        if not spec: return spec
        loader = spec.loader
        loader.__class__ = FloatLiteralLoader
        return loader

sys.meta_path[-1] = FloatLiteralFinder
