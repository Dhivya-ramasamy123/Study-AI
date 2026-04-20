from typing import List
from pydantic import BaseModel, Field, validator


class MCQQuestion(BaseModel):
    question : str=Field(description="The question text")
    options: List[str]=Field(description="A list of 4 options")
    correct_answer: str=Field(description="The correct answer from the options")

    @validator('question',pre=True)
    def clean_questions(cls,v):
        if isinstance(v,dict):
            return v.get('description',str(v))
        return str(v)
    


class FillBlankQuestion(BaseModel):
    question:str=Field(description="The question text with '___' for the bank" )
    answer : str=Field(description="The correct word or phrase to fill in the blank")

    @validator('question',pre=True)
    def clean_questions(cls,v):
        if isinstance(v,dict):
            return v.get('description',str(v))
        return str(v)