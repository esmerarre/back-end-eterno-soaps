from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    category_id: int
    ingredients: list[str]

    class Config:
        from_attributes = True
