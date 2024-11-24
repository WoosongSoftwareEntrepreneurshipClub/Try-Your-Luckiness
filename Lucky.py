import datetime
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from Ai import genAi
import json

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import re
import markdown2
import send_mail

pdfmetrics.registerFont(TTFont("NotoSansTC", "NotoSansTC-Regular.ttf"))

def set_background(canvas, doc):
    canvas.setFillColor("#c10000")
    canvas.rect(-0.5, -1, 653, 793, fill=1)
    canvas.setFillColor("#fcc325")
    canvas.rect(40, 70, letter[0] - 75, 660, fill=1)


def markdown_to_rich_text(markdown_line, styles):
    """
    Convert Markdown line to HTML-like styled text for Paragraphs.
    """
    # Replace `**text**` with <b>text</b>
    markdown_line = re.sub(r"\*\*(.*?)\*\*", r"\1", markdown_line)
    # Replace `*text*` with <i>text</i>
    markdown_line = re.sub(r"\*(.*?)\*", r"\1", markdown_line)
    return markdown_line

def render_markdown_to_pdf(markdown_content, output_file):
    """
    Render Markdown content to a styled PDF.
    """
    # Convert Markdown to HTML using markdown2
    html_content = markdown2.markdown(markdown_content)
    
    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    doc.onFirstPage = set_background
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(name="newHeader1", fontSize=18, leading=22, spaceAfter=10, textColor="#d4af37"))
    styles.add(ParagraphStyle(name="newHeader2", fontSize=16, leading=20, spaceAfter=8, textColor="#ffd700"))
    styles.add(ParagraphStyle(name="Header3", fontSize=14, leading=18, spaceAfter=6, textColor="#000000", fontName='Helvetica-bold'))
    styles.add(ParagraphStyle(name="Header4", fontSize=12, leading=16, spaceAfter=4, textColor="#000000", fontName='Helvetica-bold'))
    styles.add(ParagraphStyle(name="List", fontSize=12, leftIndent=20, bulletIndent=10, leading=14, fontName="NotoSansTC"))
    styles.add(ParagraphStyle(name="newBodyText", fontSize=12, leading=16, fontName="NotoSansTC"))
    styles.add(ParagraphStyle(name="newBlockquote", fontSize=12, leading=16, textColor="gray", leftIndent=20))
    styles.add(ParagraphStyle(name="newCode", fontName="Courier", fontSize=10, backColor="#f4f4f4", textColor="red"))

    # Parse HTML content into styled paragraphs
    elements = []
    # Split content into lines and process for specific Markdown patterns
    lines = markdown_content.split("\n")
    for line in lines:
        line = markdown_to_rich_text(line, styles)
        if line.startswith("# "):  # H1
            elements.append(Paragraph(line[2:], styles["newHeader1"]))
        elif line.startswith("## "):  # H2
            elements.append(Paragraph(line[3:], styles["newHeader2"]))
        elif line.startswith("### "):  # H3
            elements.append(Paragraph(line[4:].strip(), styles["Header3"]))
        elif line.startswith("#### "):  # H4
            elements.append(Paragraph(line[5:].strip(), styles["Header4"]))  
        elif line.startswith(">"):  # Blockquote
            elements.append(Paragraph(line[2:], styles["newBlockquote"]))
        elif line.startswith("```"):  # Ignore code block markers
            continue
        elif line.startswith("- "):  # Unordered list
            elements.append(Paragraph(f"• {line[2:].strip()}", styles["List"]))
        elif line == "---":  # Horizontal rule
            elements.append(Spacer(1, 6))
            elements.append(HRFlowable(width="100%", color="#000000"))
            elements.append(Spacer(1, 6))
        elif line.startswith("```"):  # Ignore code block markers
            continue
        elif line.strip():  # Normal text
            elements.append(Paragraph(line.strip(), styles["newBodyText"]))
        elements.append(Spacer(1, 12))  # Add spacing between lines
    
    # Build the PDF
    doc.build(elements)
    print(f"PDF successfully saved to {output_file}")

