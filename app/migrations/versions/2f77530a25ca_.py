"""empty message

Revision ID: 2f77530a25ca
Revises: 0cd568c7c318
Create Date: 2024-04-13 12:33:13.703701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f77530a25ca'
down_revision = '0cd568c7c318'
branch_labels = None
depends_on = None


def upgrade():
    # Create an association table for many-to-many relationship between Events and Flairs
    op.create_table('flair_event_association',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('flair_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.eventID'], name='fk_event_id'),
        sa.ForeignKeyConstraint(['flair_id'], ['flair.flairID'], name='fk_flair_id'),
        sa.PrimaryKeyConstraint('event_id', 'flair_id')
    )
    
    # Modify the Flair table to drop unnecessary columns and adjust foreign keys
    with op.batch_alter_table('flair', schema=None) as batch_op:
        batch_op.drop_column('eventID')
        batch_op.drop_column('flairone')
        batch_op.drop_column('flairtwo')
        batch_op.drop_column('flarirthree')
        batch_op.add_column(sa.Column('name', sa.String(length=80), nullable=True))

def downgrade():
    with op.batch_alter_table('flair', schema=None) as batch_op:
        batch_op.add_column(sa.Column('flarirthree', sa.VARCHAR(length=80), nullable=True))
        batch_op.add_column(sa.Column('flairtwo', sa.VARCHAR(length=80), nullable=True))
        batch_op.add_column(sa.Column('flairone', sa.VARCHAR(length=80), nullable=True))
        batch_op.add_column(sa.Column('eventID', sa.INTEGER(), nullable=True))
        batch_op.drop_column('name')
    
    op.drop_table('flair_event_association')
