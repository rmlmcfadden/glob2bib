#!/usr/bin/python3

"""
glob2bib: a bibliography generator for BibTeX and BibLaTeX/Biber

Taking an .aux file and directory as input:
1) get all the citation keys listed in the .aux file
2) recursively find all the .bib files found within the directory
3) extract all the entries with matching keys from the .bib files

Features:
- print the extracted entries to the terminal or write them to a file
- works for .aux files generated by both BibTeX or BibLaTeX/Biber
- optionally convert unicode greek literals found in entries to (escaped) greek
math TeX commands  
"""


# get the list of citation keys from an .aux file
def get_keys(aux_file, biblatex=False):
    # empty list to hold the citation keys
    keys = []

    # citation identifiers
    bibtex_citation = "\citation{"
    bibtex_empty_citation = "\citation{}\n"

    biblatex_citation = r"\abx@aux@cite{"
    biblatex_empty_citation = r"\abx@aux@cite{}" + "\n"

    revtex41_citation = "\citation{REVTEX41Control}\n"
    apsrev41_citation = "\citation{apsrev41Control}\n"

    revtex42_citation = "\citation{REVTEX42Control}\n"
    apsrev42_citation = "\citation{apsrev42Control}\n"

    revtex = [
        revtex41_citation,
        apsrev41_citation,
        revtex42_citation,
        apsrev42_citation,
    ]

    # open the .aux file
    with open(aux_file, "r") as fh:
        # read the lines
        for line in fh.readlines():
            # check for revtex garbage
            if any(line == r for r in revtex):
                continue

            # BibLaTeX backend
            if (
                biblatex == True
                and biblatex_citation in line
                and line != biblatex_empty_citation
            ):
                # strip away the strings around the key
                l = line.replace(biblatex_citation, "")
                l = l.replace("}", "")
                l = l.replace("\n", "")
                # check for multiple keys...
                if "," in l:
                    l2 = l.split(",")
                    # ...and append each of them to the list
                    for ll in l2:
                        keys.append(ll)
                else:
                    keys.append(l)

            # BibTeX backend
            if (
                biblatex == False
                and bibtex_citation in line
                and line != bibtex_empty_citation
            ):
                # strip away the strings around the key
                l = line.replace(bibtex_citation, "")
                l = l.replace("}", "")
                l = l.replace("\n", "")
                # check for multiple keys...
                if "," in l:
                    l2 = l.split(",")
                    # ...and append each of them to the list
                    for ll in l2:
                        keys.append(ll)
                else:
                    keys.append(l)

    # remove the duplicates and sort the keys
    keys = list(dict.fromkeys(keys))
    keys.sort()

    return keys


# replace unicode greek literals with (escaped) TeX greek math commands
def replace_greek(text):
    # greek letters and their english names
    greek_letter = [
        "α",
        "β",
        "γ",
        "Γ",
        "δ",
        "Δ",
        "ϵ",
        "ζ",
        "η",
        "θ",
        "Θ",
        "ι",
        "κ",
        "λ",
        "Λ",
        "μ",
        "ν",
        "π",
        "Π",
        "ρ",
        "σ",
        "Σ",
        "τ",
        "υ",
        "Υ",
        "ϕ",
        "Φ",
        "χ",
        "ψ",
        "Ψ",
        "ω",
        "Ω",
    ]
    english_name = [
        "alpha",
        "beta",
        "gamma",
        "Gamma",
        "delta",
        "Delta",
        "epsilon",
        "zeta",
        "eta",
        "theta",
        "Theta",
        "iota",
        "kappa",
        "lambda",
        "Lambda",
        "mu",
        "nu",
        "pi",
        "Pi",
        "rho",
        "sigma",
        "Sigma",
        "tau",
        "upsilon",
        "Upsilon",
        "phi",
        "Phi",
        "chi",
        "psi",
        "Psi",
        "omega",
        "Omega",
    ]

    # perform the substitution
    for gl, en in zip(greek_letter, english_name):
        text = text.replace(gl, "{$\\" + en + "$}")

    return text


