"""Disk bus

Revision ID: 7132a60093ce
Revises: 37298ef77ee8
Create Date: 2021-12-28 12:04:25.637691+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7132a60093ce'
down_revision = '37298ef77ee8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_disk', schema=None) as batch_op:
        batch_op.add_column(sa.Column('disk_bus', sa.String(length=20), nullable=False, server_default="UNKNOWN"))
        batch_op.add_column(sa.Column('disk_lunid', sa.String(length=30), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_disk', schema=None) as batch_op:
        batch_op.drop_column('disk_lunid')
        batch_op.drop_column('disk_bus')

    # ### end Alembic commands ###
