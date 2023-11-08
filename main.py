import typer
from ai import AI
from role import Role
from permissions import Permissions
from fpdf import FPDF
from flask import Flask, request, send_from_directory
import os
from flask_cors import CORS

def main(prompt = "tech"):
    # Initialize the AI and databases
    ai = AI()
    # Generate a business plan
    plan_prompt = f"Generate a business plan for a {prompt} startup"
    print("Generating Plan")
    plan = ai.generate_business_plan(plan_prompt)
    plan_content = plan.content
    print("Base Plan: ", plan_content)

    # Review the plan
    review_prompt = f"Review the business plan for a {prompt} startup having the following content:\n\n{plan_content}\n\nProvide constructive feedback to improve the plan."
    print("Under Review by QA ")
    review_qa = ai.review_plan(review_prompt + "\n\nYou are the QA.")
    print("Review QA: ", review_qa)

    # Edit the plan
    edit_prompt = f"Edit the business plan for a {prompt} startup having the following content:\n\n{plan_content}\n\nReview Comments:\n\nQA: {review_qa}\n\nRevise the plan to address the feedback."
    print("Under Edit by CTO ")
    edit_cto = ai.edit_plan(edit_prompt)
    print("EDIT CTO: ", edit_cto)


    # Approve the plan
    approve_prompt = f"Approve the business plan for a {prompt} startup having the following content:\n\n{plan_content}\n\nReview Comments:\n\nQA: {review_qa}\n\nEdits:\n\nCTO: {edit_cto}\n\nIf you are satisfied with the plan, provide your final approval."
    print("Under Approval by CEO ")
    approval_ceo = ai.approve_plan(approve_prompt)
    print("APPROVAL CEO: ", approval_ceo)

    
    pdf = FPDF()
    
    # Add a page for the base plan
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Base Plan: ", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = plan_content)
    
    # Add a page for the QA review
    pdf.add_page()
    pdf.cell(200, 10, txt = "Review by QA: ", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = review_qa)
    
    # Add a page for the CTO edit
    pdf.add_page()
    pdf.cell(200, 10, txt = "Edit by CTO: ", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = edit_cto)
    
    # Add a page for the CEO approval
    pdf.add_page()
    pdf.cell(200, 10, txt = "Approval by CEO: ", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = approval_ceo)
    
    # Save the pdf with name .pdf
    pdf.output("plan_document.pdf")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate-plan', methods=['POST', 'OPTIONS'])
def generate_plan():
    if request.method == 'OPTIONS':
        # Preflight request; respond with 200 OK and the necessary headers.
        response = app.make_default_options_response()
    else:
        # Handle POST request.
        prompt = request.json['prompt']
        prompt_string = '\n'.join(f"{key}: {value}" for key, value in prompt.items())
        print("Prompt: ", prompt_string)
        main(prompt_string)
        response = send_from_directory(os.getcwd(), 'plan_document.pdf', as_attachment=True)
    
    return response

port = int(os.environ.get("PORT", 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
