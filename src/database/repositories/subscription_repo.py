"""Handles all database operations regarding subscriptions."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Subscription


async def create_subscription(
    session: AsyncSession,
    user_id: int,
    skin_id: int,
) -> Subscription:
    """Creates a subscription for a user with their chosen skin.

    Args:
        session (AsyncSession): Active request-scoped database session.
        user_id (int): The users discord id.
        skin_id (int): The id of the skin.

    Returns:
        Subscription: Object containing the data about the subscription.
    """
    subscription = Subscription(user_id=user_id, skin_id=skin_id)
    session.add(subscription)
    await session.commit()

    return subscription
