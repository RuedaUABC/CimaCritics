"""Agregar comics guardados

Revision ID: 4a8f0b7e9d31
Revises: 2c8d8a6c1f20
Create Date: 2026-05-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '4a8f0b7e9d31'
down_revision = '2c8d8a6c1f20'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if 'comic_guardado' not in inspector.get_table_names():
        op.create_table(
            'comic_guardado',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('usuario_id', sa.Integer(), nullable=False),
            sa.Column('comic_id', sa.Integer(), nullable=False),
            sa.Column('fecha_guardado', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id']),
            sa.ForeignKeyConstraint(['comic_id'], ['comic.id']),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('usuario_id', 'comic_id', name='uq_comic_guardado_usuario'),
        )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if 'comic_guardado' in inspector.get_table_names():
        op.drop_table('comic_guardado')
