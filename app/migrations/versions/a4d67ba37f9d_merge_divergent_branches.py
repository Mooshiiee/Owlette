"""Merge divergent branches

Revision ID: a4d67ba37f9d
Revises: 4ae0d5305dd5, 831e356a9953
Create Date: 2024-04-25 16:35:35.524244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4d67ba37f9d'
down_revision = ('4ae0d5305dd5', '831e356a9953')
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('rsvp', schema=None) as batch_op:
        batch_op.drop_constraint('unique_user_id', type_='unique')  # Check the actual name in your DB
        batch_op.create_unique_constraint('unique_rsvp_per_user_event', ['userID', 'eventID'])

def downgrade():
    with op.batch_alter_table('rsvp', schema=None) as batch_op:
        batch_op.drop_constraint('unique_rsvp_per_user_event', type_='unique')
        batch_op.create_unique_constraint('unique_user_id', ['userID'])  # This is illustrative; adjust as needed