from ..db import db
import datetime

class Milestone(db.Document):
    """
    Milestone model for representing project milestones.
    
    Attributes:
        title (str): Title of the milestone.
        description (str): Description of the milestone.
        due_date (datetime): Deadline for the milestone.
        project (Project): Reference to the associated project.
        created_at (datetime): Timestamp when the milestone was created.
        updated_at (datetime): Timestamp when the milestone was last updated.
    """
    title = db.StringField(max_length=128, required=True)
    description = db.StringField()
    due_date = db.DateTimeField()
    project = db.ReferenceField("Project", required=True, reverse_delete_rule=db.CASCADE)  # Milestones are deleted if the associated project is deleted.
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        """
        String representation of the Milestone instance.
        """
        return f"<Milestone {self.title}>"

    def to_dict(self):
        """
        Serialize the milestone instance to a dictionary format for API responses.
        
        Returns:
            dict: Dictionary representation of the milestone instance.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "project": str(self.project.id) if self.project else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
