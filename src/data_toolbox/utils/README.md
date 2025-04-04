# src/utils

## What

A collection of reusable NON-Streamlit utilities. This is different than code
in src/components which focus on not repeating Streamlit components
If a feature is used by two or more tools, it's recommended to abstract
the code here.

## Why

To reduce code duplication.

## HOW to Add Utilities to src/utils

1. Do due diligence that the utility you wish to add has not already been
    written in one of the functions
1. Follow example pseudocode for adding functions/methods if available
1. Coordinate with Data Team if you want to add a new utility .py file
1. Write the utility to be flexible e.g. a word translator tool that can handle
    a variety of object types and not one tool per type

## External Packages

There are packages are not available on all networks. \
These packages are stored here:

### skopeutils

- [package registry](https://gitlab.wildfireworkspace.com/groups/datascience/-/packages/125)

### pycellex

- [Repository](https://gitlab.wildfireworkspace.com/datascience/pycellex/-/tree/2.2.6?ref_type=tags)
- [package registry](https://gitlab.wildfireworkspace.com/groups/datascience/-/packages/177)

### installing external packages with pip

[datascience/python-packages](https://gitlab.wildfireworkspace.com/datascience/python-packages)
