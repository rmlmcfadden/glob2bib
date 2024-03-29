# `glob2bib`: a bibliography generator for [BibTeX] and [BibLaTeX]/[Biber]

Bibliography management is a tedious, but a necessary endeavor when writing any
technical document. Naturally, one accumulates many references while researching
a topic and it is often convenient to organize them in some "centralized" manner
(e.g., a large, monolithic `.bib` file or several smaller ones). Instead of
copying the whole collection into every project, it is preferable to include
only those entries that are actually needed. This not only keeps the document
source uncluttered, but also prevents unecessarily long LaTeX compile times due
to needlessly parsing over a large number of unused `.bib` entries. Of course,
doing this manually is a nuisance and should be avoided at all costs. Thanks to
`glob2bib`, one never needs to resort to such primitive sorting practices again!

Taking an `.aux` file (generated during the compilation of a `.tex` source) and
adirectory as input, `glob2bib`:
1. extracts all the citation keys listed in the `.aux` file.
2. recursively finds all the `.bib` files found within the specified directory.
3. extracts all the entries from the `.bib` files whose keys match those in the `.aux` file.
4. prints the extracted entries to the terminal or (optionally) writes them to a file.

For convenience, `glob2bib` works for `.aux` files generated by both [BibTeX] and
[BibLaTeX]/[Biber] workflows. Similarly, it can also optionally convert unicode
greek literals found in the extracted entries to (escaped) greek math [TeX]
commands. The latter feature is particularly useful when different documents use
different [TeX] engines (e.g., [pdfTeX] or [LuaTeX]).

## Installation

`glob2bib` is just a simple Python script with no external dependencies. For
convenience, a `Makefile` is included for lazy integration into *nix systems.
Installation is as easy as:
```
make install
```
Note that, as per usual, superuser privilages are required for this.

## Usage

Typical use looks like:
```
glob2bib document.aux /path/to/bib/database -o references.bib
```
which will output the extracted entries to a new `.bib` file `references.bib`.

A full discription of all input options can be obtained using:
```
glob2bib --help
```
which will print:
```
usage: glob2bib [-h] [-v] [-o OUTPUT] [-s] [-b] [-l] [-a] [-u] aux_file bib_dir

glob2bib: a bibliography generator for BibTeX and BibLaTeX/Biber

positional arguments:
  aux_file              auxillary file (.aux) from LaTeX compilation
  bib_dir               directory to recursively glob for .bib files

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        name of the output file to write the extracted .bib entries to
  -s, --substitute-unicode
                        substitute unicode greek literals with (escaped) greek math TeX commands
  -b, --biblatex        assume BibLaTeX/Biber as the bibliography management backend
  -l, --long-journal-titles
                        substitute abbreviated journal titles with their full names
  -a, --abbreviated-journal-titles
                        substitute full journal titles with their abbreviated names
  -u, --url-swap        swap the url field for the doi in each entry

Copyright (c) 2019-2022 Ryan M. L. McFadden
```

## Caveats

It is assumed that each `.bib` entry is of the form:
```
@article{key,
   author = "...",
   title = "...",
   ...
   doi = "...",
   url = "..."
}

```
where the most crucial feature is the ending, which consists solely of a lone
`}` on the line trailing the last entry data. As is, `glob2bib` will fail to
parse `.bib` entries that do not comply with this formatting.

[TeX]: https://ctan.org/pkg/tex
[LuaTeX]: https://ctan.org/pkg/luatex
[pdfTeX]: https://ctan.org/pkg/pdftex
[BibTeX]: https://ctan.org/pkg/bibtex
[BibLaTeX]: https://ctan.org/pkg/biblatex
[Biber]: https://ctan.org/pkg/biber
