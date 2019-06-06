from string import Template

body_template = Template('''
### Total: ${num_issues} <b>unsolved issues</b> </summary>

${issues_detail}

''')

issue_template_line = Template('''
<details>
<summary>${from_linter}: [${text}](${filename}#L${line}) </summary>

```go
${source_lines}
```
</details>
''')


def generate_comment_body(report):
    issues_detail = ''

    for issue in report['Issues']:
        issue_markdown = issue_template_line.substitute(
            from_linter=issue['FromLinter'],
            text=issue['Text'],
            filename=issue['Pos']['Filename'],
            line=issue['Pos']['Line'],
            source_lines='\r\n'.join(issue['SourceLines']),
        )
        issues_detail += issue_markdown

    return  body_template.substitute(
        num_issues=len(report['Issues']),
        issues_detail=issues_detail
    )
