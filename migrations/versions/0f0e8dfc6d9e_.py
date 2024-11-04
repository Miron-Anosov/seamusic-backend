"""empty message

Revision ID: 0f0e8dfc6d9e
Revises: 0e04006c1c8b
Create Date: 2024-11-04 13:25:52.195187

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f0e8dfc6d9e"
down_revision: Union[str, None] = "0e04006c1c8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_to_playlists_author_association",
        sa.Column("playlist_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["playlist_id"],
            ["playlists.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("playlist_id", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_to_playlists_author_association")
    # ### end Alembic commands ###
