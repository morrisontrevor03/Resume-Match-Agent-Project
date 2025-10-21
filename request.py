from openai import OpenAI 
import os
from dotenv import load_dotenv
import readpdf
from pydantic import BaseModel, Field

load_dotenv() 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

#define output schema
class ResponseModel(BaseModel):
    score: str = Field(..., description="The overall score from 0-100 of the match between resume and posting")
    differences: list[str] = Field(..., description="Fill a list of differences between the job description and the resume")

#get inputs
resume = readpdf.text_redacted
posting = """
About Trellis AI
Trellis helps healthcare providers treat more patients, faster—while eliminating pre-service paperwork.

We automate document intake, prior authorizations, and appeals at scale to streamline operations and accelerate care.

Our AI agent is trained on millions of clinical data points and converts messy, unstructured documents into clean, structured data directly in your EHR.

With Trellis, leading healthcare providers and pharmaceutical companies were able to:

Reduce time to treatment by over 90%

Improve prior authorization approval and reimbursement rates

Leverage structured data to enhance drug program performance and clinical decision-making

Administrative costs account for over 20% of U.S. healthcare spending—delaying care, draining revenue, and driving staff burnout while having less visibility into patient care than ever before. We built Trellis to tackle this head on.

About the role
Trellis helps healthcare providers treat more patients faster—while eliminating pre-service paperwork.
We do this by automating document intake, prior authorizations, and appeals at scale to streamline operations and accelerate care.

Trellis is a spinout from Stanford AI lab and is backed by leading investors including YC, General Catalyst, Telesoft partners, and executives at Google and Salesforce.

The Role
Forward Deployed Engineers (FDEs) at Trellis work directly with healthcare providers, pharmaceutical companies, and diagnostic labs to understand their most pressing operational challenges and implement AI-powered solutions that transform patient care. Our customers trust Trellis for mission-critical healthcare operations, and projects often start with complex questions like "How do we reduce prior authorization denial rates while accelerating patient access to life-saving treatments?" or "How can we streamline our drug program enrollment process to get patients the medications they need faster?"

🧍🏻‍♂️Why work with us
Be at the forefront of what's possible in AI and Healthcare data.
Work on the most important problem of our time—with direct, measurable impact.
You will work closely with the F500 customers and the founding team. You will get to wear multiple hats from sales and marketing to recruiting.
Extreme ownership: you will own key part of Trellis business operations and have the opportunities to start new initiatives.
Be a part of a world-class team (e.g., team members have previously won the international physics olympiad, published economics research, were a founding engineer at Unicorn Startup, and taught AI classes to hundreds of Stanford graduate students).
To apply, please complete this take home and email the Github link with your code to founders[at]runtrellis.com. We will only be looking at completed take homes emailed to the address, so please make sure all requirements are met before submitting.
Requirements
Core Responsibilities: As an FDE, your role combines the technical depth of a senior engineer with the strategic thinking of a healthcare consultant. You'll work in small, autonomous teams with direct access to leadership and own end-to-end delivery of high-impact projects. Your day might include:
Technical Implementation: Architecting and building custom AI workflows, integrating with EHR systems, and developing healthcare-specific data pipelines
Customer Collaboration: Working directly with clinical teams, operations managers, and C-suite executives to understand workflows and optimize outcomes
Data Engineering: Processing and structuring complex healthcare data, from clinical notes to insurance guidelines to lab results
Product Development: Building custom interfaces and tools that seamlessly integrate into existing healthcare workflows
Strategic Planning: Establishing implementation roadmaps and success metrics for large-scale healthcare transformation projects
"""

#define prompt

prompt = f"Match the resume with the job posting provided. Return only using the JSON format provided. Make sure to use the match_score in a reasonable manner. Resume: {resume} Posting: {posting}"

response = client.responses.parse(
    model="gpt-4.1",
    input=prompt,
    text_format=ResponseModel
) 

obj: ResponseModel = response.output_parsed

print("score:", obj.score)
print("Differences", obj.differences)