"""empty message

Revision ID: a690454733a4
Revises: a7f7350f9197
Create Date: 2024-05-03 15:19:37.833094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a690454733a4'
down_revision = 'a7f7350f9197'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rsvp',
    sa.Column('rsvpID', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('eventID', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['eventID'], ['event.eventID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('rsvpID'),
    sa.UniqueConstraint('userID', 'eventID', name='unique_rsvp_per_user_event')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rsvp')
    # ### end Alembic commands ###
