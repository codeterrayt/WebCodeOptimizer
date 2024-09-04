**WebCodeOptimizer**
==================

**WebCodeOptimizer** is a tool designed to optimize web code by compressing HTML, CSS, and JavaScript files and removing unused images from your project. The optimization process ensures that your code remains error-free and bug-free while improving performance by reducing file sizes and eliminating unnecessary resources.



## Features

- **HTML, CSS, and JavaScript Optimization**: Compresses your web files to reduce their size without affecting functionality.
- **Image Management**: Automatically detects and removes images that are not used in your project.
- **Error-Free Optimization**: Ensures that the optimization process does not introduce any errors or bugs into your project.

## Installation Guide

Follow these steps to install and set up the WebCodeOptimizer:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/codeterrayt/WebCodeOptimizer.git
cd WebCodeOptimizer
```


**Installation Guide**
------------------------
To install WebCodeOptimizer, follow these steps:

1. Create a virtual environment (venv) for your project.
```bash
python -m venv venv
```
3. Activate the venv.
```bash
venv\Scripts\activate
```
 
5. Install the required modules using `requirements.txt`.
```bash
pip install -r requirements.txt
```

**Usage**
---------

### Creating an Instance

Create an instance of the `ProjectOptimizer` class, passing two paths as arguments:
```python
proj = ProjectOptimizer(r"./code/", r"./optimized/")
```
The first path is for the main code, and the second path is where to create the optimized code folder.

### Optimizing the Code

1. Clone the project folder:
```python
proj.CreateClone()
```
2. Find all HTML, CSS, JS, and image files in the project:
```python
proj.FindAllHTML()
proj.FindAllJS()
proj.FindAllCSS()
proj.FindImagesInProjectHTML()
```
3. Remove unused images:
```python
proj.RemoveUnUsedImages()
```
4. Compress HTML, CSS, and JS files:
```python
proj.CompressHTML()
proj.CompressJS()
proj.CompressCSS()
```

**Methods**
------------

### `CreateClone()`

Clones the project folder.

### `FindAllHTML()`, `FindAllJS()`, `FindAllCSS()`,

Finds all HTML, CSS, and JS files in the project.

### `FindImagesInProjectHTML()`

Finds images referenced in HTML files in the project.

### `RemoveUnUsedImages()`

Removes unused images from the project.

### `CompressHTML()`, `CompressJS()`, `CompressCSS()`

Compresses HTML, CSS, and JS files using various optimization techniques.

## Contributing to WebCodeOptimizer

We welcome contributions to the WebCodeOptimizer project! Whether you're fixing bugs, adding new features, improving documentation, or helping out in any other way, your input is greatly appreciated.

**License**
---------

WebCodeOptimizer is licensed under the MIT License. See [LICENSE](LICENSE) for details.
