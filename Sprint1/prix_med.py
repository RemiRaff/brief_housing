class Prix_Median(Base):
    __tablename__ = "prix_median"

    id_prix_median = Column(Integer, primary_key=True)

    ocean_proximity = Column(String(30))
    latitude = Column(Float)
    longitude = Column(Float)
    housing_median_age = Column(Float)
    total_rooms = Column(Float)
    total_bedrooms = Column(Float)
    population = Column(Float)
    households = Column(SmallInteger)
    median_income = Column(Float)
    median_house_value = Column(Integer)

    def __init__(
        self,
        ocean_proximity,
        latitude,
        longitude,
        housing_median_age,
        total_rooms,
        total_bedrooms,
        population,
        households,
        median_income,
        median_house_value,
    ):
        self.ocean_proximity = ocean_proximity
        self.latitude = latitude
        self.longitude = longitude
        self.housing_median_age = housing_median_age
        self.total_rooms = total_rooms
        self.total_bedrooms = total_bedrooms
        self.population = population
        self.households = households
        self.median_income = median_income
        self.median_house_value = median_house_value
