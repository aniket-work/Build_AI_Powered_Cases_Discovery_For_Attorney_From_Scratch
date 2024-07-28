from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Directory to save the PDFs
output_dir = "database"
os.makedirs(output_dir, exist_ok=True)

# Sample legal case content
cases = [
    {
        "title": "Case 1: Smith vs. Johnson",
        "content": [
            "Paragraph 1: In this case, the plaintiff, Mr. Smith, alleges that the defendant, Mr. Johnson, breached a contract by failing to deliver goods on time.",
            "Paragraph 2: The contract stipulated a delivery date of June 1, 2023, but the goods were not delivered until July 15, 2023. This delay caused significant financial losses for Mr. Smith.",
            "Paragraph 3: Mr. Smith is seeking damages to cover the losses incurred due to the delayed delivery."
        ]
    },
    {
        "title": "Case 2: Brown vs. Davis",
        "content": [
            "Paragraph 1: Ms. Brown claims that Mr. Davis was negligent in maintaining his property, leading to her injury when she slipped and fell on an icy sidewalk.",
            "Paragraph 2: The incident occurred on January 10, 2024, during a heavy snowstorm. Ms. Brown sustained a broken ankle and is seeking compensation for medical expenses and lost wages.",
            "Paragraph 3: Mr. Davis argues that he took reasonable steps to clear the sidewalk and that the weather conditions were beyond his control."
        ]
    },
    {
        "title": "Case 3: Lee vs. Parker",
        "content": [
            "Paragraph 1: Mr. Lee is suing Ms. Parker for defamation, claiming that she made false statements about him that damaged his reputation.",
            "Paragraph 2: The statements were made in a series of social media posts between March and April 2024. Mr. Lee alleges that these posts caused him to lose clients and suffer emotional distress.",
            "Paragraph 3: Ms. Parker contends that her statements were true and protected by free speech."
        ]
    },
    {
        "title": "Case 4: Gonzalez vs. Thompson",
        "content": [
            "Paragraph 1: Mr. Gonzalez alleges that Mr. Thompson failed to fulfill a service agreement for landscaping work.",
            "Paragraph 2: The agreement specified that the work would be completed by September 1, 2023. However, Mr. Thompson did not complete the work, causing Mr. Gonzalez to seek another service provider.",
            "Paragraph 3: Mr. Gonzalez is seeking reimbursement for the additional costs incurred and compensation for the inconvenience."
        ]
    },
    {
        "title": "Case 5: Patel vs. Green",
        "content": [
            "Paragraph 1: Ms. Patel is suing Mr. Green for damages after a car accident she claims was caused by his reckless driving.",
            "Paragraph 2: The accident occurred on July 20, 2024, resulting in significant damage to Ms. Patel's vehicle and personal injuries.",
            "Paragraph 3: Mr. Green denies the allegations, stating that Ms. Patel was at fault for not observing traffic signals."
        ]
    },
    {
        "title": "Case 6: Wilson vs. Robinson",
        "content": [
            "Paragraph 1: Mr. Wilson is seeking damages from Mr. Robinson for breach of a rental agreement.",
            "Paragraph 2: Mr. Robinson allegedly vacated the rental property without providing the required notice, leaving Mr. Wilson with unpaid rent and repair costs.",
            "Paragraph 3: Mr. Robinson argues that the property was uninhabitable and that he had no choice but to leave."
        ]
    },
    {
        "title": "Case 7: Nguyen vs. Carter",
        "content": [
            "Paragraph 1: Dr. Nguyen is suing Mr. Carter for malpractice, alleging that a procedure performed by Mr. Carter caused her significant harm.",
            "Paragraph 2: The procedure took place on February 15, 2024, and Dr. Nguyen claims that it resulted in long-term health issues.",
            "Paragraph 3: Mr. Carter contends that the procedure was conducted according to standard medical practices and that the complications were unforeseeable."
        ]
    },
    {
        "title": "Case 8: Martinez vs. White",
        "content": [
            "Paragraph 1: Mr. Martinez claims that Ms. White breached a business contract by failing to deliver goods as agreed.",
            "Paragraph 2: The contract was for the delivery of electronic components by December 1, 2023. The components were not delivered, causing Mr. Martinez to lose a significant business opportunity.",
            "Paragraph 3: Ms. White argues that the delay was due to supply chain issues beyond her control."
        ]
    },
    {
        "title": "Case 9: Kim vs. Harris",
        "content": [
            "Paragraph 1: Ms. Kim is suing Mr. Harris for invasion of privacy, alleging that he installed surveillance cameras in her home without her consent.",
            "Paragraph 2: The cameras were discovered on March 5, 2024, and Ms. Kim claims they caused her significant distress.",
            "Paragraph 3: Mr. Harris contends that the cameras were installed for security purposes and that Ms. Kim was aware of their presence."
        ]
    },
    {
        "title": "Case 10: Allen vs. Edwards",
        "content": [
            "Paragraph 1: Mr. Allen is suing Ms. Edwards for breach of an employment contract, alleging wrongful termination.",
            "Paragraph 2: Mr. Allen claims he was terminated without cause on May 1, 2024, resulting in financial and emotional distress.",
            "Paragraph 3: Ms. Edwards argues that Mr. Allen was terminated for cause due to repeated violations of company policy."
        ]
    },
]

# Generate PDFs
for i, case in enumerate(cases, start=1):
    pdf_file = os.path.join(output_dir, f"legal_case_{i}.pdf")
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, case["title"])

    # Content
    c.setFont("Helvetica", 12)
    text = c.beginText(72, height - 108)
    for paragraph in case["content"]:
        text.textLine(paragraph)
        text.textLine("")  # Add a blank line between paragraphs

    c.drawText(text)
    c.showPage()
    c.save()

print(f"Generated {len(cases)} PDF files in '{output_dir}' directory.")
