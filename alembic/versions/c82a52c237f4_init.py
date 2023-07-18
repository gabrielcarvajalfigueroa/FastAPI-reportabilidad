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
    # Se necesita agregar un constraint para que pueda ser llamada como FK en daily_report
    op.create_unique_constraint("uq_phases_name", "phases", ["name"])

    op.create_table(
        'daily_reports',
        sa.Column('daily_report', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('phase', sa.String(), sa.ForeignKey('phases.name')),
        sa.Column('real', sa.Integer, nullable=False),
        sa.Column('ISO_weekly', sa.Integer, nullable=False),
        sa.Column('movil_weekly', sa.Integer, nullable=False),
        sa.Column('month_real', sa.Integer, nullable=False),
        sa.Column('annual_real', sa.Integer, nullable=False)
    )

    op.create_table(
        'users',
        sa.Column('id_user', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('is_admin', sa.Boolean, nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'users_requests',
        sa.Column('id_request', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('message', sa.String(), nullable=False)        
    )

def downgrade() -> None:
    op.drop_table('phases')
    op.drop_table('pits')
    op.drop_table('daily_reports')
    op.drop_table('users')
    op.drop_table('users_request')