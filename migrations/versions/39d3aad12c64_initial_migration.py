"""Initial Migration

Revision ID: 39d3aad12c64
Revises: 
Create Date: 2023-12-22 13:56:44.152438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "39d3aad12c64"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "coupon",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("platform_apply", sa.String(length=50), nullable=False),
        sa.Column("platform_get", sa.String(length=50), nullable=False),
        sa.Column("expiry_date", sa.DateTime(), nullable=False),
        sa.Column("details", sa.Text(), nullable=False),
        sa.Column("date_posted", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("coupon")
    op.drop_table("user")
    # ### end Alembic commands ###
