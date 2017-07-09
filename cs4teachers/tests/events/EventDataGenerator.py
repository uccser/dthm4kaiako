"""Create test data of event models."""

from events.models import (
    Event,
    Location,
    Resource,
)


class EventDataGenerator:
    """Class for generating test data for events."""

    def create_event(self, number, location=None, is_published=True):
        """Create event object.

        Args:
            number: Identifier of the event (int).

        Returns:
            Event object.
        """
        event = Event(
            name="Event {}".format(number),
            description="Description for Event {}".format(number),
            location=location,
            is_published=is_published,
        )
        event.save()
        return event

    def create_location(self, number):
        """Create location object.

        Args:
            number: Identifier of the location (int).

        Returns:
            Location object.
        """
        location = Location(
            name="Location {}".format(number),
            address="Erskine Building, Science Rd, Ilam, Christchurch",
            geolocation="-43.5225594,172.5811949",
            description="Description for Location {}".format(number),
        )
        location.save()
        return location

    def create_resource(self, number):
        """Create resource object.

        Args:
            number: Identifier of the resource (int).

        Returns:
            Resource object.
        """
        resource = Resource(
            name="Resource {}".format(number),
            url="https://www.{}.com/".format(number),
            description="Description for Resource {}".format(number),
        )
        resource.save()
        return resource
