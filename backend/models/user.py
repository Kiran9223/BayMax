class User(UserBase):
    id: int
    is_active: bool
    preferences: Optional[UserPreferences] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        