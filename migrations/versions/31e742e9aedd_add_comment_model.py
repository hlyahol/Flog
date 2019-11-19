"""add comment model

Revision ID: 31e742e9aedd
Revises: c8bc4d8ab74c
Create Date: 2019-11-18 21:29:47.762962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "31e742e9aedd"
down_revision = "c8bc4d8ab74c"
branch_labels = None
depends_on = None

user_table = sa.table(
    "user",
    sa.column("id", sa.Integer()),
    sa.column("username", sa.String(64)),
    sa.column("email", sa.String(100)),
    sa.column("password", sa.String(200)),
    sa.column("settings", sa.Text()),
    sa.column("is_admin", sa.Boolean()),
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("floor", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("html", sa.Text(), nullable=True),
        sa.Column("create_at", sa.DateTime(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["user.id"],),
        sa.ForeignKeyConstraint(["parent_id"], ["comment.id"],),
        sa.ForeignKeyConstraint(["post_id"], ["post.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("post_id", "floor", name="_post_floor"),
    )
    op.drop_column("page", "comment")
    op.add_column("user", sa.Column("is_admin", sa.Boolean(), nullable=True))
    op.add_column("user", sa.Column("name", sa.String(100), nullable=True))
    op.create_unique_constraint("_username_email", "user", ["username", "email"])
    op.drop_constraint("user_username_key", "user", type_="unique")
    op.execute(user_table.update().values(is_admin=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("user_username_key", "user", ["username"])
    op.drop_constraint("_username_email", "user", type_="unique")
    op.drop_column("user", "is_admin")
    op.drop_column("user", "name")
    op.add_column(
        "page", sa.Column("comment", sa.BOOLEAN(), autoincrement=False, nullable=True)
    )
    op.drop_table("comment")
    # ### end Alembic commands ###