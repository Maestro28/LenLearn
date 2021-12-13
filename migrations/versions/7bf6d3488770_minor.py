"""minor

Revision ID: 7bf6d3488770
Revises: 71db908d1b53
Create Date: 2021-12-13 11:46:07.749670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bf6d3488770'
down_revision = '71db908d1b53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_vocabular_timestamp', table_name='vocabular')
    op.create_index(op.f('ix_vocabular_last_check'), 'vocabular', ['last_check'], unique=False)
    op.drop_column('vocabular', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vocabular', sa.Column('timestamp', sa.DATETIME(), nullable=True))
    op.drop_index(op.f('ix_vocabular_last_check'), table_name='vocabular')
    op.create_index('ix_vocabular_timestamp', 'vocabular', ['timestamp'], unique=False)
    # ### end Alembic commands ###