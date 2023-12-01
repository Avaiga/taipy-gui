"""
This initial text  must be removed and placed in the Taipy documentetion:

This Python file contain two rotines that allow the use of comentes in Taipy peges
that using Markdown codes. 
For HTML codes the comments are made using /*    */ delimiters, for Markdown
we define the same but incliding the use of a like python comment given by /# delimiter

Two types of comments are allowed inside of the string that define the page Markdown code::
	 A- Line-ending comment: /# XXXX  =>  Need be used in the end of the line or in a complete line.
	                                                                    All words before /# will be removed  
	 B- Comment inserted: /* XXXX  */    =>  Can be used inside the code. 
	                                                                    Only the text  /* XXXX  */   will be removed

Example of the new use comments in Taipe pages definition:

page_login ='''''' 
/* The Taipy page begining  here,  to get 3 new lines use \n to do this:*/  \n\n\n
/# In the line below the msg1[1] contain "Username or Email"
/#presented in 8 idions:   

/# "Username or Email" message,  in 8 idions:
<|{msg1[Idioma_sel.id /*number of selected idiom =1 to 8 */]}|text|raw|>\n

/#This Markdown get  the user name
<|{UserName}|input|> \n 

/# "Inform Password" message, in 8 idions:
<|{msg2[Idioma_sel.id]/* Password */}|text|raw|>:\n

/#This Markdown get  the Password:
<|{PassWord}|input|> \n 
/# We need a way to hide the letters
/# when the user enters this value!

/#This Markdown creat a Login button: 
<|msg3[Idioma_sel.id+1]/*button caption: "Login" in 8 idions */}|button|active|
on_action=confirma_login /* python rotine that react to the button press action*/|>\n
/# We need define a rotine in python to use this UserName and PassWord values:
/# def  confirma_login(state):
/#      print("nome User=",state.UserName ); 
/#      print("senha=",state.PassWord ); 

/* The Taipy page finish here, with this  3'', the use of new line is optional */ \n 
''''''

The same page with  Markdown code, affer the comments be removed:

page_login ='''''' 
\n\n\n

<|{msg1[Idioma_sel.id]}|text|raw|>\n

<|{UserName}|input|> \n 

<|{msg2[Idioma_sel.id]}|text|raw|>:\n

<|{PassWord}|input|> \n 

<|msg3[Idioma_sel.id+1]}|
button|active|on_action=confirma_login|>\n

''''''
Observation: Whitout comment is a more clean code, but hard to undstand 
this msg1 to msg3 meaning, and the Idioma_sel use,  and that 
confirma_login is a pythoc rotine name...
"""

#Here is the real  beginning of _comment.py

import re

#The function remove_commen allows User to do comments in Markdown codes in order to 
#facilitate understanding and documentation of what was developed.
#Everything after /# until the end of the line will be removed.
#Only the part that falls within the delimiters (/* */) will be removed.

def remove_comment(string):
    # Remove /* ... */ comments
    string = re.sub(r'/\*.*?\*/', '', string)
    # Remove entire lines starting with /#
    lines = string.split('\n')
    cleaned_lines = [line for line in lines if not line.strip().startswith('/#')]
    return '\n'.join(cleaned_lines)

# this funcition remove the commente of a pages_dict like:
#  pages = {
#     "/": pg_root,
#     "home": pg_home,
#     "login": pg_login,     
#     "about": pg_about
#     }
#
# The pages are get one by one and apply remove_comment function
# When user call Gui(page=page).run() the fist sptep inside
# Gui.run is do  page = remove_comment_from_pages(page)
# so for the Taipy code interpreter It's as if none of these comments existed. 

def remove_comment_from_pages(pages_dict):
    #print("remov comments")
    for key, value in pages_dict.items():
        pages_dict[key] = remove_comment(value)
    return pages_dict

