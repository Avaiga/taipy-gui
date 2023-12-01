"""
This Python file contains two routines that enable the use of comments in Taipy pages using Markdown codes. It supports two types of comments:
 A- Line-ending comment (/#): Should be used at the end of a line or on a standalone line. Everything after /# will be removed.
 B- Inserted comment (/* ... */): Can be used within the code. Only the text within /* ... */ will be removed.

Example usage in Taipy pages definition:

Original Page with Comments:
---------------------------
page_login = '''
/* Page starts here and two new lines will be include:*/ \n\n
/# This line will be removed and this 3 new lines not has efect: \n\n\n 
/# ''Username or Email'' message in various languages:
<|{msg1[Idioma_sel.id/* idiom number from 0 to 7*/]}|text|raw|>
\n /# This new line will be usede because '\n' is place berore of '/#'
/* These lines of code was disabled for  purpose of testing 
/#This Markdown get  the user name:
<|{UserName}|input|> \n 
/#This Markdown get  the Password:
<|{PassWord}|input|> \n
 */
 \n
'''

Processed Page without Comments:
--------------------------------

page_login = '''
\n
<|{msg1[Idioma_sel.id]}|text|raw|>\n
\n
\n
'''
Note: Removing comments results in cleaner code but may reduce understandability regarding 
message variables and function names.

Design by Dr. Policarpo Yoshin Ulianov
Powered by ChatGPT 4 
Please remove the text above and put it in Taipy docs  if this improvment was aproved
"""
# Beginning of _comment.py

import re

def remove_comment(string):
    """
    Remove comments from Markdown strings.
    - /* ... */: Removes multiline comments.
    - /#: Removes everything after /# till the end of the line. 
    If a line starts with /#, the whole line is removed.
    """
    string = re.sub(r'/\*.*?\*/', '', string, flags=re.DOTALL)
    
    lines = string.split('\n')
    cleaned_lines = [line.split('/#')[0] if '/#' in line else line for line in lines if not line.strip().startswith('/#')]
    return '\n'.join(cleaned_lines)

def remove_comment_from_pages(pages_dict):
    """
    Apply remove_comment to each page in a dictionary of pages.
    This function is typically called before rendering the pages in Taipy, ensuring that comments by do not appear in the final output.
    """
    return {key: remove_comment(value) for key, value in pages_dict.items()}

