# AI Usage Policy

This project welcomes the use of AI coding assistants (like Gemini, Copilot, Claude, etc.) to help write code, draft documentation, or refactor. However, to maintain the quality, security, and IP compliance of this project under its Apache 2.0 License, we require contributors to adhere to the following guidelines:

## 1. Transparency
All non-trivial AI-generated or AI-assisted contributions must be disclosed.
When submitting a Pull Request, you must accurately fill out the AI Usage section of the PR template.

## 2. Human Responsibility
You are responsible for every line of code you submit, regardless of whether you wrote it or an AI generated it.
- **You must understand the code:** Do not submit code you cannot explain or maintain.
- **You must review the code:** All AI-generated code must be reviewed by a human for logic, security vulnerabilities, and adherence to project conventions before submission.

## 3. Intellectual Property
Do not prompt AI assistants with proprietary or licensed code that you do not have the rights to use. Ensure that the generated output does not violate third-party copyright or licensing terms.

## 4. How to Mark AI Code
For significant blocks of code or entire files that are primarily AI-generated, we encourage using git commit trailers for tracking:

```text
Ai-Generated: gemini-3.1-pro
Ai-Reviewed: true
Reviewer: <your-name>
```

For inline tracking of substantial AI-generated logic, you may optionally use a comment header:
```python
# @ai-generated: gemini-3.1-pro | YYYY-MM-DD | prompt: "brief description"
# @ai-reviewed: true | reviewer: <your-name>
```
