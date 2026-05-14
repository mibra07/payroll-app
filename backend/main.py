# main.py

from fileinput import filename

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException # FastAPI is used to create the API, UploadFile and File are used to handle file uploads, Depends is used for dependency injection, and HTTPException is used to handle exceptions in the API
from sqlalchemy.orm import Session # Session is used to create a session for interacting with the database, it is imported from sqlalchemy.orm
from sqlalchemy import text # text is used to execute raw SQL queries, it is imported from sqlalchemy

from db import Base, engine, get_db # Base is the base class for all the models in the database, engine is the connection to the database, and get_db is a function that creates a new session for interacting with the database, all of these are imported from db.py
import models # models is the module that contains the models for the database, it is imported from models.py

#from sqlalchemy.dialects.sqlite import insert # insert is used to perform an upsert operation in SQLite, it is imported from sqlalchemy.dialects.sqlite
#from datetime import datetime # datetime is used to handle date and time operations, it is imported from the standard library


from fastapi.middleware.cors import CORSMiddleware



from services.csv_parser import parse_csv # parse_csv is a function that takes a file as input and returns a list of dictionaries representing the rows in the CSV file, it is imported from services/csv_parser.py
from services.aggregation import BASE_QUERY # BASE_QUERY is a string that contains the base SQL query for aggregation, it is imported from services/aggregation.py

from fastapi.responses import StreamingResponse # StreamingResponse is used to return a streaming response, it is imported from fastapi.responses
import csv # csv is used to read and write CSV files, it is imported from the standard library
from io import StringIO # StringIO is used to create an in-memory file-like object, it is imported from the standard library

Base.metadata.create_all(bind=engine) # create_all is used to create the tables in the database based on the models defined in the Base class, it is called on the metadata of the Base class and it is passed the engine to specify the database connection
app = FastAPI() # app is the FastAPI application instance

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- API Endpoints ---------


# -----------------------------------
# Health check endpoint
# ------------------------------------

@app.get("/health") # @app.get is a decorator that defines a GET endpoint at the specified path, in this case, it is "/health"
async def health_check(): # health_check is an asynchronous function that handles the health check endpoint, it returns a JSON response indicating that the API is healthy
    return {"status": "healthy"} # return a JSON response with a status key set to "healthy"

# -----------------------------------
# Upload configs (UPSERT)
# -----------------------------------

@app.post("/configs") # @app.post is a decorator that defines a POST endpoint at the specified path, in this case, it is "/upload-configs"
async def upload_configs(file: UploadFile, db: Session = Depends(get_db)): # upload_configs is an asynchronous function that handles the upload of configuration files, it takes a file as input and a database session as a dependency
    print("File received", file.filename)
    try:
        reader = await parse_csv(file) # parse the CSV file using the parse_csv function, it returns a list of dictionaries representing the rows in the CSV file
        inserted, updated = 0, 0 # initialize counters for inserted and updated configs
        
        inserted, updated = 0, 0 # initialize counters for inserted and updated configs
        for row in reader: # iterate over each row in the parsed CSV data
            existing = db.query(models.Config).filter_by(employee_type=row['employee_type']).first() # query the database to check if a config with the same employee_type already exists
            if existing: # if an existing config is found
                existing.shift_start = row['shift_start'] # update the shift_start value of the existing config
                existing.shift_end = row['shift_end'] # update the shift_end value of the existing config
                existing.overtime_rate = row['overtime_rate'] # update the overtime_rate value of the existing config
                existing.late_cut_rate = row['late_cut_rate'] # update the late_cut_rate value of the existing config
                updated += 1 # increment the updated counter
            else: # if no existing config is found
                config = models.Config(
                    employee_type=row['employee_type'],
                    shift_start=row['shift_start'],
                    shift_end=row['shift_end'],
                    overtime_rate=row['overtime_rate'],
                    late_cut_rate=row['late_cut_rate']
                )
                db.add(config) # add the new config to the database session
                inserted += 1 # increment the inserted counter
            print("ROW:", row)        
        db.commit() # commit the transaction to save the changes to the database
        return {"inserted": inserted, "updated": updated} # return a JSON response with the counts of inserted and updated configs
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

# -----------------------------------
# Upload clock records (INSERT)
# -----------------------------------

@app.post("/clock-records") # @app.post is a decorator that defines a POST endpoint at the specified path, in this case, it is "/clock-records"   

async def upload_clock_records(file: UploadFile, db: Session = Depends(get_db)):
    try:
        reader = await parse_csv(file)

        inserted, skipped = 0, 0

        for row in reader:

            existing = db.query(models.ClockRecord).filter(
                models.ClockRecord.employee_id == int(row['employee_id']),
                models.ClockRecord.clock_in == row['clock_in']
            ).first()

            if existing:
                skipped += 1
                print("SKIPPED ROW:", row)
                continue

            clock_record = models.ClockRecord(
                employee_id=int(row['employee_id']),
                employee_type=row['employee_type'],
                clock_in= row['clock_in'],
                clock_out=row['clock_out']
            )

            db.add(clock_record)
            db.commit()  # ⚠️ needed inside loop
            inserted += 1
            print("INSERTED ROW:", row)

        return {"inserted": inserted, "skipped": skipped}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))    
    

