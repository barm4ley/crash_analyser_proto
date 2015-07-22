#!/usr/bin/env python

import cran

if __name__ == "__main__":
    cran.start_cran_operation(host="0.0.0.0", port=5000, debug=True)
