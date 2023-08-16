# A Context-Enhanced LLM to Fix API Documentation Smells

## Documentation Smell
Documentation smells can be described as bad documentation styles that do not necessarily make a documentation incorrect but make it difficult to understand and use. We presented 5 types of documentation smells. They are:
* Bloated: too lengthy and verbose.
* Excess Structural Info: too many structural syntax or information
* Tangled: too complex to read and understand
* Fragmented: scattered over multiple pages or sections
* Lazy: does not provide extra info other than the method prototype


## Survey on Fixing Documentation Smells
We conducted a survey of 30 software practitioners to understand the feasibility and impact of fixing different documentation smells. The survey questionnaire and responses can be found in the 'survey' folder.


## Pipeline for Fixing Lazy Documentation
We proposed an LLM-based two-stage pipeline for fixing lazy documentation, involving additional textual documentation generation and documentation-specific code example generation. The code and data of our approach can be found in the code' and 'data' folders, respectively. 
