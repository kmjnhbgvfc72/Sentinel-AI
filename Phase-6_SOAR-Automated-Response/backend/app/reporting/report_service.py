from models import Incident, Report


class ReportService:
    def __init__(self, session):
        self.session = session

    def generate(self):
        rows = self.session.query(Incident).all()
        report = Report(
            report_type="incident_summary",
            title="Incident Summary",
            content=f"Total incidents: {len(rows)}",
        )
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report
