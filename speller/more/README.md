# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

An invented long word said to mean a lung disease caused by inhaling very fine ash and sand dust.

## According to its man page, what does `getrusage` do?

It times data which are given from the function calculate.

## Per that same man page, how many members are in a variable of type `struct rusage`?

Two member. First member is "before" and the second member is "after".

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

We pass "before" and "after" by reference because if we pass them by value it will take a lot of memory. It also can cause a stack overflow.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

We start the "for" loop by getting the next character in the file and do it until we reach the End of the file (EOF). With the first "if" function we check if a character is alphabetical
or an aprostophie. If so we append it to "word[]". Too long strings to be words are ignored.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

fscanf will probably ignore special characters like . , ! ? . We can also get trouble if we get a longer string than expected. This can also cause a segmentation fault.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

constant means that parameters can't get changed.
