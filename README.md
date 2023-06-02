# Concurrency Testing

## Demonstration of concurrency (and parallelization) methods in various languages

This project is intended to demonstrate (within reason) various methods for providing concurrency
in different programming languages.  While benchmarking is necessary for comparison, it is *NOT*
the focus.  All benchmarks are, first and foremost, to provide a general understanding of
processing time impact for each method for a given CPU-bound task and a given IO-bound task.  The
secondary purpose for benchmarks are for generalized comparisons between implementations in
different programming languages.

Intent:
- Gain an understanding of concurrency methods and their impact on CPU-bound and IO-bound processes
- Gain an understanding of concurrency method impmentation differences between programming
languages
- Provide _basic_ concurrency method implementation examples

What this is *NOT*:
- A competition, of any kind
- A performance optimization exercise

# CPU-Bound Task

Given an array of numbers, calculate the maximum deviation between each value and the rest of the
values in the array.

_NOTE_: There are certainly ways where the calculation method could be optimized, but it is
intentionally simple and unoptimized to provide as much consistency for the given work load.

# IO-Bound Task

_TODO_
_Leaning toward disk IO in order to prevent undue load on websites_
