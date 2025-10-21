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
posting = ["posting"]

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