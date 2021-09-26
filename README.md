# CS555 Course Project

## About

This project will involve analyzing GEDCOM files. [Wikipedia Page on GEDCOM](https://en.wikipedia.org/wiki/GEDCOM).

## Members

* Pridhvi Myneni - B.E. Computer Engineering exp Dec 2021

## Developer Guidelines

* We'll be using Python & MongoDB for this project. Please familiarize yourself with both and install the following, preferably in this order:
  * MongoDB
  * MongoDB Compass (for easy viewing of the database)
  * Python 3.8 (not sure if necessary)
  * Anaconda (for environment/dependency management)
* Clone this repository
* `conda env create -f environment.yml`
  * If a new package is installed (prefer conda over pip):
    * `conda env export > environment.yml`
    * `conda deactivate`
    * `conda env remove -n CS555`
    * `conda env create -f environment.yml`
  * `conda activate CS555`
    * You will need to run this every time you open a new terminal
  * `conda develop gedutil`
* `pre-commit install`
  * You will have to run this every time you clone the repo somewhere new

## Commit Guidelines

We will be using commit messages of the following format:

```text
[TYPE] Header line

- Body bullet
- More body [oh look](https://example.com) - A link!
- Another bullet

You can also just write paragraphs...
```

For convenience, I won't be enforcing commit message guidelines using precommit scripts, but please follow carefully.

Types:

* [BUILD] - a build commit
* [BUG] - a bugfix
* [MERGE] - a merge commit. You can also just use the standard commit message that's autogenerated during merges
* [REFACTOR] - a commit for refactoring code.
* [MISC] - any commit that doesn't fall under the existing guidelines. Shouldn't be used often.

Please use commits as intended (just one change/commit). If you find yourself building something, fixing a bug, and refactoring all in one commit, stop and commit each change separately.