# extract a list of .bib entries, whose keys match those in key_list, found in a list of .bib files
# inspired by: https://tex.stackexchange.com/a/146660
#
# Note: though it is quicker to open each .bib file once and loop through the
# citation keys, looping over all keys and then checking every file keeps the
# entries nicely ordered in the output :-).
def get_entires(key_list, bib_list, substitute_unicode=False):
    # empty list of entries
    entries = []

    # loop over all keys
    for key in key_list:
        # loop over all bibs
        for bib in bib_list:
            # read the bib file
            with open(bib, "r") as fh:
                # flag identifying if the line is an entry
                is_entry = False
                for line in fh.readlines():

                    # strip away the whitespace at the beginnning/end and...
                    sline = line.strip()

                    # ...move on to the next line if its blanck
                    if sline == "":
                        continue

                    # check if sline is the start of a new entry
                    if sline[0] == "@":
                        # check if this entry key is in the list of keys
                        if sline.split("{")[1].strip(",") == key:
                            # update the flag
                            is_entry = True
                            # create an empty string to hold the entry contents
                            entry = ""

                    # if the key is found, conditionally add the content to entry
                    if is_entry == True:

                        # beginnning of entry
                        if sline[0] == "@":
                            entry += sline + "\n"
                        # end of entry (always assumes a lonesome closing brace!)
                        elif sline == "}":
                            entry += sline + "\n\n"
                            # toggle the entry flag
                            is_entry = False
                            # append the entry to the entries list
                            entries.append(entry)
                        # skip commented out lines
                        elif sline[0] == "%":
                            # does nothing ;-)
                            skipped = 1
                        # middle of entry
                        else:
                            # replace greek unicode literals if wanted
                            if substitute_unicode == True:
                                sline = replace_greek(sline)
                            entry += "\t" + sline + "\n"

    return entries


# main routine
from argparse import ArgumentParser
from glob import glob
import json
from os import environ

if __name__ == "__main__":

    # setup and parse command line arguments
    parser = ArgumentParser(
        prog="glob2bib",
        description="glob2bib: a bibliography generator for BibTeX and BibLaTeX/Biber",
        epilog="Copyright (c) 2019 Ryan M. L. McFadden",
    )

    # positional arguments
    parser.add_argument(
        "aux_file", help="auxillary file (.aux) from LaTeX compilation", type=str
    )
    parser.add_argument(
        "bib_dir", help="directory to recursively glob for .bib files", type=str
    )

    # optional arguments
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v0.1")
    parser.add_argument(
        "-o",
        "--output",
        help="name of the output file to write the extracted .bib entries to",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--substitute-unicode",
        default=False,
        action="store_true",
        help="substitute unicode greek literals with (escaped) greek math TeX commands",
    )
    parser.add_argument(
        "-b",
        "--biblatex",
        default=False,
        action="store_true",
        help="assume BibLaTeX/Biber as the bibliography management backend",
    )
    parser.add_argument(
        "-l",
        "--long-journal-titles",
        default=False,
        action="store_true",
        help="substitute journal title abbreviations for their full names",
    )

    args = parser.parse_args()

    # extract the (sorted) list of keys from the .aux file
    keys = get_keys(args.aux_file, args.biblatex)

    # get the (sorted) list of .bib files to search within for matching keys
    bibs = glob(args.bib_dir + "/**/*.bib", recursive=True)
    bibs.sort()

    # extract all the bibliography entries from the .bib files whose keys match hose in the .aux file
    entries = get_entires(keys, bibs, args.substitute_unicode)

    # swap the journal titles
    if args.long_journal_titles == True:
        # open the list of names/abbreviations
        with open(environ["HOME"] + "/.journal_names.json", "r") as fh:
            journal_names = json.load(fh)

        # empty list to hold the potentially modified enties
        new_entries = []

        # loop over all extracted .bib entries
        for entry in entries:
            # make a copy of the entry
            new_entry = entry

            # loop over all the abbreviated journal names and do the string substitution
            for name in journal_names["short2long"]:

                # case when the braces are used
                name_braces = "{" + name + "}"
                if name_braces in entry:
                    new_entry = entry.replace(
                        name_braces, "{" + journal_names["short2long"][name] + "}"
                    )

                # case when quotes are used
                name_quotes = '"' + name + '"'
                if name_quotes in entry:
                    new_entry = entry.replace(
                        name_quotes, '"' + journal_names["short2long"][name] + '"'
                    )

            # add the new entry to the list
            new_entries.append(new_entry)

        # replace all the the old entries with the updated ones
        entries = new_entries

    # print the entries to the terminal
    if args.output == None:
        for entry in entries:
            print(entry, end="")
    # write the entries to a file
    else:
        with open(args.output, "w") as fh:
            for entry in entries:
                fh.write(entry)
