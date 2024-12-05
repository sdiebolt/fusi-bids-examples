|version| |python|

.. |version| image:: https://img.shields.io/badge/version-0.0.9-orange.svg
    :target: https://github.com/sdiebolt/fus-bids-examples
    :alt: fUS-BIDS draft version

.. |python| image:: https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12-blue.svg
    :target: https://www.python.org/
    :alt: Python

fUS-BIDS examples
=================

This repository contains a set of synthetic example datasets to illustrate the
`fUSI-BIDS draft specification
<https://docs.google.com/document/d/1W3z01mf1E8cfg_OY7ZGqeUeOKv659jCHQBXavtmT-T8/edit?usp=sharing)>`_. 

Synthetic datasets generation
-----------------------------

The ``create_synthetic_2dt_dataset.py`` script generates a synthetic 2D+t dataset
following version v0.0.9 of the draft specification. The dataset consists of 10 mice,
each with two sessions: ``vehicle`` and ``treatment``. Each session contains a single
angiography scan (``angio`` datatype), and 6 functional scans (``fus`` datatype, 3
task-free and 3 task-based).

