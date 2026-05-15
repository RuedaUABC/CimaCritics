"""Agregar listas a comics guardados

Revision ID: a4d2f6c8b910
Revises: 4a8f0b7e9d31
Create Date: 2026-05-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a4d2f6c8b910'
down_revision = '4a8f0b7e9d31'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if 'comic_guardado' not in inspector.get_table_names():
        return

    columns = {column['name'] for column in inspector.get_columns('comic_guardado')}
    if 'lista' not in columns:
        with op.batch_alter_table('comic_guardado') as batch_op:
            batch_op.add_column(sa.Column('lista', sa.String(length=64), nullable=False, server_default='Guardados'))

    unique_constraints = {constraint['name'] for constraint in inspector.get_unique_constraints('comic_guardado')}
    with op.batch_alter_table('comic_guardado') as batch_op:
        if 'uq_comic_guardado_usuario' in unique_constraints:
            batch_op.drop_constraint('uq_comic_guardado_usuario', type_='unique')
        if 'uq_comic_guardado_usuario_lista' not in unique_constraints:
            batch_op.create_unique_constraint(
                'uq_comic_guardado_usuario_lista',
                ['usuario_id', 'comic_id', 'lista'],
            )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if 'comic_guardado' not in inspector.get_table_names():
        return

    unique_constraints = {constraint['name'] for constraint in inspector.get_unique_constraints('comic_guardado')}
    columns = {column['name'] for column in inspector.get_columns('comic_guardado')}
    with op.batch_alter_table('comic_guardado') as batch_op:
        if 'uq_comic_guardado_usuario_lista' in unique_constraints:
            batch_op.drop_constraint('uq_comic_guardado_usuario_lista', type_='unique')
        if 'uq_comic_guardado_usuario' not in unique_constraints:
            batch_op.create_unique_constraint('uq_comic_guardado_usuario', ['usuario_id', 'comic_id'])
        if 'lista' in columns:
            batch_op.drop_column('lista')
