"""Tests for subscription functionality."""

from sqlalchemy import select

from src.database.models import Subscription
from src.database.repositories import subscription_repo as repo
from src.database.session import AsyncSessionLocal


async def test_subscription_creation(db_session, seed_user, seed_skin):
    """Tests that a subscription is actually created and added to the db.

    Creates a second session for the query to make sure that it was actually committed
    to the db.
    """
    subscription = await repo.create_subscription(
        db_session, skin_id=seed_skin.id, user_id=seed_user.discord_id
    )

    async with AsyncSessionLocal() as verification_session:
        result = await verification_session.execute(
            select(Subscription).where(
                Subscription.user_id == seed_user.discord_id,
                Subscription.skin_id == seed_skin.id,
            )
        )

        saved_subscription = result.scalar_one()

        assert saved_subscription.id == subscription.id
