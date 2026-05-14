# models.py

from sqlalchemy import Column, Integer, String, Float, UniqueConstraint # Column is used to define a column in the database, Integer is used to define an integer column, String is used to define a string column, and Float is used to define a float column
from db import Base # Base is the base class for all the models in the database, it is imported from db.py

# Config table (shift rules)

class Config(Base): # Config is a model that represents the configuration for the payroll system, it inherits from Base
    __tablename__ = "configs" # __tablename__ is used to specify the name of the table in the database, in this case, it is "config"

    id = Column(Integer, primary_key=True, index=True) # id is a column that represents the primary key of the table, it is an integer and it is indexed
    
    employee_type = Column(String, unique=True) # employee_type is a column that represents the type of employee for the payroll system, it is a string, it must be unique, and it cannot be null
    shift_start = Column(String) # shift_start is a column that represents the start time of the shift for the payroll system, it is a string and it cannot be null
    shift_end = Column(String) # shift_end is a column that represents the end time of the shift for the payroll system, it is a string and it cannot be null
    
    
    overtime_rate = Column(Float) # overtime_rate is a column that represents the overtime rate for the payroll system, it is a float and it cannot be null
    late_cut_rate = Column(Float) # late_cut_rate is a column that represents the late cut rate for the payroll system, it is a float and it cannot be null
    # tax_rate = Column(Float, nullable=False) # tax_rate is a column that represents the tax rate for the payroll system, it is a float and it cannot be null
    # deduction_rate = Column(Float, nullable=False) # deduction_rate is a column that represents the deduction rate for the payroll system, it is a float and it cannot be null

# Clock records table
class ClockRecord(Base): # ClockRecord is a model that represents a clock record for an employee, it inherits from Base
    __tablename__ = "clock_records" # __tablename__ is used to specify the name of the table in the database, in this case, it is "clock_records"

    id = Column(Integer, primary_key=True, index=True) # id is a column that represents the primary key of the table, it is an integer and it is indexed
    
    
    employee_id = Column(Integer) # employee_id is a column that represents the ID of the employee for the clock record, it is a string and it cannot be null
    employee_type = Column(String) # employee_type is a column that represents the type of employee for the clock record, it is a string and it cannot be null
    clock_in = Column(String) # clock_in is a column that represents the clock-in time for the clock record, it is a string and it cannot be null
    clock_out = Column(String) # clock_out is a column that represents the clock-out time
    # timestamp = Column(String) # timestamp is a column that represents the timestamp of the clock record, it is a string and it cannot be null
    # type = Column(String) # type is a column that represents the type of clock record (clock-in or clock-out), it is a string and it cannot be null
    
    # Prevent duplicate clock records for the same employee at the same time
    __table_args__ = (UniqueConstraint('employee_id', 'clock_in'),) # __table_args__ is used to specify additional arguments for the table, in this case, it is used to specify a unique constraint on the combination of employee_id and clock_in to prevent duplicate clock records for the same employee at the same time