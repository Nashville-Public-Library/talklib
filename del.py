from talklib import TLPod

poetry = TLPod(
    display_name="Delete this",
    filename_to_match="poetry"
)
poetry.notifications.notify.enable_all = False
a = poetry.match_file()
print(poetry.display_name)
print(a)