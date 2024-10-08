"""username is unique

Revision ID: e6e2ea4638fb
Revises: 17d39bf5a4ef
Create Date: 2024-07-30 20:28:51.001843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6e2ea4638fb'
down_revision: Union[str, None] = '17d39bf5a4ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
