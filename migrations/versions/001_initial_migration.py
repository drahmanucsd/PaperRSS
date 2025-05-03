"""initial migration

Revision ID: 001
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create Paper table
    op.create_table('paper',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doi', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('journal', sa.String(length=200), nullable=False),
        sa.Column('link', sa.String(length=500), nullable=False),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('impact_factor', sa.Float(), nullable=True),
        sa.Column('pub_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('doi')
    )

    # Create Digest table
    op.create_table('digest',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('date')
    )

    # Create digest_papers association table
    op.create_table('digest_papers',
        sa.Column('digest_id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['digest_id'], ['digest.id'], ),
        sa.ForeignKeyConstraint(['paper_id'], ['paper.id'], ),
        sa.PrimaryKeyConstraint('digest_id', 'paper_id')
    )

    # Create Vote table with used_for_prefs
    op.create_table('vote',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paper_doi', sa.String(length=100), nullable=False),
        sa.Column('vote', sa.String(length=4), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('used_for_prefs', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['paper_doi'], ['paper.doi'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('vote')
    op.drop_table('digest_papers')
    op.drop_table('digest')
    op.drop_table('paper') 