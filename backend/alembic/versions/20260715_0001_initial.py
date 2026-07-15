"""Create users, machines, and alerts tables."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260715_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "ADMIN",
                "OPERATOR",
                "VIEWER",
                name="userrole",
                native_enum=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)

    op.create_table(
        "machines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=40), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=120), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "OPERATIONAL",
                "WARNING",
                "CRITICAL",
                "OFFLINE",
                name="machinestatus",
                native_enum=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("temperature_celsius", sa.Float(), nullable=False),
        sa.Column("vibration_mm_s", sa.Float(), nullable=False),
        sa.Column("output_rate", sa.Float(), nullable=False),
        sa.Column("efficiency_percent", sa.Float(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_machines")),
    )
    op.create_index(op.f("ix_machines_code"), "machines", ["code"], unique=True)
    op.create_index(op.f("ix_machines_location"), "machines", ["location"], unique=False)
    op.create_index(op.f("ix_machines_name"), "machines", ["name"], unique=False)
    op.create_index(op.f("ix_machines_status"), "machines", ["status"], unique=False)

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("machine_id", sa.Integer(), nullable=False),
        sa.Column(
            "severity",
            sa.Enum(
                "INFO",
                "WARNING",
                "CRITICAL",
                name="alertseverity",
                native_enum=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "ACKNOWLEDGED",
                "RESOLVED",
                name="alertstatus",
                native_enum=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("acknowledged_by_id", sa.Integer(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["acknowledged_by_id"], ["users.id"], name=op.f("fk_alerts_acknowledged_by_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["machine_id"], ["machines.id"], name=op.f("fk_alerts_machine_id_machines")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_alerts")),
    )
    op.create_index(op.f("ix_alerts_detected_at"), "alerts", ["detected_at"], unique=False)
    op.create_index(op.f("ix_alerts_machine_id"), "alerts", ["machine_id"], unique=False)
    op.create_index(op.f("ix_alerts_severity"), "alerts", ["severity"], unique=False)
    op.create_index(op.f("ix_alerts_status"), "alerts", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("machines")
    op.drop_table("users")
