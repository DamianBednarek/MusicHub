import factory

from src.tracks.models import Track


class TrackFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Track

    id = factory.Faker("uuid4")
    filename = factory.Faker("file_name", category="audio")
    file = "/tracks/test.mp3"
    track_length = factory.Faker("random_int")
    created_by = "user@example.com"
    is_public = factory.Faker("boolean")
