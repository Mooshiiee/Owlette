"""added flair model

Revision ID: 9970bcb483e4
Revises: 4d683edc4ded
Create Date: 2024-04-18 12:09:08.613385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9970bcb483e4'
down_revision = '4d683edc4ded'
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
    sa.UniqueConstraint('eventID'),
    sa.UniqueConstraint('userID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rsvp')
    # ### end Alembic commands ###
