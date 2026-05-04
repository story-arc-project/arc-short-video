# Importing fonts before any sibling component runs guarantees bundled OTFs
# are registered with Pango while ``Text(...)`` mobjects haven't been built
# yet — manimpango ignores registrations made after the first Text instance.
from . import fonts  # noqa: F401
