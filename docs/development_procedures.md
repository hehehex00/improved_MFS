# DataToolbox Development Standards and Procedures
The purpose of this document is to provide a framework for development moving forward. Due to the nature of our customer needs, we tend
to ship tools fast and forget about them, leading to unmaintained, undocumented, and sometimes wasted code. As we don't have a large team
to handle both development of new features as well as maintenance, we need to be more intentional with our process, ensuring success
long term. This document is broken down into two main sections: "Defining new work" and "Code Quality and Maintainability", which covers what
we need to do prior to creating new tools, and how to develop the tools in a more maintainable way.

# Defining new work
This section outlines the aspects developers need to consider prior to creating new tools. Doing the work upfront will help identify
prioritization, and keep the tools useful long-term.

-------------------------------------------------------------------------------------------------------------------------------------
## The 3 types of tools
Generally speaking, there are 3 types of tools we make. The types will have different needs and lifespans in the codebase, so it is
important to identify the type of tool before development. Knowing this will help the developers know how they need to maintain it
over the long term.

- General Purpose (ToolBox)
  - All partners can find useful, will have the longest support life (Size & Complexity Small - Large)
- Partner Specialized (ToolBox)
  - A one-off tool for a specific partner that is simple enough to live in the toolbox, but is rarely used after it's initial
    creation (Size & Complexity Small)
- Bespoke (Other)
  - A one-off tool, usually for a specific partner, that has requirements the toolbox cannot accomodate, like integrations with other
    data visualization tools i.e. ElasticSearch and are deployed separately from toolbox. These also live in separate repositories that
    DataToolbox (Size & Complexity Medium to Large)

When considering these 3 types, we'll want to prioritize new work accordingly. This may mean intentionally expanding the scope
of partner-specific tools to have value for other partners.

-------------------------------------------------------------------------------------------------------------------------------------
## Requirements Gathering
When a new tool is discussed, we need to have a standardized way of gathering all the pertinent data prior to writing the first line
of code. Having all of this information will help the team prioritize what needs to be done, undestand the maintenance lifecycle, and
estimate for deprecation in the future.

Developers should give the asking party a form containing these questions, and then the developer will include these in the MVP issue
created for the new tool:

- What type of file is being ingested?
  - How is the data formatted?
  - Will the same file be ingested? If so, how often is the file updated?
- What is the output of this file?
  - Visualizations (Graph, Map, etc.)
  - Lists
  - File (Excel, CSV, PDF, etc.)
  - Text
- Will this tool be applicable to future problem sets? (Is it reusable?)
- How will this tool be deployed? On-toolbox or elsewhere?

After requirements have been gathered, the developer should make a flow chart visually demonstrating the core logic of the tool. This
chart should be verified with the asking party, and included in the tool README and issue ticket so that others can understand the
tool at a glance.

-------------------------------------------------------------------------------------------------------------------------------------
## MVP
MVP stand for Minimum Viable Product. It means the smallest amount of product completed needed for it to be deployed/shipped. In our case, because we need to
move fast, our MVP means that the core functionality requirement is complete. When creating new tool tickets in GitHub we should tag the ticket with "MVP" so that
the developer focuses on core functionality.

- Meets functionality requirements
- Clear of CVEs
- Core logic flow chart on ticket and README

-------------------------------------------------------------------------------------------------------------------------------------
## Definition of Done
The 'Definition of Done' concept goes beyond MVP to include pieces of the implementation that are not important to the end user, but are critical for maintaining
the application going forward.

- Meets code structure requirements
- Unit tests complete
- MR properly reviewed

-------------------------------------------------------------------------------------------------------------------------------------
## Requirements for Deprecation
Applications don't live forever, so we need a process for knowing when to archive them. Our analytics should tell us how often things are being used, we can use
that to decide which tools can be removed from the toolbox.

# Code Quality and Maintainability
This sections outlines how we should structure our code and it's dependencies so that it's easier to understand and maintain.

-------------------------------------------------------------------------------------------------------------------------------------
## Code Structure

### Types
In Python defining types is optional. This is good for small scripts, but is detrimental to your mental overhead as you are trying to understand code you are
reading due to the fact that you cannot know what the underlying type is at first glance. When writing your code, you always need to define the type in the
variable declaration as well as function definitions. This ensures that variables don't mistakenly change types through later manipulation, causing bugs and confusion.
This approach is better than writing comments to describe the data being manipulated.

Example:
~~~python
# Unclear
  # Variable
    data = readDataFromFile(file)
  # Function
    def readDataFromFile(file):
      # ...CODE...
      # return data

# Clear
  # Variable
    data: array = readDataFromFile(file)
  # Function
    def readDataFromFile(file: File) -> array:
      # ...CODE...
      # return data
~~~

