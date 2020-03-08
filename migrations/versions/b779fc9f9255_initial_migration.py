"""Initial migration.

Revision ID: b779fc9f9255
Revises: 
Create Date: 2020-03-08 13:16:41.472090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b779fc9f9255'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('router',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_router_ipaddress'), 'router', ['ipaddress'], unique=True)
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_settings_name'), 'settings', ['name'], unique=True)
    op.create_table('switch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=True),
    sa.Column('vendor', sa.String(length=16), nullable=True),
    sa.Column('uplinkports', sa.String(length=32), nullable=True),
    sa.Column('community', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_switch_ipaddress'), 'switch', ['ipaddress'], unique=True)
    op.create_index(op.f('ix_switch_vendor'), 'switch', ['vendor'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_switch_vendor'), table_name='switch')
    op.drop_index(op.f('ix_switch_ipaddress'), table_name='switch')
    op.drop_table('switch')
    op.drop_index(op.f('ix_settings_name'), table_name='settings')
    op.drop_table('settings')
    op.drop_index(op.f('ix_router_ipaddress'), table_name='router')
    op.drop_table('router')
    # ### end Alembic commands ###