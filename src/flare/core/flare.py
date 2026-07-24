from dataclasses import dataclass

from flare.core.api import FlarumAPI


@dataclass
class Page:
    pass


@dataclass
class Dashboard(Page):
    pass


@dataclass
class Discussion(Page):
    pass


class Flare:
    origin: str
    endpoint: str

    api: FlarumAPI

    def __init__(self, origin: str):
        self.origin = origin
        self.endpoint = f"https://{origin}/api"

        self.api = FlarumAPI(self.endpoint)

    def get_dashboard(self) -> Dashboard:
        dashboard = Dashboard()
        dashboard.populate()

        return dashboard

    def get_discussion(self) -> Discussion:
        discussion = Discussion()
        discussion.populate()

        return discussion
