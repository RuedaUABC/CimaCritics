"""Agregar votos de reviews

Revision ID: 2c8d8a6c1f20
Revises: 7ebed57b40a4
Create Date: 2026-05-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '2c8d8a6c1f20'
down_revision = '7ebed57b40a4'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    tables = inspector.get_table_names()

    if 'voto_review' not in tables:
        op.create_table(
            'voto_review',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('review_id', sa.Integer(), nullable=False),
            sa.Column('usuario_id', sa.Integer(), nullable=False),
            sa.Column('tipo', sa.String(length=8), nullable=False),
            sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['review_id'], ['review.id']),
            sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id']),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('review_id', 'usuario_id', name='uq_voto_review_usuario'),
        )

    if 'seguimiento' in tables:
        with op.batch_alter_table('seguimiento') as batch_op:
            batch_op.create_unique_constraint('uq_seguimiento_usuarios', ['seguidor_id', 'seguido_id'])


def downgrade():
    inspector = sa.inspect(op.get_bind())
    tables = inspector.get_table_names()

    if 'seguimiento' in tables:
        with op.batch_alter_table('seguimiento') as batch_op:
            batch_op.drop_constraint('uq_seguimiento_usuarios', type_='unique')
    if 'voto_review' in tables:
        op.drop_table('voto_review')
