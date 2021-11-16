# Contributing to the final project

If you are implementing a user story, please follow the following steps.

## Environment

The repo is designed to be run in a portable environment managed through Anaconda. If you followed the steps in the readme, you should be able to simply run `conda activate CS555` to initialize the environment. See the readme for what to do in the event the `environment.yml` file has been changed since you last worked on this project.

## Implementation

1. Check out the most recent version of main

  - `git checkout main`
  - `git pull`

2. Create a new branch to contain your changes

  - `git checkout -b USXX` (replacing `XX` with the story number)

3. Create a new file to contain your check

  - `touch gedutil/gedutil/checks/usXX.py` (replacing `XX` with the story number)

4. Implement your check. If you need a reference, look at any of the other 10+ implemented stories in the same directory
5. Create a new file to contain your automated test cases

  - `touch tests/test_usXX.py`

6. Implement your automated test cases. Ensure that you test all edge cases. Ensure that you also have at least one test case that is expected to pass, and one test case that is expected to fail. Again, if you need a reference, take a look at the other 10+ tests in the same directory.
7. Add your test input files under `tests/input_files/USXX` (replacing `XX` with the story number)
8. To make your code importable, edit `gedutil/gedutil/__init__.py` and add an import statement that matches with the other 10+ import statements that also import user stories.
9. To ensure your code is run when the main file is run, also modify `gedutil/gedutil/all_checks.py` to

  1. Import your user story
  2. Add it to the list of classes that are being run in the for loop

## Testing

At this stage, I highly recommend committing and pushing your changes up to git to ensure your work is saved somewhere.

1. Ensure your code passes the pre-commit checks (either by committing or running `pre-commit run`). This will not only run the formatter, which will make reading your code easier, but also run a static analysis tool (`mypy`), which is typically very good at catching syntax errors that might be missed if they occur in an obscure edge case.
2. Run `pytest`
3. Read the output of `pytest`. If there is any red (or if the process finishes with a nonzero exit code), you know that your code failed. Pytest will also give you the output in the event of a failure, so keep an eye out for debugging purposes. You can also run single pytest test cases, if you simply look up pytest documentation. Even if your code passes tests, look at the output of pytest. There is a coverage table, which indicates if/where your tests do not cover all edge cases. If your newly implemented user story is not at 100% coverage, modify your code until it meets 100% coverage. Although coverage is not something that is required, or graded, having 100% coverage will reduce the risk of having bugs in your code.

## Pushing to Git

If you completed all of the above successfully, then your code should pass checks just fine. The automated tests simply (1) ensure that the formatter and static analysis ran and (2) your code passes pytest. If you completed all of the steps in testing and setup your repo & developer environment per the readme, this shouldn't be a concern.
