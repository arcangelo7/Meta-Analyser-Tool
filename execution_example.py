# -*- coding: utf-8 -*-
# Copyright (c) 2019, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

# import the class 'MetaAnalyserTool' from the local file 'mat.py'
from mat import MetaAnalyserTool

# create a new object of the class 'MetaAnalyserTool' specifying the input CSV files to process
my_mat = MetaAnalyserTool("metadata_sample.csv")

# my_mat.<method> ...


# A function to measure the time of other functions
import time


def measure_runtime(func):
    start = time.time()
    func()
    end = time.time()
    print(end - start)


# Example of use
measure_runtime(lambda: my_mat.get_by_id("orcid:0000-0003-0387-921X", None))