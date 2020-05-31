import sys

def define_ast(output_dir, base_name, types):
    path = output_dir + '/' + base_name + '.java'
    with open(path, 'w') as out_file:
        out_file.write('package com.andrewhalle.lox;\n')
        out_file.write('\n')
        out_file.write('import java.util.List;\n')
        out_file.write('\n')
        out_file.write('abstract class ' + base_name + ' {\n')
        define_visitor(out_file, base_name, types)
        for t in types:
            s = t.split(':')
            class_name = s[0].strip()
            fields = s[1].strip()
            define_type(out_file, base_name, class_name, fields)

        out_file.write('\n')
        out_file.write('  abstract <R> R accept(Visitor<R> visitor);\n')
        out_file.write('}\n')

def define_visitor(writer, base_name, types):
    writer.write('  interface Visitor<R> {\n')
    for t in types:
        type_name = t.split(':')[0].strip()
        writer.write('    R visit' + type_name + base_name + '(' +
            type_name + ' ' + base_name.lower() + ');\n')
    writer.write('  }\n')
    writer.write('\n')

def define_type(writer, base_name, class_name, field_list):
    writer.write('  static class ' + class_name +
        ' extends ' + base_name + ' {\n')
    writer.write('    ' + class_name + '(' + field_list + ') {\n')

    fields = field_list.split(',')
    for field in fields:
        name = field.strip().split(' ')[1]
        writer.write('      this.' + name + ' = ' + name + ';\n')

    writer.write('    }\n')

    writer.write('\n')
    writer.write('    @Override\n')
    writer.write('    <R> R accept(Visitor<R> visitor) {\n')
    writer.write('      return visitor.visit' + class_name +
        base_name + '(this);\n')
    writer.write('    }\n')

    writer.write('\n')
    for field in fields:
        writer.write('    final ' + field.strip() + ';\n')

    writer.write('  }\n')
    writer.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: generate_ast <output directory>')
        sys.exit(-1)
    output_dir = sys.argv[1]
    define_ast(output_dir, 'Expr', [
        'Assign   : Token name, Expr value',
        'Binary   : Expr left, Token operator, Expr right',
        'Call     : Expr callee, Token paren, List<Expr> arguments',
        'Grouping : Expr expression',
        'Literal  : Object value',
        'Logical  : Expr left, Token operator, Expr right',
        'Unary    : Token operator, Expr right',
        'Variable : Token name'
    ])
    define_ast(output_dir, 'Stmt', [
        'Block      : List<Stmt> statements',
        'Expression : Expr expression',
        'Function   : Token name, List<Token> params, List<Stmt> body',
        'If         : Expr condition, Stmt thenBranch, Stmt elseBranch',
        'Print      : Expr expression',
        'Return     : Token keyword, Expr value',
        'Var        : Token name, Expr initializer',
        'While      : Expr condition, Stmt body'
    ])
