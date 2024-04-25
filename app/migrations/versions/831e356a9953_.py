"""empty message

Revision ID: 831e356a9953
Revises: 474342b9bcb6
Create Date: 2024-04-24 20:42:58.724314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '831e356a9953'
down_revision = '474342b9bcb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('commentID', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('eventID', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['eventID'], ['event.eventID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('commentID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