### Functions
Functions are a key abstraction to utilize, but it is important to use them correctly. We don't want to over-abstract our code to the point where the core logic is
hidden away.

We want to focus on writing **Pure Functions**, which meet two criteria
1. Given two calls of the function given the same parameters, the output will be identical. Meaning that there is no external influence into the function such as
  mutable global variables, configuration, etc.
2. The function has no side effects. Meaning that it does not mutate existing values, but returns new ones.

[Pure Functions](https://en.wikipedia.org/wiki/Pure_function) are the easiest to apply Unit Tests for, and limits the amount of abstraction you can do.

### Locality of Behavior
Locality of Behavior ([LoB](https://dev.to/ralphcone/new-hot-trend-locality-of-behavior-1g9k)) is an emerging paradigm set out to redefine the concept of *cohesion*
when it applies to programming. LoB states:

*The behaviour of a unit of code should be as obvious as possible by looking only at that unit of code.*

How you can interpret this is by looking at any 10 consecutive lines of code, and being able to understand what is happening at that point in the program.
This concept pairs with the idea of implementing the right amount of abstraction with functions.

If you are writing a large block of code that is processing data from a data structure and you need to take a tangent to retrieve more data from somewhere else,
instead of intermixing that logic with the processing, you abstract that retrieval to another properly-named function. When you do this you can see that
the code is retrieving more data, but you're not stressing your mental capacity with the *how?* while trying to understand the larger logic.

-------------------------------------------------------------------------------------------------------------------------------------
## Internal Library

It's important to maintain a internal library of useful functions that work between multiple tools.

When writing functions for your tool, consider if it could be used elsewhere, and if so place the function in our internal library at
`streamlit-1.0/src/data_toolbox/utils`.

Library functions, because they are used across multiple tools, need 100% Unit Test coverage.

Before writing a new function, consider whether the internal library already supports that functionality, and implement it if so.

-------------------------------------------------------------------------------------------------------------------------------------
## Unit Testing
Unit Testing is key to having fault tolerant code. Having 100% coverage throughout all tools is unnecessary, however covering your backend functions
ensures that your core logic doesn't break.

When writing Unit Tests, you want to create at minimum 2 Tests per function.

- 1 test for each 'success' path
- 1 test for a 'fail' condition

If you write Pure Functions, writing simple Unit Tests is much easier, which will save you a lot of debugging time.

-------------------------------------------------------------------------------------------------------------------------------------
## Choosing & Maintaining Packages
When choosing to implement packages or dependencies into the codebase, consider the following aspects:

- Does the package have sufficient documentation?
- Is the package actively maintained?
- Does the package contain known CVEs in the version you want to use?
- How many different versions there are, and what are the differences between them?
- What type of versioning does it use?

Use all of these factors to determine which package would be best to use long-term.

### Types of Versioning
- Semantic Versioning (SemVer): The most widely used paradigm, follows the X.X.X or Major.Minor.Patch convention.
  - Major: Signifies that all sub-versions underneath this version follow the same API pattern. Changing version numbers within the Major
  *should not* break the functionality.
  - Minor: Signifies improvements to the current Major API implementation regarding performance or stability.
  - Patch: Signifies bug and CVE fixes.
- Sequential Versioning: Similiar to Semantic Versioning, it often looks like 0.X.0. It often ignores the idea of Major/Minor versions.
  It can be difficult to understand when there are breaking changes to the API. This is somewhat common amongst dependencies.
- Date-Based Versioning: Uses the date that version was released. For this type it can be difficult to understand when there are
  breaking changes to the API. Luckily for dependecies, this is rarely encountered.
- Others: Alphanumeric, Odd-Even, and Rational Versioning also exist, but are very rare so it's unlikely you will encounter them.

### Updating Packages
In order to avoid bugs and CVEs from infecting our code, we need to ensure that we are regularly updating our packages so we get the
latest patches. How we do this depends on the versioning type of each package. All of the packages currently in our repo use either
*Semantic Versioning* or *Sequential Versioning*.

- Semantic Versioning: In our requirements.txt files, we want to specify the Major version, and leave the Minor and Patch versions
open to be managed by the Package Manager. This will ensure that everytime the application is built or deployed, we are getting the most
up-to-date version compatible with our code. There is still a small chance that a Minor or Patch version will break something, but in that
case we will investigate that on a case-by-case basis, and lock down the specific version of that package if necessary
- Sequential Versioning: Unlike above, it is impossible to guarantee that continously updating these types of packages will not break
our functionality. For these types of packages we will continue using specific version numbers in the requirements.txt files,
however we need a process for evaluating and updating them periodically or switching to a different package altogether. Catching CVEs
via scanning will also tell us when these need to be updated.

-------------------------------------------------------------------------------------------------------------------------------------
