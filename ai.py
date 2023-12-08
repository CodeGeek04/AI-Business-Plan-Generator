import openai

def get_completion(prompt, model="gpt-3.5-turbo-16k"):

    messages = [ {"role": "system", 
                      "content": prompt,
                }]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.4,
        )
    except Exception as e:
        print("ERROR: ", e)
        return "ERROR"

    return response.choices[0].message["content"]

class Plan:
    title = "Business Plan"
    content = "This is a business plan"
    author = "AI"


class AI:
    def __init__(self, temperature=0.7):
        self.model = "gpt-3.5-turbo"
        self.temperature = temperature
        openai.api_key = "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"

    def generate_business_plan(self, prompt):
        # Generate a business plan based on the prompt
        plan_title = "Business Plan"
        plan_author = "AI"
        ai_prompt = f"Generate a business plan for a {prompt} startup. Be very concise and quick and dont include any unnecessary information."
        ai_content = get_completion(ai_prompt)

        if ai_content == "ERROR":
            plan = Plan()
            plan.title = plan_title
            plan.content = "We are receiving unusually high traffic. Please try again in a few minutes."
            plan.author = plan_author
            return plan

        plan = Plan()
        plan.title = plan_title
        plan.content = ai_content
        plan.author = plan_author

        return plan

    def review_plan(self, review_prompt):
        # Review the generated plan and provide feedback
        review_comment = get_completion(review_prompt)
        if review_comment == "ERROR":
            return "NO REVIEWS"
        return review_comment

    def edit_plan(self, edit_prompt):
        # Make edits to the plan based on the review comment
        edited_plan = get_completion(edit_prompt)
        if edited_plan == "ERROR":
            return "NO EDITS"
        return edited_plan

    def approve_plan(self, approve_prompt):
        # Approve the final business plan
        approval_comment = get_completion(approve_prompt)
        if approval_comment == "ERROR":
            return "I APPROVE THIS PLAN"
        return approval_comment
