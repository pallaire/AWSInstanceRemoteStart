import sched

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static, Label

from vpn import *


class PalVPNApp(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        self.vpn = VPN()

        yield Header()

        self.label = Label("q", id="vpnstatus")
        yield self.label

        self.buttonStart = Button("Start", id="start", disabled=True)
        yield self.buttonStart

        self.buttonStop = Button("Stop", id="stop", disabled=True)
        yield self.buttonStop

        yield Footer()

        self.set_interval(10.0, self.on_interval)
        self.on_interval()

    def on_interval(self) -> None:
        status = self.vpn.state()

        self.label.update(f"VPN Instance is: {status}")
        self.label.remove_class("statusstopped")
        self.label.remove_class("statusrunning")
        self.label.remove_class("statuswaiting")

        if status == "stopped":
            self.label.add_class("statusstopped")
            self.buttonStart.disabled = False
            self.buttonStop.disabled = True
        elif status == "running":
            self.label.add_class("statusrunning")
            self.buttonStart.disabled = True
            self.buttonStop.disabled = False
        else:
            self.label.add_class("statuswaiting")
            self.buttonStart.disabled = True
            self.buttonStop.disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.vpn.start()
            self.on_interval()
        elif event.button.id == "stop":
            self.vpn.stop()
            self.on_interval()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PalVPNApp()
    app.run()

