# Standard imports

# Third party imports
import sys

from argonaut.config.config import (
    PROJECT_JSON_PATH,
    PROJECT_TRACKER_JSON_PATH,
    PROJECT_TRACKER_REPO_NAME,
    PROJECT_TRACKER_REPO_OWNER,
)
from argonaut.document_types.supported_document_types import (
    get_document_type_from_abbreviation,
)
from argonaut.gui.dialog import get_folder_input, show_info
from argonaut.misc.git import git_clone
from argonaut.project_management.project_management import update_all_projects
from argonaut.tracker.document_tracker import DocumentTracker
from argonaut.tracker.project_tracker import ProjectTracker
import wx

# Local imports
from argonaut.creator.project_creator import ProjectCreator
from argonaut.creator.document_creator import DocumentCreator
from argonaut.logger.logger import create_default_logger


class MainFrame(wx.Frame):
    def __init__(self, gh_user: str):
        super().__init__(
            parent=None, title="MØWUT Project Management", size=wx.Size(600, 800)
        )

        self.logger = create_default_logger(__name__)

        panel = wx.Panel(self)

        # Vertical layout
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create buttons
        self.button1 = wx.Button(panel, label="Create new project")
        self.button2 = wx.Button(panel, label="Create new document")
        self.button3 = wx.Button(panel, label="Update all projects")
        self.button4 = wx.Button(panel, label="Button 4")
        self.button5 = wx.Button(panel, label="Button 5")
        self.button6 = wx.Button(panel, label="Exit")

        # Bind callbacks
        self.button1.Bind(wx.EVT_BUTTON, self.create_new_project)
        self.button2.Bind(wx.EVT_BUTTON, self.create_new_document)
        self.button3.Bind(wx.EVT_BUTTON, self.on_button3_click)
        self.button4.Bind(wx.EVT_BUTTON, self.on_button4_click)
        self.button5.Bind(wx.EVT_BUTTON, self.on_button5_click)
        self.button6.Bind(wx.EVT_BUTTON, self.exit)

        sizer.Add(wx.StaticText(panel, label=f"Detected Github user: {gh_user}"))

        # Add buttons to layout
        for button in [
            self.button1,
            self.button2,
            self.button3,
            self.button4,
            self.button5,
            self.button6,
        ]:
            sizer.Add(button, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(sizer)

    # Placeholder callback functions

    def create_new_project(self, event):
        self.logger.info("Requested new project creation")
        with ProjectCreator(self) as x:
            x.run()

    def create_new_document(self, event):
        self.logger.info("Requested new document creation")
        with DocumentCreator(self) as x:
            x.run()

    def on_button3_click(self, event):
        update_all_projects()

    def on_button4_click(self, event):
        self.logger.info("Button 4 clicked")
        # TODO: Add Button 4 logic here

    def on_button5_click(self, event):
        self.logger.info("Button 5 clicked")
        # TODO: Add Button 5 logic here

    def exit(self, event):
        self.logger.info("Requested exit")
        sys.exit(0)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame("TEST")
    frame.Show()
    app.MainLoop()
