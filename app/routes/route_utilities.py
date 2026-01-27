from fastapi import HTTPException, status
from sqlalchemy import select

## NOT COMPLETE ##


def validate_model(session, cls, model_id):
    try:
        model_id = int(model_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")

    query = select(cls).where(cls.id == model_id)
    model = session.execute(query).scalars().first()

    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__} {model_id} not found")
    return model
