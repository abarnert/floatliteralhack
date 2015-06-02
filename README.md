# floatliteralhack
A quick hack to make float literals save a str so Decimal can use it

The right way to do this would be to change the parser, so that we
generate a Num node with a str in it, or something equivalent. As a
quick&dirty import hack solution that just modifies the AST after
parsing, we can't do that; all we can do is call str on the float in
the Num node. This is good enough to make Decimal(1.2) give you the
right result (because repr(1.2) is '1.2'), but not good enough in
general. It's only meant to let people test the idea for performance
and/or usability issues.
