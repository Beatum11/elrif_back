from __future__ import annotations
import uuid



class TalentDomain:
    def __init__(self,id: uuid.UUID,
                 profile_id: uuid.UUID,
                  bio: str, 
                 role: str, 
                 portfolio_link: str,
                 project_price: float = 0,
                 rating: int = 50):
        
        self.id = id
        self.profile_id = profile_id
        self.bio = bio
        self.role = role
        self.portfolio_link = portfolio_link
        self.project_price = project_price
        self.rating = rating

    @staticmethod
    def create(profile_id: uuid.UUID,
                bio: str, 
                role: str, 
                portfolio_link: str,
                project_price: float = 0,
                rating: int = 50):
        
        id = uuid.uuid4()
        return TalentDomain(
            id=id,
            profile_id=profile_id,
            bio=bio,
            role=role,
            portfolio_link=portfolio_link,
            project_price=project_price,
            rating=rating
        )

    def update_bio(self, bio: str):
        if not bio:
            raise ValueError("bio can't be empty")
        self.bio = bio

    def update_role(self, role: str):
        if not role:
            raise ValueError("role can't be empty")
        self.role = role

    def update_portfolio_link(self, portfolio_link: str):
        self.portfolio_link = portfolio_link

    def update_project_price(self, project_price: float):
        if project_price <= 0:
            raise ValueError("Price must be more than 0")
        self.project_price = project_price

    def update_rating(self, new_rating: int):
        if new_rating < 0:
            raise ValueError("rating can't be less than 0")
        self.rating = new_rating
