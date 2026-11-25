# Security policy

## Supported versions

Security fixes are released for the latest minor version on PyPI.

## Reporting a vulnerability

Please **don't open a public issue**. Report it privately through GitHub's [private vulnerability reporting](https://github.com/karawash-projects/pyramz/security/advisories/new). You'll get an acknowledgement within a few days, and a fix or mitigation plan once the report has been assessed.

Pyramz generates SVG markup that is often inserted directly into HTML, so issues are most likely around **markup injection**. One example would be an option value that escapes its attribute. All option values and titles are escaped, and reports of a way around that are especially welcome.
