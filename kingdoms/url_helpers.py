"""URL generation helpers for kingdom views."""

from django.urls import reverse


def kingdom_url(name, kingdom_pk, **kwargs):
    """Generate kingdoms: namespace URL with kingdom pk.

    Args:
        name: URL pattern name (without 'kingdoms:' prefix)
        kingdom_pk: Primary key of the kingdom
        **kwargs: Additional URL kwargs

    Returns:
        Reversed URL string
    """
    return reverse(f"kingdoms:{name}", kwargs={"pk": kingdom_pk, **kwargs})


def turn_url(name, kingdom_pk, turn_pk, **kwargs):
    """Generate turn-specific URL.

    Args:
        name: URL pattern name (without 'turns:' prefix)
        kingdom_pk: Primary key of the kingdom
        turn_pk: Primary key of the turn
        **kwargs: Additional URL kwargs

    Returns:
        Reversed URL string
    """
    return reverse(
        f"turns:{name}",
        kwargs={"pk": kingdom_pk, "turn_pk": turn_pk, **kwargs},
    )
