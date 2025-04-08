from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import re
from io import BytesIO
from docx import Document
from fastapi import FastAPI, HTTPException
#from enum import Enum
from src.helpers_practice.utils import process_input
import os
from typing import Union, Optional

class ErrorResponse(BaseModel):
    message: str

app = FastAPI(title="Email Writing and Question Generation API")


# Define the input data model with mandatory fields
class InputData(BaseModel):
    user_id: int = Field(..., description="User ID should be a positive integer.")
    session_id: str = Field(..., description="Session ID must not be empty.")
    level: str = Field(..., description="Level must be one of a1, a2, b1, b2, c1, c2.")
    scenario: str = Field(..., description="Scenario must not be empty.")
    question_id: int = Field(..., description="Question ID must be an integer between 0 and 5.")
    user_response: str = Field(..., description="User response must not be empty.")


    @validator('user_id')
    def validate_user_id(cls, value):
        # Check if the user_id is an integer
        if not isinstance(value, int):
            raise ValueError("user_id must be an integer.")
        
        # Check if the user_id is exactly 7 digits
        if len(str(value)) != 7:
            raise ValueError("user_id should have exactly 7 digits.")
        return value

    # Custom validator for session_id
    @validator('session_id')
    def check_session_id(cls, v):
        if not v.strip():
            raise ValueError('session_id must not be empty.')
        return v
    
     # Custom validator for level
    @validator('level')
    def check_level(cls, v):
        allowed_levels = {'a1', 'a2', 'b1', 'b2', 'c1', 'c2'}
        if v.lower() not in allowed_levels:
            raise ValueError(f"level must be one of {', '.join(allowed_levels)}. You provided: {v}")
        return v.lower()

    # Custom validator for scenario
    @validator('scenario')
    def check_scenario(cls, v):
        if not v.strip():
            raise ValueError('scenario must not be empty.')
        return v

    # Custom validator for question_id
    @validator('question_id')
    def check_question_id(cls, v):
        if not (0 <= v <= 5):
            raise ValueError('question_id must be between 0 and 5.')
        return v

    # Custom validator for user_response
    @validator('user_response')
    def check_user_response(cls, v):
        if not v.strip():
            raise ValueError('user_response must not be empty.')
        return v    
    

# Define the endpoint
@app.post("/v1/bot/")
async def process(data: InputData):
    try:
        result = process_input(
            user_id=data.user_id,
            session_id=data.session_id,
            level=data.level,
            scenario=data.scenario,
            question_id=data.question_id,
            user_response=data.user_response  # This can be None if not provided
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