# -----------------------------------
# Get summary report with pagination    
# -----------------------------------

@app.get("/summary")
def get_summary(
    limit: int = 50, # limit is a query parameter that specifies the number of records to return, it is an integer and it has a default value of 50
    offset: int = 0, # offset is a query parameter that specifies the number of records to skip, it is an integer and it has a default value of 0
    employee_type: str | None = None, # employee_type is a query parameter that specifies the type of employee to filter the summary report, it is a string and it is optional
    sort: str = "employee_id", # sort is a query parameter that specifies the field to sort the summary report by, it is a string and it has a default value of "employee_id"
    order: str = "asc", # order is a query parameter that specifies the order to sort the summary report, it is a string and it has a default value of "asc"
    db: Session = Depends(get_db) # db is a dependency that provides a database session for interacting with the database, it is created using the get_db function and it is passed as an argument to the endpoint function
):
    # validate query parameters
    if limit > 500 or limit < 1: 
        raise HTTPException(400, "invalid limit")

    if sort not in ["employee_id", "overtime_hours", "late_hours"]:
        raise HTTPException(400, "invalid sort")

    if order not in ["asc", "desc"]:
        raise HTTPException(400, "invalid order")

    # build query with optional employee_type filter
    query = BASE_QUERY

    # apply employee_type filter if provided
    if employee_type:
        query += " WHERE cr.employee_type = :employee_type"

    # apply sorting and pagination
    query += f"""
    GROUP BY cr.employee_id
    ORDER BY {sort} {order}
    LIMIT :limit OFFSET :offset
    """

    # execute query and fetch results
    rows = db.execute(text(query), {
        "limit": limit,
        "offset": offset,
        "employee_type": employee_type
    }).fetchall()

    # total count of distinct employee_id for pagination
    total = db.execute(text("""
        SELECT COUNT(DISTINCT employee_id)
        FROM clock_records
    """)).scalar() # execute a raw SQL query to count the total number of distinct employee_id values in the clock_records table, it returns a scalar value representing the total count
    
    # calculate next_offset for pagination, if the next offset exceeds the total count, set it to None
    next_offset = offset + limit if offset + limit < total else None

    return {
        "items": [dict(row._mapping) for row in rows], # convert each row in the result set to a dictionary using row._mapping and return a list of these dictionaries as the items in the response
        "limit": limit,
        "offset": offset,
        "total": total,
        "next_offset": next_offset # include the limit, offset, total count, and next_offset in the response for pagination purposes
    }

# -----------------------------------
# Single employee summary report
# -----------------------------------

@app.get("/summary/{employee_id}")
def get_employee_summary(employee_id: int, db: Session = Depends(get_db)):
    query = BASE_QUERY + " WHERE cr.employee_id = :employee_id GROUP BY cr.employee_id" # build a SQL query by appending a WHERE clause to the BASE_QUERY to filter the results for a specific employee_id, and group the results by employee_id
    row = db.execute(text(query), {"employee_id": employee_id}).fetchone() # execute the query with the provided employee_id as a parameter and fetch a single row from the result set, it returns a Row object representing the summary for the specified employee_id
    if not row:
        raise HTTPException(404, "employee not found")
    return dict(row._mapping) # convert the Row object to a dictionary using row._mapping and return it as the response for the single employee summary report endpoint

# -----------------------------------
# Export summary report as CSV (Streaming)
# -----------------------------------

@app.get("/summary.csv")
def export_summary_csv(
    employee_type: str | None = None,
    sort: str = "employee_id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    # generator function to stream CSV data in batches
    def generate_csv():
        buffer = StringIO()
        writer = csv.writer(buffer, lineterminator="\n")

        # HEADER
        writer.writerow([
            "employee_id",
            "late_hours",
            "overtime_hours",
            "total_late_cut",
            "total_overtime_pay"
        ])
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

        # STEP 1 → Build query
        query = BASE_QUERY

        if employee_type:
            query += " WHERE cr.employee_type = :employee_type"

        query += f"""
        GROUP BY cr.employee_id
        ORDER BY {sort} {order}
        """

        # STEP 2 → Execute query
        rows = db.execute(text(query), {
            "employee_type": employee_type
        }).fetchall()

        # STEP 3 → Stream rows
        for row in rows:
            writer.writerow([
                row._mapping["employee_id"],
                row._mapping["late_hours"],
                row._mapping["overtime_hours"],
                row._mapping["total_late_cut"],
                row._mapping["total_overtime_pay"]
            ])

            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=summary.csv"}
    )