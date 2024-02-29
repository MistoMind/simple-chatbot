from sqlalchemy.orm import Session

from models.user import UserModel
from schemas.user import UserCreateSchema


class CRUDUser:
    def create(self, db: Session, user: UserCreateSchema):
        db_user = UserModel(**user.model_dump())

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def filter(self, *criterion, db: Session):
        return db.query(UserModel).filter(*criterion)

    def get_by_id(self, db: Session, id: int):
        return db.query(UserModel).filter(UserModel.id == id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(UserModel).filter(UserModel.email == email).first()


user_crud = CRUDUser()
