"""init

Revision ID: c82a52c237f4
Revises: 
Create Date: 2023-07-10 16:09:39.241147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c82a52c237f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pits',
        sa.Column('id_pit', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'phases',
        sa.Column('id_phase', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('id_pit', sa.Integer, sa.ForeignKey('pits.id_pit'))
    )


def downgrade() -> None:
    op.drop_table('phases')
    op.drop_table('pits')