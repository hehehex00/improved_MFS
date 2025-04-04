# Contributing

First off, thanks for taking the time to contribute! 💛\
All types of contributions are encouraged and valued.\
We look forward to seeing what you create!. 🎉

You should also be familiar with the [DataToolbox Team Development Procedures](development_procedures.md)

## Table of Contents

- **[I Have a Question](#i-have-a-question)**
- **[Gitlab Workflow](#gitlab-workflow)**
- **[Standards for Tools](#standards-for-tools)**
- **[New Tools](#new-tools)**
- **[Limitations](#limitations)**

## I Have a Question

> If you haven't read the available [documentation](../README.md) start there first.

Before you ask a question, it is best to search for existing
[Issues](https://gitlab.wildfireworkspace.com/eop/streamlit-1.0/-/issues)
that might help you. In case you have found a suitable issue and still need
clarification, you can write your question in this issue or reach to the Data
Team leadership.

## GitLab Workflow

This project is managed from within GitLab. We also have a slack channel you can
join.

1. Claim an Issue

    In Gitlab we use the term "issue" to refer to a task (new feature, bug fix etc)
    - Review the Gitlab issue board for the project.
    [Project Issues](https://gitlab.wildfireworkspace.com/eop/streamlit-1.0/-/issues)
    - Assign an issue to yourself to get started.

1. Create a new branch for the issue

    The branch name should begin with the issue number (e.g. 30-name-of-branch).
    This will link the issue, branch and future MR together.
    The branch can be created manually or by using the create branch option from
    within the issue.

1. Get setup locally

    Review the documentation to build the application on your local computer

1. Write code

    Be sure to write code focused on meeting the requirements from the Gitlab issue.

    _If there are new features / bug fixes you would like to implement that are
    not currently tracked as issues, reach out to Data Team leadership so they
    can create an issue for the recommended bug fix or feature._

1. Open a MR (Merge Request)

- Push the changes up to your remote branch in Gitlab.
- Open a Merge Request for your feature branch.
- Data Team will review the MR and may request changes to the submitted code
    (e.g. to fix a bug or refactor code for quality).
- Once Data Team approves the MR your job is complete! 🎉

## Standards for Tools

Delivering functional usable tools that meet a user need is a key element to the
success of the Data Team.

### Minimal Standards (MVP)

These are the minimum standards for new tools:

- Tool is based on the tool template.
- Tool meets an articulable user need\
    _An exception may be made for tools labeled "experimental."_
- Tool has been tested and is stable.

### Ideal Standard

To go beyond a minimally viable product (MVP), review and implement the following:

#### User Experience

**Error Handling:** Print useful human readable error messages to the screen.
This is particularly important for aspects of the code that handle user input.

_Example: User presses "Search" without typing in any keywords in the search box.
Instead of printing ```index out of range...[stacktrace]```
print ```Please enter keywords into the search box.```_

Reference the [Laws of UX](https://lawsofux.com) for more ideas/inspiration.

#### Code Quality

**Start with following Python's Official style guide:**
**[PEP 8](https://peps.python.org/pep-0008).** This will cover most code quality
advice. It includes coding conventions and formatting guidelines.

**Linting.** Before opening a merge request please ensure you have run the
appropriate linter to evaluate quality and style. Your linting score doesn't
need to be perfect but please conform to the advice given in most cases.

For Python code use [ruff](https://docs.astral.sh/ruff/). It can
be added as a Visual Studio Code extension or run from the command line.

```cmd
py -m pip install ruff
ruff .\src
```

When changing documentation such as the README or CONTRIBUTING, please ensure
you are using markdownlint, which can also be added to Visual Studio Code.

**Testing.** Every tool developed should be tested in some way. Ideally with a
combination of manual user tests and an included unit test suite. You can find
existing test data on the share drive: ```Y:\P-Groups\D01\14_Toolbox_Test_Data```

1. Install `pytest` (e.g. `pip install pytest`)
1. From the streamlit-1.0/src directory run `python -m pytest.` This will
    cause pytest to collect all the tests in the project in run them while properly
    importing the required dependencies.

**D.R.Y. Your Code!** D.R.Y. (Don't Repeat Yourself) Code
shared by multiple tools is abstracted to the components folder. Code reused
multiple times within the code is abstracted to a function or method.

**Ten thousand lines of code in one file is too much.** Break down your code into
funtions or classes that perform specific tasks. This promotes code reuse,
readability, and maintainability. Some developers try to keep their files <= 100
lines of code.

**One hundred parameters in one function is too much.** Consider refactoring
code if you start to have functions/methods with > 6 parameters. An excessive
amount of parameters makes code hard to understand, often unnecessarily.

**Use meaningful variable, function, and class names.** Prefer descriptive names.
Avoid names like "var_1."

**Document your code.** Add comments to your code that explain what's going on or
why you chose a certain method of doing something if the reason is not obvious.
This is particularly important with complex portions of the code. Include
references to stack overflow where appropriate. Don't forget the docstrings,
they are also important!

### Philosophical Standards

**Minimalism.** Keep the tool simple and focused on solving specific issues.
Avoid unnecessary features and complexities that might confuse or overwhelm
users.

**Flexibility.** Design the tool to handle different data formats, structures,
and sizes.

**Accessibility.** Make the tool accessible to users with _varying_ levels of
technical expertise. Provide clear documentation and intuitive interfaces to
help users understand and effectively use the tool.

**Efficiency.** Strive for efficient data parsing algorithms and code
implementation to minimize processing time and resource usage, enabling users to
parse large datasets quickly and accurately.

_Technical example: When using
`pandas`, prefer `itertuples` over `iterrows` because `iterrows`
touches every cell which is very slow._

## New Tools

New tools can easily be added to the template.

> **Important:**
> Before adding a new tool, please review
[Archived Tools](https://gitlab.wildfireworkspace.com/eop/datatoolboxarchive) to see a list deprecated tools
and why they were removed.

1. Copy the Tool Template `src/admin_tools/tool_template`\
    _This is what you will use as the starting point for your tool._
2. Paste the template into one of the directories inside of `src` and rename it.
3. Add an entry to the `tools` dictionary found in `src/tool_dictionary.py`
    it should look like this:

    ```python
        "Your Tool": Tool_Metadata(
            'Your Tool',
            your_tool,
            accepted_file_types=[],
            image_path="./images/your_tool_logo.png", # optional
            uses=["Phone Numbers", "Addresses", "Social Media"],
            category=tool_categories['data_manipulation'],
            featured=False,
        ),
    ```

    _This adds it to the navigation bar and the home page._
4. If your tool is going to be hosted in a separate container your entry should
    have an additional argument in it `port` and use the standard function
    `redirect_to_tool` instead of `your_tool`:

    ```python
        "Your Tool": Tool_Metadata(
            'Your Tool',
            redirect_to_tool,
            accepted_file_types=[],
            image_path="./images/your_tool_logo.png", # optional
            uses=["Phone Numbers", "Addresses", "Social Media"],
            category=tool_categories['data_manipulation'],
            featured=False,
            port=1234,
        ),
     ```

    _This allows navigation between containers._
5. If you tool is hosted in separate container, add your container to
    the `docker-compose.yml` in the root of the project. Your container should
    declare its `port` and be named after your tool:

    ```yml
        your_tool:
            container_name: your_tool
            build:
            args:
                TOOL_NAME: your_tool
            context: .
            dockerfile: src/data_toolbox/your_tool/Dockerfile
            ports:
            - "portnum:portnum"
            volumes:
            - feedback-data:/datatoolbox/feedback_data
            - datatoolbox-log:/var/log/datatoolbox
    ```

6. If you want your tool to be tracked using analytics and you are
    using a separate docker container, you will need to import
    some utility components and the analytics integration. You'll
    also need to define your main streamlit app using the
    following pattern:

    ```python
        import components as toolbox_components
        from data_toolbox import analytics_integration

        ...

        def your_main_function():
            """Streamlit main function."""
            # Navigation Sidebar for containerized apps
            toolbox_components.home_button()

        ...

        if __name__ == "__main__":
            analytics_context = analytics_integration.get_analytics_context()
            with analytics_context:
                your_main_function()
    ```

    _This enables analytics and surfaces the button for inter-container navigation._
7. Once you finish building the tool you are done!

## Limitations

For applications that will be deployed onto our internet facing network, there
are no limitations on what Python packages you can import.
For applications that will be deployed to other networks, the packages are
limited to the python standard library and approved packages.
