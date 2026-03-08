# Python Docstring Conventions

This reference covers the most popular Python docstring styles: **PEP 257**, **Google**, and **NumPy**.

## PEP 257 (Standard Python)

PEP 257 is the official Python docstring convention. It's simple and widely supported.

### One-liner Docstrings

```python
def function(arg1: str, arg2: int) -> bool:
    """Do something with the arguments and return a boolean."""
    pass
```

**Rules:**
- Fits on a single line
- Ends with a period
- Describes what the function does (imperative form)
- Can be used as a doctest

### Multi-line Docstrings

```python
def complex_function(arg1: str, arg2: int) -> dict:
    """Brief description of the function in one line.

    More detailed description of what the function does,
    including any important behavior or side effects.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of the return value
    """
    pass
```

**Structure:**
1. Summary line (one sentence, ends with period)
2. Blank line
3. More detailed description
4. Blank line (optional)
5. Args, Returns, Raises sections (optional)

### Class Docstrings

```python
class MyClass:
    """Brief description of the class.

    More detailed description including attributes,
    constructor behavior, and usage examples.

    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """

    def __init__(self, arg1: str):
        """Initialize MyClass.

        Args:
            arg1: Description of arg1
        """
        pass
```

---

## Google Style

Google's style is more readable and popular in modern Python projects.

### Function Docstring

```python
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from a remote API endpoint.

    Connects to the specified URL and retrieves data,
    returning it as a parsed dictionary.

    Args:
        url (str): The URL to fetch from
        timeout (int): Request timeout in seconds. Defaults to 30.

    Returns:
        dict: Parsed JSON response from the server

    Raises:
        requests.ConnectionError: If connection fails
        ValueError: If response is not valid JSON

    Example:
        >>> data = fetch_data("https://api.example.com/users")
        >>> print(data['users'])
    """
    pass
```

### Class Docstring

```python
class DataFetcher:
    """Handles data fetching from various sources.

    This class manages connections to remote APIs and handles
    retries, caching, and error recovery. Configure behavior
    through the constructor.

    Attributes:
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum retry attempts
        cache (dict): In-memory cache for responses

    Example:
        >>> fetcher = DataFetcher(timeout=60)
        >>> data = fetcher.fetch("https://api.example.com")
    """

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize the DataFetcher.

        Args:
            timeout (int): Request timeout in seconds. Defaults to 30.
            max_retries (int): Maximum retry attempts. Defaults to 3.
        """
        pass
```

### Sections Reference

- **Args**: List of function parameters
- **Returns**: Description of return value
- **Raises**: Exceptions that can be raised
- **Yields**: What generator yields
- **Examples**: Usage examples with code
- **Note**: Important information
- **Warning**: Warnings about usage
- **Attributes**: Class attributes (for classes)
- **See Also**: Related functions or classes

---

## NumPy Style

NumPy style is detailed and popular in scientific Python (NumPy, SciPy, pandas).

### Function Docstring

```python
def calculate_statistics(data, method='mean'):
    """Calculate statistics for numerical data.

    Compute various statistical measures for the input data
    using the specified calculation method.

    Parameters
    ----------
    data : array_like
        Input data array to process
    method : {'mean', 'median', 'std'}, optional
        Statistical method to use. Default is 'mean'.

    Returns
    -------
    result : ndarray
        Calculated statistics for each column
    metadata : dict
        Information about the calculation

    Raises
    ------
    ValueError
        If data is empty or method is invalid
    TypeError
        If data cannot be converted to numeric

    Examples
    --------
    >>> data = [1, 2, 3, 4, 5]
    >>> result, meta = calculate_statistics(data)
    >>> print(result)
    """
    pass
```

### Class Docstring

```python
class DataProcessor:
    """Process and transform data for analysis.

    Provides methods for cleaning, normalizing, and
    transforming data into formats suitable for
    statistical analysis.

    Parameters
    ----------
    normalize : bool, optional
        Whether to normalize data to [0, 1]. Default is False.
    remove_nulls : bool, optional
        Whether to remove null values. Default is True.

    Attributes
    ----------
    data : ndarray
        Current dataset being processed
    is_normalized : bool
        Whether data is currently normalized
    """

    def __init__(self, normalize=False, remove_nulls=True):
        """Initialize DataProcessor."""
        pass
```

### Sections Reference

- **Parameters**: Function parameters (instead of Args)
- **Returns**: Return value(s)
- **Yields**: For generators
- **Raises**: Exceptions that can be raised
- **Examples**: Usage examples with code
- **Notes**: Additional notes
- **References**: Academic references
- **Attributes**: Class attributes
- **See Also**: Related functions

---

## Type Hints in Docstrings

When using type hints, you can simplify docstring type annotations:

### With Type Hints (Modern)

```python
def process(data: list[str], max_size: int = 100) -> dict[str, int]:
    """Process a list of strings and return counts.

    Args:
        data: List of strings to process
        max_size: Maximum size limit

    Returns:
        Dictionary mapping strings to occurrence counts
    """
    pass
```

### Without Type Hints (Legacy)

```python
def process(data, max_size=100):
    """Process a list of strings and return counts.

    Args:
        data (list[str]): List of strings to process
        max_size (int): Maximum size limit. Defaults to 100.

    Returns:
        dict[str, int]: Dictionary mapping strings to occurrence counts
    """
    pass
```

---

## Best Practices

### ✓ DO

- Write in imperative mood: "Return the value" not "Returns the value"
- Include type information
- Document exceptions that can be raised
- Provide examples for complex functions
- Keep first line under 79 characters
- Use consistent style throughout your project

### ✗ DON'T

- Leave docstrings empty or with just ellipsis (`...`)
- Document obvious parameters
- Repeat information from type hints
- Write complete sentences for parameter descriptions (unless necessary)
- Use `__author__` or `__date__` (use git history instead)

---

## Choosing a Style

| Style | Best For | Pros | Cons |
|-------|----------|------|------|
| **PEP 257** | Standard libraries, simple projects | Simple, official standard | Less detail-oriented |
| **Google** | Modern Python projects, teams | Readable, popular, clear | Slightly verbose |
| **NumPy** | Scientific computing, data science | Comprehensive, detailed | More verbose |

**Recommendation:** Use Google style for most projects. Use NumPy for scientific/data projects. Use PEP 257 for standard library compatibility.
