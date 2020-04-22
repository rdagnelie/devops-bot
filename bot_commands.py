from validator_collection import checkers
from chat_functions import send_text_to_room
import compute
import network


class Command(object):
    def __init__(self, client, store, config, command, room, event):
        """A command made by a user

        Args:
            client (nio.AsyncClient): The client to communicate to matrix with

            store (Storage): Bot storage

            config (Config): Bot configuration parameters

            command (str): The command and arguments

            room (nio.rooms.MatrixRoom): The room the command was sent in

            event (nio.events.room_events.RoomMessageText): The event describing the command
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

    async def process(self):
        """Process the command"""
        if self.command.startswith("ping"):
            await self._network_ping()
        elif self.command.startswith("reach"):
            await self._network_reach()
        elif self.command.startswith(("mbox", "mailbox")):
            await self._network_mailbox()
        elif self.command.startswith(("bjm", "bonjourmadame")):
            await self._network_bonjourmadame()
        elif self.command.startswith(("uh", "uhash", "user_hash", "userhash")):
            await self._compute_uhash()
        elif self.command.startswith(("mh", "mhash", "mysql_hash", "mysqlhash")):
            await self._compute_mhash()
        elif self.command.startswith(("pwd", "passwd", "cpwd", "cpasswd", "clear_pwd")):
            await self._compute_cpwd()
        elif self.command.startswith("help"):
            await self._show_help()
        else:
            await self._unknown_command()

    async def _network_ping(self):
        response = ""
        if len(self.args) == 2 and self.args[1].isnumeric():
            response = network.network_ping(self.args[0], self.args[1])
        elif len(self.args) == 1:
            response = network.network_ping(self.args[0], 1)
        else:
            response = "Give me at least one URL...."
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _network_reach(self):
        """reach website et return HTTP code"""
        response = ""
        if self.args:
            if len(self.args) == 1:
                if checkers.is_url(self.args[0]):
                    response = network.network_reach(self.args[0],"")
                url = "https://" + self.args[0]
                if checkers.is_url(url):
                    response = network.network_reach(self.args[0],"")
            if len(self.args) == 2:
                if checkers.is_url(self.args[0]) and self.args[1] == "details":
                    response = network.network_reach(self.args[0],"details")
                url = "https://" + self.args[0]
                if checkers.is_url(url):
                    response = network.network_reach(self.args[0],"details")

        else:
            response = "Im not soothsayer...Give me an url !"
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _network_mailbox(self):
        """Get stats from mailbox"""
        response = ""
        if self.args:
            if self.args[0] in ("clearall", "clear", "get"):
                response = network.network_mailbox(self.args[0])
        else:
            response = network.network_mailbox("get")
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _network_bonjourmadame(self):
        """ get image URL from bonjourmadame site """
        if self.args:
            if self.args[0] in ["random", "latest"]:
                response = network.network_bonjourmadame(self.args[0])
        else:
            response = network.network_bonjourmadame("random")
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _compute_uhash(self):
        response = ""
        if self.args and self.args[0].isnumeric():
            response = compute.compute_uhash(int(self.args[0]))
        else:
            response = compute.compute_uhash(count=1)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _compute_mhash(self):
        response = ""
        if self.args and self.args[0].isnumeric():
            response = compute.compute_mhash(int(self.args[0]))
        else:
            response = compute.compute_mhash(count=1)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _compute_cpwd(self):
        response = ""
        if self.args and self.args[0].isnumeric():
            response = compute.compute_cpwd(int(self.args[0]))
        else:
            response = compute.compute_cpwd(count=1)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _compute_kamoulox(self):
        response = compute.compute_kamoulox("kamoulox")
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _compute_kamoulautre(self):
        response = compute.compute_kamoulox(self.command)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = (
                "Hello, I am Alfred, your new Companion ! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.client, self.room.room_id, text)
            return
        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "* !ping dot.com * !reach dot.com * !mbox | !mailbox clearall * !bjm | !bonjourmadame * !uh | !uhash | !user_hash | !userhash * !mh | !mhash | !mysql_hash | !mysqlhash * !pwd | !passwd | !cpwd | !cpasswd !clear_pwd"
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )
