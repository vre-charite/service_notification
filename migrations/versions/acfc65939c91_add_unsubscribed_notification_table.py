# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

"""Add unsubscribed_notifications table.

Revision ID: acfc65939c91
Revises: f7b7903f78c4
Create Date: 2022-01-21 11:54:15.802511
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'acfc65939c91'
down_revision = 'f7b7903f78c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'unsubscribed_notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('notification_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='notifications',
    )


def downgrade():
    op.drop_table('unsubscribed_notifications', schema='notifications')