def call_AI():
    email_pattern = re.compile("^((?!\.)[\w\-_.]*[^.])(@\w+)(.\w+(\.\w+)?[^.\W])$")
    name = name_entry.get(); bd = birth_entry.get()
    if len(name) == 0:
        update_fortune_message("Check Your Name", "center")
    else:
        if email_var:
            email = email_entry.get()
            if email_pattern.match(email) == None:
                update_fortune_message("Invalid Email Address", 'center')
                return
        else:
            email = ''
        gemini = genAi()  
        response = gemini.get_response(userName=name, Date=str(datetime.datetime.now().date()), userBirth=bd)
        response = json.loads(response)
        print(response)
        # response = {"date": "2024-11-23", "name": "ASDFADSF", "birth": "2011-04-03", "luckiness": 60, "description": "### Fortune Analysis Result for ASDFADSF\n\n- **Today's Date**: November 23, 2024\n- **Birth Information**: April 3, 2011 (Heavenly Stem: 辛, Earthly Branch: 卯)\n\n#### **Fortune Summary**\n- **Five Elements**: The central element of your birth chart is Metal (金), and today's elements present a moderate balance.\n- **Compatibility Analysis**: Your birth Earthly Branch 卯(Mao) has a neutral interaction with today's Earthly Branch.\n- **Overall Fortune**: Today's energy is relatively stable, suitable for steady progress and thoughtful actions.\n\n---\n\n#### **Fortune Score**\n- **Luckiness Index**: 60/100\n\n---\n\nThis analysis is for reference only and may help you make better decisions."}
        message = f"{response['description']}" + "\n\n\n#### by Software & Entrepreneurship Club\n- Email: softwareentrepreneurshipclub@gmail.com\n- Instagram: software_entrepreneurship_club"
        update_fortune_message(message=message, align='center')
        render_markdown_to_pdf(message, f'./result/{response['name']}.pdf')
        if email_var.get():
            email = email_entry.get()
            send_mail.sendMail(email, message, f'./result/{response['name']}.pdf')
        # clear input labels
        name_entry.delete(0, END)  # Clear the existing content
        email_entry.delete(0, END)  # Clear the existing content

root = Tk()
root.title("Test Your Luckiness!")
root.geometry("1000x800")
root.config(bg="#c10000")


# Title
title_label = Label(root, text="Test Your Luckiness!", font=("Papyrus", 36, "bold"), 
                       fg="#ffd700", bg="#c10000")
title_label.pack(pady=20)

# Input Section
input_frame = Frame(root, bg="#fcc325", bd=5, relief="ridge", borderwidth=0, )
input_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Name Input
name_label = Label(input_frame, text="Your Name:", font=("Arial", 16), bg="#fcc325", fg="black")
name_label.pack(pady=10)
name_entry = Entry(input_frame, font=("Arial", 14), width=30)
name_entry.pack(pady=5)

# Birthday Input
birth_label = Label(input_frame, text="Birthday (YYYY-MM-DD):", font=("Arial", 16), bg="#fcc325", fg="black")
birth_label.pack(pady=10)
birth_entry = DateEntry(input_frame, font=("Arial", 14), width=30, background='white', date_pattern = 'yyyy-mm-dd', maxdate = datetime.date.fromisoformat('2007-12-31'), foreground = 'black', 
                        bordercolor = 'black', headersbackground='white', headersforeground='black', weekendbackground = 'white', weekendforeground = 'black')
birth_entry.pack(pady=5)

# Email Input
email_label = Label(input_frame, text="Your Email (Optional):", font=("Arial", 16), bg="#fcc325", fg="black")
email_label.pack(pady=10)
email_entry = Entry(input_frame, font=("Arial", 14), width=30)
email_entry.pack(pady=5)

# Checkbox for Email Agreement
email_var = BooleanVar()
email_checkbox = Checkbutton(input_frame, text="Agree to receive results via email", variable=email_var,
                                 font=("Arial", 12), bg="#fcc325", fg="black", activebackground="#fcc325")
email_checkbox.pack(pady=10)

# Button
try_button = Button(root, text="Try!", font=("Arial", 18, "bold"), bg="#04cc0a", fg="black", 
                       activebackground="#005b01", activeforeground="white", command=call_AI)
try_button.pack(pady=20)

# Result Section
result_frame = Frame(root, bg="#05057f", bd=5, relief="ridge", border=0)
result_frame.pack(pady=20, padx=20, fill="both", expand=True)

result_scroll = Scrollbar(result_frame, orient='vertical')
result_scroll.pack(side = RIGHT, fill = Y)

result_title = Label(result_frame, text="Your Fortune Result", font=("Arial", 18, "bold"), 
                        fg="#ffd700", bg="#05057f")
result_title.pack(pady=10)

fortune_message = "Click 'Try!' to reveal your luck."

# result_label = Label(result_frame, textvariable=fortune_message, font=("Arial", 16), justify='left',
#                         fg="#ffe4b5", bg="#05057f")
# result_label.pack(pady=20)
result_text = Text(result_frame, font=("Arial", 16), fg="#ffe4b5", bg="#05057f", wrap="word", border=0, yscrollcommand=result_scroll.set)
result_text.pack(pady=10, padx=10, fill="both", expand=True)

result_scroll.config(command=result_text.yview)

def update_fortune_message(message = "Click 'Try!' to reveal your luck.", align = 'center'):
    result_text.delete(1.0, END)  # Clear the existing content
    result_text.insert(END, message)  # Insert the new content
    result_text.tag_configure("align", justify = align)
    result_text.tag_add("align", "1.0", "end")

update_fortune_message()
# Run the application
root.mainloop()