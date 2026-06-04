---
mode: ask
description: Add NumPy-style docstring tests for the selected function
---

Add a NumPy-style docstring to the selected function with an `Examples` section using `doctest` format.

Requirements:
- Show at least one valid input and its expected output
- Show one edge case (e.g. empty list, boundary value, negative number)
- The examples must be runnable with `python -m doctest <file>`

After generating the docstring, verify it is correct by reasoning through each example.

If the function handles CET conversion, include one winter example and one summer example.
