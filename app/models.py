from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime, timezone

class User(db.Model):
    user_id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    first_name: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    last_name: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    email: so.Mapped[str] = so.mapped_column(unique=True, nullable=False, index=True)
    password: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    role: so.Mapped[str] = so.mapped_column(nullable=False, index=True)

    def __repr__(self):
        return f'<Login {self.user_id}, {self.last_name}, {self.first_name}, {self.email}, {self.role}>'

class HealthRecord(db.Model):
    record_id: so.Mapped[int] = so.mapped_column(primary_key=True, nullable=False, index=True)
    patient_id: so.Mapped[int] = so.mapped_column(unique=True, nullable=False, index=True)
    date: so.Mapped[datetime] = so.mapped_column(sa.DATE, nullable=False, index=True)
    status: so.Mapped[str] = so.mapped_column(nullable=False, index=True)

class Checkup(db.Model):
    checkup_id: so.Mapped[int] = so.mapped_column(primary_key=True, nullable=False, index=True)
    patient_last_name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, index=True)
    patient_first_name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, index=True)
    checkup_date: so.Mapped[datetime] = so.mapped_column(sa.DATE, nullable=False, default=lambda: datetime.now(timezone.utc))
    medication: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, index=True)
    dosage: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, index=True)
    notes: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, index=True)

    def __repr__(self):
        return (f'<Checkup {self.checkup_id}, {self.patient_last_name}, {self.patient_first_name}, '
                f'{self.checkup_date}, {self.medication}, {self.dosage}, {self.notes}>')
