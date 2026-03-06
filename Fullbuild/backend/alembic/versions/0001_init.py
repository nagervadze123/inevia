"""init

Revision ID: 0001
Revises:
Create Date: 2026-03-06
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('email', sa.String(255), nullable=False, unique=True), sa.Column('password_hash', sa.String(255), nullable=False), sa.Column('plan', sa.String(64), nullable=True), sa.Column('created_at', sa.DateTime(), nullable=True))
    op.create_table('projects', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('name', sa.String(255), nullable=False), sa.Column('status', sa.String(50)), sa.Column('niche', sa.String(255)), sa.Column('target_market', sa.String(255)), sa.Column('platform_targets', sa.JSON()), sa.Column('created_at', sa.DateTime()))
    op.create_table('signals', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('source_type', sa.String(100)), sa.Column('query', sa.String(255)), sa.Column('payload_json', sa.JSON()), sa.Column('fetched_at', sa.DateTime()))
    op.create_table('opportunities', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('title', sa.String(255)), sa.Column('confidence_score', sa.Integer()), sa.Column('demand_score', sa.Integer()), sa.Column('competition_score', sa.Integer()), sa.Column('profit_score', sa.Integer()), sa.Column('differentiation_json', sa.JSON()), sa.Column('created_at', sa.DateTime()))
    op.create_table('strategy_docs', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('version', sa.Integer()), sa.Column('strategy_json', sa.JSON()), sa.Column('created_at', sa.DateTime()))
    op.create_table('assets', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('asset_type', sa.String(100)), sa.Column('format', sa.String(50)), sa.Column('storage_url', sa.Text()), sa.Column('meta_json', sa.JSON()), sa.Column('created_at', sa.DateTime()))
    op.create_table('listings', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('platform', sa.String(20)), sa.Column('listing_json', sa.JSON()), sa.Column('created_at', sa.DateTime()))
    op.create_table('content_calendars', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('platform', sa.String(20)), sa.Column('month', sa.String(20)), sa.Column('calendar_json', sa.JSON()), sa.Column('created_at', sa.DateTime()))
    op.create_table('runs', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False), sa.Column('run_type', sa.String(64)), sa.Column('status', sa.String(20)), sa.Column('started_at', sa.DateTime()), sa.Column('finished_at', sa.DateTime()), sa.Column('tokens_used', sa.Integer()), sa.Column('cost_estimate', sa.Float()), sa.Column('error_json', sa.JSON()), sa.Column('idempotency_key', sa.Text(), nullable=False, unique=True))


def downgrade() -> None:
    for t in ['runs','content_calendars','listings','assets','strategy_docs','opportunities','signals','projects','users']:
        op.drop_table(t)
