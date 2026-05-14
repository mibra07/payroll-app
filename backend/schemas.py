# schemas.py

from pydantic import BaseModel # BaseModel is used to define the schema for the API, it is imported from pydantic

class SummaryResponse(BaseModel): # SummaryResponse is a schema that represents the response for the summary endpoint, it inherits from BaseModel
    employee_id: int # employee_id is a field that represents the ID of the employee for the summary response, it is an integer
    late_hours: float # late_hours is a field that represents the total late hours for the summary response, it is a float
    overtime_hours: float # overtime_hours is a field that represents the total overtime hours for the summary response, it is a float
    total_late_cut: float # total_late_cut is a field that represents the total late cut for the summary response, it is a float
    total_overtime_pay: float # total_overtime_pay is a field that represents the total
    # employee_type: str # employee_type is a field that represents the type of employee for the summary response, it is a string
    # total_hours: float # total_hours is a field that represents the total hours worked for the summary response, it is a float
    # total_pay: float # total_pay is a field that represents the total pay for the summary response, it is a float

