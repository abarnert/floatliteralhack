# floatliteralhack
A quick hack to make float literals save a str so Decimal can use it

This just hacks the tokenizer to replace any number literal that looks
like a float literal to instead be a constructor for a FloatLiteral
subtype that remembers the token's string.

See floatliteral_ast for an alternative implementation that transforms
the AST instead of the tokens. The disadvantage of that implementation
is that by the time you've got an AST, the literal token has already
been transformed into a float; we can convert it back by calling str
on it, but that only works for simple cases like Decimal(1.2) (because
repr(1.2) is '1.2'), not in general. On the other hand, it means that
inspecting the source and so on gives you the right information.

At any rate, either way, this is only meant to let people test the
idea for unexpected performance and/or usability issues.

If you're interested in the more general issue of how to hack Python 
without actually hacking Python, I wrote [a blog post][1] that you
might find interesting.

  [1]: http://stupidpythonideas.blogspot.com/2015/06/hacking-python-without-hacking-python.html
