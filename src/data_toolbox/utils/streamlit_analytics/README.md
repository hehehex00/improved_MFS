# Streamlit Analytics

This is a modification of the Streamlit Analytics package.\
The original package is not compatible with Streamlit `1.30.0` and later.\
The last update to the package was in 2022.\
This modification will act as our version of the package until we implement a
better solution or until the package is updated.

## Before

```python
    query_params = st.experimental_get_query_params()
```

## After

```python
    query_params = st.query_params
```

## References

- <https://pypi.org/project/streamlit-analytics/>
- <https://github.com/jrieke/streamlit-analytics/pull/44>
