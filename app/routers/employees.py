# app/routers/employees.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models import Employee
from app.database import get_session
from app.schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, session: Session = Depends(get_session)):
    db_employee = Employee(**employee.dict())
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee

@router.get("/", response_model=list[EmployeeResponse])
def list_employees(session: Session = Depends(get_session)):
    employees = session.exec(select(Employee)).all()
    return employees
